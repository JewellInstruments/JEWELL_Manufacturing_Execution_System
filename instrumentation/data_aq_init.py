import logging

from system import stage_configuration
import system.serial_protocols as serial_protocols

from network import validate_asset_calibration

# ask the Data Aq system for its IDN string. use the make, model, serial number
# to search in the calibration database for the asset number and calibration date.
# returns 1 if meter is calibration. returns 0 if not.


def check_data_aq_in_calibration(port: serial_protocols.serial_open) -> bool:
    """_summary_

    Args:
        port (serial_protocols.serial_open): _description_

    Returns:
        bool: _description_
    """

    serial_protocols.serial_write(port, "*IDN?\r")  # get the idn query.
    data = serial_protocols.serial_read(port)

    return validate_asset_calibration.check_asset_calibration_data(data)


def check_daq_card_in_calibration(port: serial_protocols.serial_open) -> bool:
    """_summary_

    Args:
        port (serial_protocols.serial_open): _description_

    Returns:
        bool: _description_
    """

    card_serial_numbers = {}

    for card in range(1, stage_configuration.NUMBER_OF_CARDS + 1):
        serial_protocols.serial_write(port, f"SYST:CARD{card}:SNUM?\r")
        data = serial_protocols.serial_read(port)
        card_serial_numbers[f"card{card}"] = data.rstrip()
        validate_asset_calibration.check_asset_calibration_data(data)

    return True


def config_data_aq_for_temp(
    port: serial_protocols.serial_open,
    full_setup: bool = False,
    thermistor: bool = True,
) -> bool:
    """_summary_

    Args:
        port (serial_protocols.serial_open): _description_
        full_setup (bool, optional): _description_. Defaults to False.
        thermistor (bool, optional): _description_. Defaults to True.

    Returns:
        bool: _description_
    """

    try:
        print("Configuring the data aquisition system for thermometry")

        if stage_configuration.DAQ_IDN == "HEWLETT-PACKARD":
            pass
        elif stage_configuration.DAQ_IDN == "KEITHLEY":
            if full_setup:
                serial_protocols.serial_write(port, "*RST\r")  # reset the dev
                serial_protocols.serial_write(
                    port, "SYST:BEEP 0\r"
                )  # clear the error queue
                # decrease integration speed
                serial_protocols.serial_write(port, ":SENS:VOLT:DC:NPLC 0.05\r")
                serial_protocols.serial_write(
                    port, "SYST:CLE\r"
                )  # clear the error queue
                serial_protocols.serial_write(port, ":FORM:ELEM READ,CHAN\r")
                serial_protocols.serial_write(
                    port, ":ROUT:OPEN:ALL\r"
                )  # open all Routes
                # set continuous trigger to off
                serial_protocols.serial_write(port, "INIT:CONT OFF\r")
                serial_protocols.serial_write(port, "TRIG:SOUR IMM\r")  # set the source

            serial_protocols.serial_write(
                port, f"FUNC 'TEMP', (@{stage_configuration.TEMP_CHAN})\r"
            )
            serial_protocols.serial_write(
                port, f"UNIT:TEMP {stage_configuration.TEMP_UNITS}\r"
            )
            serial_protocols.serial_write(
                port, "TEMP:TC:ODET ON\r"
            )  # set the temp probe type
            if not thermistor:
                serial_protocols.serial_write(
                    port,
                    f"TEMP:TC:TYPE {stage_configuration.TEMP_PROBE}, (@{stage_configuration.TEMP_CHAN})\r",
                )
                serial_protocols.serial_write(
                    port, f"TEMP:RJUN:RSEL SIM, (@{stage_configuration.TEMP_CHAN})\r"
                )
                serial_protocols.serial_write(
                    port,
                    f"TEMP:RJUN:SIM {stage_configuration.TEMP_CJC}, (@{stage_configuration.TEMP_CHAN})\r",
                )
            serial_protocols.serial_write(port, ":INITiate:CONTinuous OFF\r")

            if full_setup:
                serial_protocols.serial_write(
                    port, "TRIG:COUN 1\r"
                )  # set trigger count to 1
                serial_protocols.serial_write(
                    port, f":SAMP:COUN {stage_configuration.NUM_TEMP_CHANS}\r"
                )
                serial_protocols.serial_write(
                    port, f":ROUT:SCAN (@{stage_configuration.TEMP_CHAN})\r"
                )
                # use this to toggle the display
                serial_protocols.serial_write(port, "DISPLAY:ENABLE 1\r")
                serial_protocols.serial_write(port, ":TRAC:CLE\r")  # clear the buffer

                return bool(check_data_aq_in_calibration(port))
        else:
            logging.warning("port not setup...")
    except Exception as e:
        print(e)


