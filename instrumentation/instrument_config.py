from system import serial_protocols
from system import stage_configuration

from instrumentation import motor_initialization


class mock_port:
    def __init__(self, port):
        self.port = port

    def write(self, text):
        print(text)

    def readline(self):
        print("reading data")


def instrumentation_setup() -> dict:
    """setup and initialize all instruments

    Returns:
        dict: instruments serial port connections in a dict.
    """
    if stage_configuration.CONTROLLER_TYPE == "Automation1":
        stage_port = motor_initialization.automation1_configure_stage()
    else:
        stage_port = serial_protocols.serial_open(
            stage_configuration.STAGE_PORT,
            stage_configuration.STAGE_BAUD,
            use_visa=False,
        )
        stage_port.timeout = 30

    data_aq_port = serial_protocols.serial_open(
        stage_configuration.DAQ_PORT, stage_configuration.DAQ_BAUD
    )

    if stage_configuration.CHAMBER_AVAILABLE is True:
        chamber_port = serial_protocols.socket_open(
            stage_configuration.CHAMBER_TCP_ADDR, stage_configuration.CHAMBER_TCP_ADDR
        )
    else:
        chamber_port = None

    power_supply_port = serial_protocols.serial_open(
        stage_configuration.DPS_PORT, stage_configuration.DPS_BAUD
    )

    return {
        "Stage": stage_port,
        "DataAq": data_aq_port,
        "Chamber": chamber_port,
        "Supply": power_supply_port,
    }


def instrumentation_close_connections(instruments: dict) -> None:
    """close connections to all instruments

    Args:
        instruments (dict): _description_
    """
    if stage_configuration.CONTROLLER_TYPE == "Automation1":
        motor_initialization.automation1_close_connection(instruments["Stage"])
    else:
        instruments["Stage"].close()

    instruments["DataAq"].close()
    instruments["Supply"].close()
    if stage_configuration.CHAMBER_AVAILABLE:
        instruments["Chamber"].close()

    return
