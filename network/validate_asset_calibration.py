import datetime

from network import api_calls

from system import stage_configuration


def check_asset_calibration_data(string: str) -> bool:
    # sourcery skip: use-datetime-now-not-today

    print(string)
    if "KEITHLEY" in string:
        # EXAMPLE: KEITHLEY INSTRUMENTS INC.,MODEL 2700,4389666,B10  /A02
        serial_no = string.split(",")[2]
        manufacturer = "KEITHLEY"
    elif "SORENSEN" in string:
        # EXAMPLE: SORENSEN, XPF 60-20DP, J00439813, 2.00-4.06
        serial_no = string.split(",")[2].replace(" ", "")
        manufacturer = "SORENSEN"
    elif string != "":
        # check if this is a MUX card.
        # EXAMPLE: 4592359
        serial_no = string
        manufacturer = "KEITHLEY"
    else:
        print("\033[91mInstrument not recognized.\033[00m")
        return 0

    asset_found = False

    assets = api_calls.get_assets_by_location(stage_configuration.__STAGE_NAME__)

    for record in assets:
        if manufacturer == "KEYSIGHT":
            serial_match = True
        else:
            serial_match = record["serial_number"] == serial_no
        manufacturer_match = record["manufacturer"] == manufacturer

        if serial_match and manufacturer_match:
            asset_found = True
            break

    if asset_found is True:
        asset_due_date = datetime.datetime.strptime(record["due_date"], "%Y-%m-%d")

        todays_date = datetime.datetime.today()

        if todays_date > asset_due_date:
            print(
                f"\033[91mAsset {record['asset_number']} is not calibrated. Asset was due {record['due_date']}.\033[00m"
            )
            return False
        else:
            print(
                f"\033[92mAsset {record['asset_number']} is calibrated. Not due till {record['due_date']}.\033[00m"
            )
            return True
    else:
        print("\033[91mAsset not found.\033[00m")
        return False
