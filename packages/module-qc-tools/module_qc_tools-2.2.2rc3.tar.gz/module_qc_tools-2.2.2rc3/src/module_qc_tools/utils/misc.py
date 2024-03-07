#!/usr/bin/env python3
from __future__ import annotations

import json
import logging
from pathlib import Path

import jsonschema
from jsonschema import validate

from module_qc_tools import data

log = logging.getLogger("measurement")


def get_chip_type(config):
    chiptype = ""
    try:
        chiptype = next(iter(config))
    except IndexError:
        log.error(
            bcolors.BADRED
            + "One of your chip configuration files is empty"
            + bcolors.ENDC
        )

    if chiptype not in {"RD53B", "ITKPIXV2"}:
        log.warning(
            bcolors.WARNING
            + "Chip name in configuration not one of expected chip names (RD53B or ITKPIXV2)"
            + bcolors.ENDC
        )
    return chiptype


def get_identifiers(config):
    identifiers = {}
    chiptype = get_chip_type(config)
    identifiers["ChipID"] = config[chiptype]["Parameter"]["ChipId"]
    identifiers["Name"] = config[chiptype]["Parameter"]["Name"]
    identifiers["Institution"] = ""
    identifiers["ModuleSN"] = ""
    return identifiers


def get_meta_data(config):
    return {
        "FirmwareVersion": "",
        "FirmwareIdentifier": "",
        "ChannelConfig": "",
        "SoftwareVersion": "",
        "ChipConfigs": config,
        "SoftwareType": "",
    }


class bcolors:
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    BADRED = "\033[91m"
    ENDC = "\033[0m"


def check_meas_config(input_data, path):
    info_schema_path = str(data / "schema/config.json")
    with Path(info_schema_path).open(encoding="utf-8") as inFile:
        info_schema = json.load(inFile)
    try:
        validate(instance=input_data, schema=info_schema)
    except jsonschema.exceptions.ValidationError as err:
        log.error(
            bcolors.BADRED
            + "Input measurement config fails schema check with the following error:"
            + bcolors.ENDC
        )
        log.error(bcolors.BADRED + f"Input config: {path}" + bcolors.ENDC)
        log.error(bcolors.BADRED + f"Json Schema: {info_schema_path}" + bcolors.ENDC)
        log.error(err.message)
        raise RuntimeError() from None


# Function to check that reading ground through ADC does return 0 counts
def check_adc_ground(yr, scan_config):
    vmux_gnd = yr.read_adc(
        30, readCurrent=False, rawCounts=True, share_vmux=scan_config["share_vmux"]
    )[0].split()
    imux_gnd = yr.read_adc(
        63, readCurrent=True, rawCounts=True, share_vmux=scan_config["share_vmux"]
    )[0].split()
    if any(int(x) != 0 for x in vmux_gnd) or any(int(x) != 0 for x in imux_gnd):
        log.error(
            bcolors.BADRED
            + f"Reading Vmux30(Imux63) (ground) through ADC gave {vmux_gnd}({imux_gnd}) counts - when it should be 0(0)! Please check."
            + bcolors.ENDC
        )
        raise RuntimeError()


# Convert micro-amps to voltages using rImux
# TODO: Decide if I should change read-adc script to return V instead
def microItoV(read_uA, yr):
    read_V = []
    for r, chip in zip(read_uA, range(yr._number_of_chips)):
        if chip in yr._disabled_chip_positions:
            continue
        try:
            rImux = yr.get_config(chip)["RD53B"]["Parameter"]["ADCcalPar"][2]
        except Exception:
            rImux = 4.99e3  # Default in YARR read-adc script
            log.warning(
                bcolors.WARNING
                + f"Unable to find rImux from ADCcalPar in chip config - using default rImux = {rImux} Ohm"
                + bcolors.ENDC
            )
        read_V += [r * 1e-6 * rImux]
    return read_V


# Function to read vmux through multimter or ADC, handles shared / separate vmux
def read_vmux(
    meter,
    yr,
    scan_config,
    chip_position=None,
    v_mux=-1,
    i_mux=-1,
    use_adc=False,
    raw_adc_counts=False,
):
    log.debug(
        f"Reading monitorV={v_mux}, monitorI={i_mux} with use_adc={use_adc} and raw_adc_counts={raw_adc_counts}"
    )
    reads = []

    # Read through ADC
    if use_adc:
        # Read ground as 0
        if (19 <= v_mux <= 30) or (i_mux == 63):
            for chip in range(yr._number_of_chips):
                if chip != chip_position and chip_position is not None:
                    continue
                reads.append(0.0)
        else:
            if i_mux > -1:
                read = yr.read_adc(
                    i_mux,
                    readCurrent=True,
                    rawCounts=raw_adc_counts,
                    chip_position=chip_position,
                    share_vmux=scan_config["share_vmux"],
                )[0]
            else:
                read = yr.read_adc(
                    v_mux,
                    readCurrent=False,
                    rawCounts=raw_adc_counts,
                    chip_position=chip_position,
                    share_vmux=scan_config["share_vmux"],
                )[0]
            try:
                if raw_adc_counts:
                    reads = [int(x) for x in read.split()]
                else:
                    reads = [float(x) for x in read.split()[0::2]]  # Remove units
            except Exception as e:
                log.error(f"Unable to decode return from read_adc: {read}")
                raise RuntimeError() from e

            # If we read current, we need to convert back to V
            if i_mux > -1:
                reads = microItoV(reads, yr)

            #  Fill in values at disabled chip positions
            for i in yr._disabled_chip_positions:
                if i != chip_position and chip_position is not None:
                    continue
                reads.insert(i, -999)

    # Read through multimeter
    else:
        for chip in range(yr._number_of_chips):
            if chip != chip_position and chip_position is not None:
                continue
            if chip in yr._disabled_chip_positions:
                reads.append(-999)
                continue
            yr.set_mux(
                chip_position=chip,
                v_mux=v_mux,
                i_mux=i_mux,
                reset_other_chips=scan_config["share_vmux"],
            )
            meas, _status = meter.measure_dcv(
                channel=scan_config["v_mux_channels"][chip]
            )
            reads.append(meas)

    return reads
