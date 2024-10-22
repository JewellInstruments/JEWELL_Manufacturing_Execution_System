import sys
import logging
import time

# import random

from system import stage_configuration
from system import serial_protocols


def get_plate_temp(port):
    if stage_configuration.DAQ_IDN == "HEWLETT-PACKARD":
        serial_protocols.serial_write(port, "FETCH?\n")  # request data FETCH?
        data_array = serial_protocols.serial_read(port)  # read the com port
    elif stage_configuration.DAQ_IDN == "KEITHLEY":
        for _ in range(2):
            serial_protocols.serial_write(port, ":TRAC:CLE\r")  # clear the buffer
            serial_protocols.serial_write(
                port, "ROUT:SCAN:TSO IMM\r"
            )  # prepare the scan
            serial_protocols.serial_write(
                port, "ROUT:SCAN:LSEL INT\r"
            )  # prepare the scan
            serial_protocols.serial_write(port, "*CLS\r")
            serial_protocols.serial_write(port, "READ?\r")  # record data
            data_array = serial_protocols.serial_read(port)  # read the com port

    return float(data_array.replace("+", "").split(",")[0])


def read_error_from_data_aq(port: serial_protocols.serial_open) -> None:
    while True:
        serial_protocols.serial_write(port, "SYST:ERR?\r")  # record data
        raw = serial_protocols.serial_read(port, "CR")  # read the com port
        if raw.split(",")[0] == "0":
            break
        else:
            print(raw)


def read_data_from_data_aq(
    port: serial_protocols.serial_open, mode: str, channels: int, offset: int = 0
) -> dict:
    # everything here is in V, A...
    t0 = time.time()
    loop_time = 0

    while loop_time < stage_configuration.DAQ_TIMEOUT:
        data, key = get_data_from_data_aq(port)
        # logging.warning(data)
        loop_time = time.time() - t0
        if data != []:
            break

    xy_scalar = 1.0 * 1e1 if mode.upper() == "Current" else 1e0
    temp_scalar = 1.0  # no scaling required
    keymap = stage_configuration.DIFF_PORT_CONFIG

    data_array = {}
    array_buffer = {}
    try:
        for index in range(1, channels + 1):
            try:
                dict_key = f"PORT_{index}"
                x = round(data[key[keymap[dict_key][0]]] * xy_scalar, 6)
                y = round(data[key[keymap[dict_key][1]]] * xy_scalar, 6)
                t = round((data[key[keymap[dict_key][2]]] - offset) * temp_scalar, 3)
            except Exception as e:
                *_, exc_tb = sys.exc_info()
                logging.warning(f"\t{e} -> Line {exc_tb.tb_lineno}")

            array_buffer[dict_key] = [x, y, t]

        # T_air = 22.5  # round(data[-1],3)
        # T_plate = 22.5  # round(data[-2],3)
        # array_buffer["TEMP"] = [T_air, T_plate]
        data_array = array_buffer

    except Exception as e:
        *_, exc_tb = sys.exc_info()
        logging.warning(f"\t{e} -> Line {exc_tb.tb_lineno}")

    finally:
        return data_array


def get_data_from_data_aq(port: serial_protocols.serial_open) -> tuple[list, dict]:
    data_array = []
    key = {}
    j = 0
    NULL = []

    if stage_configuration.DAQ_IDN == "HEWLETT-PACKARD":
        serial_protocols.serial_write(port, "FETCH?\n")  # request data FETCH?
        data_array = serial_protocols.serial_read(port)  # read the com port
    elif stage_configuration.DAQ_IDN == "KEITHLEY":
        for _ in range(2):
            serial_protocols.serial_write(port, ":TRAC:CLE\r")  # clear the buffer
            serial_protocols.serial_write(
                port, "ROUT:SCAN:TSO IMM\r"
            )  # prepare the scan
            serial_protocols.serial_write(
                port, "ROUT:SCAN:LSEL INT\r"
            )  # prepare the scan
            serial_protocols.serial_write(port, "*CLS\r")
            serial_protocols.serial_write(port, "READ?\r")  # record data
            raw = serial_protocols.serial_read(port)  # read the com port

        raw = raw.rstrip().split(",")

        if len(raw) > 1:
            try:
                for i in range(len(raw)):
                    if i % 2 == 0:
                        buf = float(raw[i].replace("+", ""))
                        data_array.append(buf)
                        key[raw[i + 1]] = j
                        j += 1
                # reopen all channels
                # serial_protocols.serial_write(port, ":ROUT:OPEN:ALL\r")
                logging.debug("\tDone scanning, returning values now...")
                return data_array, key
            except Exception as e:
                print(e)
                return NULL, key
        else:
            # reopen all channels
            serial_protocols.serial_write(port, ":ROUT:OPEN:ALL\r")
            logging.debug("\tDone scanning, returning values now...")
            return NULL, key

    else:
        logging.warning("DAQ not setup...")
        return NULL, key