def select_channels(
    mode: str = None, channels: int = 0, differential: bool = False
) -> list:
    """_summary_

    Args:
        mode (str, optional): _description_. Defaults to None.
        channels (list, optional): _description_. Defaults to [].
        differential (bool, optional): _description_. Defaults to False.

    Returns:
        list: _description_
    """
    if mode == "Current":
        return
    chans_to_scan = []
    # keys = list(settings.DIFF_PORT_CONFIG.keys())
    if not differential:
        print("Selecting the card for single-ended use.")
        for port in range(channels):
            for channel in range(len(stage_configuration.DIFF_PORT_CONFIG["PORT_1"])):
                chans_to_scan.append(
                    stage_configuration.DIFF_PORT_CONFIG[f"PORT_{port+1}"][channel]
                )
    elif channels != 0:
        # i = 0
        # chans_to_scan.extend(iter(list(stage_configuration.DIFF_PORT_CONFIG[keys[i]])))
        # chans_to_scan.extend(iter(list(stage_configuration.SINGLE_PORT_CONFIG[keys[i]])))
        for port in range(channels):
            for channel in range(range(stage_configuration.DIFF_PORT_CONFIG["PORT_1"])):
                chans_to_scan.append(
                    stage_configuration.DIFF_PORT_CONFIG[f"PORT_{port+1}"][channel]
                )
                chans_to_scan.append(
                    stage_configuration.SINGLE_PORT_CONFIG[f"PORT_{port+1}"][channel]
                )
    else:
        print("Something bad just happened.")

    chans_to_scan.sort()

    return chans_to_scan


def config_data_aq_for_voltage(
    port: serial_protocols.serial_open,
    mode: str = "",
    channels: int = 0,
    differential: bool = False,
    ac_dc: str = "DC",
) -> bool:
    """_summary_

    Args:
        port (serial_protocols.serial_open): _description_
        mode (str, optional): _description_. Defaults to "".
        channels (list, optional): _description_. Defaults to [].
        differential (bool, optional): _description_. Defaults to False.

    Returns:
        bool: _description_
    """
    print("\nConfiguring Data Acquisition System...Please wait.")

    logging.debug("Configuring Data Acquisition System...")

    channels_to_scan = select_channels(
        mode=mode, channels=channels, differential=differential
    )

    if stage_configuration.DAQ_IDN == "KEITHLEY":
        return issue_commands_to_data_aq(port, mode, channels_to_scan, ac_dc)
    elif stage_configuration.DAQ_IDN != "HEWLETT-PACKARD":
        logging.warning("port not setup...")
        return False


def issue_commands_to_data_aq(
    port: serial_protocols.serial_open, mode: str, channels: list, ac_dc: str
) -> bool:
    """_summary_

    Args:
        port (serial_protocols.serial_open): _description_
        mode (str): _description_
        channels (list): _description_

    Returns:
        bool: _description_
    """
    # sourcery skip: use-fstring-for-formatting

    serial_protocols.serial_write(port, "*RST\r")  # reset the dev
    serial_protocols.serial_write(port, "SYST:BEEP 0\r")  # clear the error queue
    # decrease integration speed
    serial_protocols.serial_write(port, ":SENS:VOLT:DC:NPLC 0.05\r")
    serial_protocols.serial_write(port, ":SENS:VOLT:DC:RANG 1000 \r")
    serial_protocols.serial_write(port, "SYST:CLE\r")  # clear the error queue
    # setup the output (reading, channel)
    serial_protocols.serial_write(port, ":FORM:ELEM READ,CHAN\r")
    serial_protocols.serial_write(port, ":ROUT:OPEN:ALL\r")  # open all Routes
    # set continous trigger to off
    serial_protocols.serial_write(port, "INIT:CONT OFF\r")
    serial_protocols.serial_write(port, "TRIG:SOUR IMM\r")  # set the source
    # set the buffer to 55000 points, fixes the -363 error on port
    serial_protocols.serial_write(port, "TRAC:POIN 55000\r")
    if ac_dc == "DC":
        serial_protocols.serial_write(port, f"FUNC 'VOLT', (@{','.join(channels)})\r")
    else:
        serial_protocols.serial_write(
            port, f"FUNC 'VOLT:AC', (@{','.join(channels)})\r"
        )
    serial_protocols.serial_write(
        port, f":SENS:VOLT:RANG 10, (@{','.join(channels)})\r"
    )

    # channels.extend(
    #     (stage_configuration.TEMP_CHAN_AIR, stage_configuration.TEMP_CHAN_PLATE)
    # )
    N_scan_chans = len(channels)
    # config_data_aq_for_temp(port, full_setup=False)
    if mode == "Current":
        config_dataq_for_thermistor(port, channels)
    serial_protocols.serial_write(port, "TRIG:COUN 1\r")  # set trigger count to 1
    serial_protocols.serial_write(port, f":SAMP:COUN {N_scan_chans}\r")
    serial_protocols.serial_write(port, ":ROUT:SCAN (@{})\r".format(",".join(channels)))
    # use this to toggle the display
    serial_protocols.serial_write(port, "DISPLAY:ENABLE 1\r")
    # set the buffer to autoclear
    serial_protocols.serial_write(port, ":TRAC:CLE\r")

    print("\nDone configuring Data Acquisition System.")
    print("\nChecking the calibration of the Data Acquisition System")

    calibrated_bool = check_data_aq_in_calibration(
        port
    ) and check_daq_card_in_calibration(
        port
    )  # noqa: E501

    return bool(calibrated_bool)


def config_dataq_for_thermistor(port, channels):
    """_summary_

    Args:
        port (_type_): _description_
        channels (_type_): _description_

    Returns:
        _type_: _description_
    """
    return 1
