import time
import logging

from system import serial_protocols
from system import stage_configuration


from network import validate_asset_calibration


def set_power_supply_state(
    supply_port: serial_protocols.serial_open,
    state: str,
    pwr_pos: int = 12,
    pwr_neg: int = 0,
    current_pos: float = 0.8,
    current_neg: float = 0.8,
) -> None:
    """_summary_

    Args:
        supply_port (serial_protocols.serial_open): _description_
        state (str): _description_
        pwr_pos (int, optional): _description_. Defaults to 12.
        pwr_neg (int, optional): _description_. Defaults to 0.
        current_pos (float, optional): _description_. Defaults to 0.8.
        current_neg (float, optional): _description_. Defaults to 0.8.
    """

    print(f"Turning Power Supply {state}")

    if state.upper() == "ON":
        check_supply_calibration_date(supply_port)

        set_voltage_output(
            supply_port, 1, abs(pwr_pos), stage_configuration.POWER_SUPPLY
        )
        set_voltage_output(
            supply_port, 2, abs(pwr_neg), stage_configuration.POWER_SUPPLY
        )
        set_current_limit(
            supply_port, 1, abs(current_pos), stage_configuration.POWER_SUPPLY
        )
        set_current_limit(
            supply_port, 2, abs(current_neg), stage_configuration.POWER_SUPPLY
        )
        set_output_state(1, supply_port, stage_configuration.POWER_SUPPLY)
    else:
        set_output_state(0, supply_port, stage_configuration.POWER_SUPPLY)

    return


def check_supply_calibration_date(supply_port: serial_protocols.serial_open) -> bool:
    """_summary_

    Args:
        supply_port (serial_protocols.serial_open): _description_

    Returns:
        bool: _description_
    """

    serial_protocols.serial_write(supply_port, "*IDN?\r\n")
    time.sleep(1.5)
    IDN_STR = serial_protocols.serial_read(supply_port)
    return bool(validate_asset_calibration.check_asset_calibration_data(IDN_STR))


def set_voltage_output(
    supply_port: serial_protocols.serial_open, chan: int, val: float, dev_id: str
) -> None:
    """_summary_

    Args:
        supply_port (serial_protocols.serial_open): _description_
        chan (int): _description_
        val (float): _description_
        dev_id (str): _description_
    """

    if dev_id == "GW INSTEK":
        serial_protocols.serial_write(supply_port, f"VSET{chan}:{val}\r")
        serial_protocols.serial_write(supply_port, f"VSET{chan}?\r")
        val = serial_protocols.serial_read(supply_port)
        serial_protocols.serial_write(supply_port, f"VOUT{chan}?\r")
    elif dev_id == "KEYSEIGHT":
        serial_protocols.serial_write(supply_port, f"INST OUT{chan}\r")
        serial_protocols.serial_write(supply_port, f"VOLT {chan}\r")
    elif dev_id == "SORENSEN":  # SORENSEN, XPF 60-20DP, J00439813, 2.00-4.06
        serial_protocols.serial_write(supply_port, f"V{chan} {val}\r")
        serial_protocols.serial_write(supply_port, f"V{chan}?\r")
        _ = serial_protocols.serial_read(supply_port)
    else:
        logging.warning("supply_port not setup...")


def set_current_limit(
    supply_port: serial_protocols.serial_open, chan: int, val: float, dev_id: str
) -> None:
    """_summary_

    Args:
        supply_port (serial_protocols.serial_open): _description_
        chan (int): _description_
        val (float): _description_
        dev_id (str): _description_
    """

    if dev_id == "GW INSTEK":
        serial_protocols.serial_write(supply_port, f"ISET{chan}:{val}\r")
        serial_protocols.serial_write(supply_port, f"ISET{chan}?\r")
        val = serial_protocols.serial_read(supply_port)
        serial_protocols.serial_write(supply_port, f"IOUT{chan}?\r")
        out = serial_protocols.serial_read(supply_port)
        logging.info(out)
    elif dev_id == "KEYSEIGHT":
        serial_protocols.serial_write(supply_port, f"INST OUT{chan}\r")
        serial_protocols.serial_write(supply_port, f"CURR {chan}\r")
    elif dev_id == "SORENSEN":  # SORENSEN, XPF 60-20DP, J00439813, 2.00-4.06
        serial_protocols.serial_write(supply_port, f"I{chan} {val}\r")
        serial_protocols.serial_write(supply_port, f"I{chan}?\r")
        out = serial_protocols.serial_read(supply_port)
        logging.info(out)

    else:
        logging.warning("supply_port not setup...")


def set_output_state(
    status: int, supply_port: serial_protocols.serial_open, dev_id: str
) -> None:
    """_summary_

    Args:
        status (str): _description_
        supply_port (serial_protocols.serial_open): _description_
        dev_id (str): _description_
    """

    if dev_id == "GW INSTEK":
        serial_protocols.serial_write(supply_port, f"OUT{status}\r")
    elif dev_id == "KEYSEIGHT":
        if status == 1:
            status = "ON"
        elif status == 0:
            status = "OFF"
        else:
            return
        serial_protocols.serial_write(supply_port, f"OUTPUT {status}\r\n")
    elif dev_id == "SORENSEN":
        # output_status = 1 if status == 1 else 0
        serial_protocols.serial_write(supply_port, f"OP1 {status}")
        serial_protocols.serial_write(supply_port, f"OP2 {status}")
    else:
        logging.warning("supply_port not setup...")
