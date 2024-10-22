import time

from system import serial_protocols

# this file contains basic instrument primitives and basic calculations


# colorizes text - only works for terminal prints, does not work with QT windows
# color codes: black:30m, red:31m, green:32m, yellow:33m, blue:34m, magenta:35m, cyan:36m, white:37m
# style codes: none:0m, bold:1m, underline:4m, blinking:5m
# example: for bold green text use colorize("myText", '1:32')
def colorize(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"


# communicates with global database for serialization, should be called early in production of assemblies
def createSerialNumber(handler, partNumber: str, jobNumber: str):
    serialInfo = {"part_number": partNumber, "work_order": jobNumber}
    response = handler.post("serial_number/", serialInfo)
    return response.data["serial_number"]


# checks that a given measurement is within tolerance (all inputs need common units), returns bool
def measurement_within_tol(measurement: float, target: float, tolerance: float):
    return (measurement <= target + tolerance) and (measurement >= target - tolerance)


# function to create a channel scan on a DAQ with a given SCPI function (.1sec delay, <cycles> number of repeat scans)
def createScanAndRead(instr, func: str, chanStart: int, chanEnd: int, cycles: int):
    serial_protocols.socket_write(
        instr, f"SENS:FUNC '{func}', (@{chanStart}:{chanEnd})\r\n"
    )
    serial_protocols.socket_write(instr, f"ROUT:DEL .1, (@{chanStart}:{chanEnd})\r\n")
    serial_protocols.socket_write(instr, f"ROUT:SCAN:COUN:SCAN {cycles}\r\n")
    serial_protocols.socket_write(instr, f"ROUT:SCAN:CRE (@{chanStart}:{chanEnd})\r\n")
    serial_protocols.socket_write(instr, "INIT\r\n")
    serial_protocols.socket_write(instr, "*WAI\r\n")

    # waiting time is for pyvisa timeouts - maybe just add it to the actual resource manager?
    time.sleep(1.6 * cycles)

    serial_protocols.socket_write(instr, "ROUT:OPEN:ALL\r\n")
    serial_protocols.socket_write(instr, ":TRAC:ACT:STAR?\r\n")
    buffer_start = serial_protocols.socket_read(instr)
    buffer_start = buffer_start.strip("\n")
    serial_protocols.socket_write(instr, ":TRAC:ACT:END?\r\n")
    buffer_end = serial_protocols.socket_read(instr)
    buffer_end = buffer_end.strip("\n")

    # put data in the buffer, convert to float
    serial_protocols.socket_write(
        instr, f':TRAC:DATA? {buffer_start}, {buffer_end}, "defbuffer1", READ\r\n'
    )
    list = serial_protocols.socket_read(instr)
    list = list.split(",")
    for item in range(0, len(list)):
        list[item] = float(list[item])

    return list


# function to turn a power supply channel on at a given voltage
def powerSupplyChanOn(instr, chan: int, voltage: float, maxAmp: float):
    serial_protocols.socket_write(instr, f"APPL CH{chan},{voltage},{maxAmp}\r\n")
    serial_protocols.socket_write(instr, f"OUTP CH{chan}, ON\r\n")


# function to turn a power supply channel off, sets voltage to 0
def powerSupplyChanOff(instr, chan: int):
    serial_protocols.socket_write(instr, f"OUTP CH{chan}, OFF\r\n")
    serial_protocols.socket_write(instr, f"APPL CH{chan},0,.3\r\n")
