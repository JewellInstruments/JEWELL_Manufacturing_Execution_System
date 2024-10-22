import sys
import logging
import socket
import time

import serial

import pyvisa

import minimalmodbus
from typing import Union


def is_port_open(port):
    try:
        return 1 if port.isOpen() is True else 0
    except Exception:
        return 0


def serial_open(
    port: str = "",
    PortBaud: int = 9600,
    bytesize: int = 8,
    parity: str = "N",
    addr: int = 1,
    use_modbus: bool = False,
    use_visa: bool = True,
) -> None:
    """open a serial connection using modbus, pyserial, or pyvisa.

    Args:
        port (str, optional): can be COMxx, GPIB0::xx::INSTR, or ASRL::xx::INSTR. Defaults to "".
        PortBaud (int, optional): only used with pyserial. Defaults to 9600.
        bytesize (int, optional): only used with pyserial. Defaults to 8.
        parity (str, optional): only used with pyserial. Defaults to "N".
        addr (int, optional): only used with modbus. Defaults to 1.
        use_modbus (bool, optional): connect to modbus instrument. Defaults to False.
        use_visa (bool, optional): connect to instrument using pyvisa. Defaults to True.

    Returns:
        _type_: open connection to instrument
    """
    if use_modbus:
        device = minimalmodbus.Instrument(port, addr)  # , debug = True

        device.serial.baudrate = PortBaud
        device.serial.bytesize = bytesize
        device.serial.parity = parity
        device.serial.timeout = 10
        device.mode = minimalmodbus.MODE_RTU

    else:
        if use_visa is True:
            rm = pyvisa.ResourceManager()
            port = f"TCPIP::{port}::INSTR"
            if "COM" in port:
                com_id = port[3:]
                port = f"ASRL{com_id}::INSTR"
            device = rm.open_resource(port)
        else:
            device = serial.Serial(
                port=port,
                baudrate=PortBaud,
                bytesize=bytesize,
                parity=parity,
                stopbits=1,
                timeout=5,
            )

    return device


def serial_close(port):
    port.close()


def serial_flushinput(port):
    N = 2  # number of times to flush the buffer
    for _ in range(N):
        port.flushInput()
        port.flushOutput()
    return


def serial_read(
    port: Union[serial_open, pyvisa.ResourceManager.open_resource],
    use_visa: bool = True,
):
    """Read data from instrument.

    Args:
        port (Union[serial_open, pyvisa.ResourceManager.open_resource]): connection to instrument
        use_visa (bool, optional): use the pyvisa module. Defaults to True.

    Returns:
        _type_: data returned from instrument
    """
    # SerialPort_FlushInput(port)
    resp = None

    try:
        if use_visa is True:
            resp = port.read().rstrip()
            # print(resp)
        else:
            resp = port.readline().decode("utf-8")
    except Exception as e:
        *_, exc_tb = sys.exc_info()
        logging.warning(f"\t{e} -> Line {exc_tb.tb_lineno}")
    # print(resp)
    return resp


def serial_write(
    port: Union[serial_open, pyvisa.ResourceManager.open_resource],
    text: str,
    use_visa: bool = True,
):
    """write data packet to instrument

    Args:
        port (Union[serial_open, pyvisa.ResourceManager.open_resource]): connection to instrument
        text (str): data packet to send to instrument
        use_visa (bool, optional): use the pyvisa module. Defaults to True.
    """
    # SerialPort_FlushInput(port)
    # print("{} - {}".format(port.port, text))
    # print(text)
    logging.info(text)
    if use_visa is True:
        # print(text)
        port.write(text.rstrip())
    else:
        port.write(text.encode())
    time.sleep(0.125)


def serial_write_read(
    port: Union[serial_open, pyvisa.ResourceManager.open_resource],
    text: str,
    use_visa: bool = True,
):
    """_summary_

    Args:
        port (Union[serial_open, pyvisa.ResourceManager.open_resource]): _description_
        text (str): _description_
        use_visa (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
    """
    serial_write(port, text, use_visa=use_visa)
    return serial_read(port, use_visa=use_visa)


def close_out(*args):
    try:
        for dev in args:
            try:
                serial_close(dev)
            except Exception:
                logging.warning("dev not open")
    except Exception:
        logging.warning("Something really bad just happened")
    finally:
        sys.exit()


def socket_open(ip_address: str, port: int) -> socket.socket:
    """open socket connection to instrument.

    Args:
        ip_address (str): static ip address of instrument
        port (int): port for socket connection

    Returns:
        socket.socket: open connection.
    """
    device = socket.socket()
    device.connect((ip_address, port))
    device.settimeout(5)
    return device


def socket_write(device: socket.socket, packet: str) -> None:
    """write data packet over socket connection to instrument

    Args:
        device (socket.socket): open socket connection to instrument
        packet (str): data packet to send to instrument
    """
    logging.debug(packet)
    device.send(f"{packet}\n".encode())
    time.sleep(0.125)


def socket_read(device: socket.socket) -> str:
    """read data from instrument over socket connection

    Args:
        device (socket.socket): open socket connection to instrument

    Returns:
        str: data returned from instrument.
    """
    return device.recv(2048).decode("utf-8")
