import os
import logging
import json

from system import settings


def init_directory(filepath: str) -> None:
    """create a new folder if one does not already exist.

    Args:
        filepath (str): path to folder to create.
    """
    if not os.path.isdir(filepath):
        logging.info("Directory is not set up... setting up now...")
        os.makedirs(filepath, exist_ok=False)


def get_test_setup_json_data() -> dict:
    """open the json test setup data file and load the data into a dict.

    Returns:
        dict: json data for the test setup
    """
    filename = os.environ.get("WO_FILEPATH")
    with open(filename, "r") as file:
        json_data = json.load(file)
    return json_data


def load_json_data_to_file(work_order: str, data: dict) -> None:
    """open the json file and write data into it.

    Args:
        work_order (str): work order used in the file name to keep things unique
        data (dict): json data.
    """
    filepath = os.path.join(
        settings.HOME_PATH,
        settings.HOST_NAME,
        work_order,
    )
    init_directory(filepath)

    filename = os.path.join(filepath, f"{work_order}.json")

    os.environ["WO_FILEPATH"] = filename

    with open(filename, "w") as file:
        json.dump(data, file)


def build_test_data_file(unit_id_dict: dict, port: str) -> str:
    """_summary_

    Args:
        unit_id_dict (dict): _description_
        port (str): _description_

    Returns:
        str: _description_
    """
    filepath = os.environ.get("SO_FILEPATH")
    serial_no = unit_id_dict[port]["serial_no"]
    part_no = unit_id_dict[port]["part_no"]
    return os.path.join(
        filepath,
        f"part_no_{part_no}_serialno_{serial_no}.csv",
    )


def get_test_data_from_file(
    unit_id_dict: str, port: str, axis: str, test: str
) -> tuple[list, list]:  # type: ignore
    """_summary_

    Args:
        unit_id_dict (_type_): _description_
        list (_type_): _description_

    Returns:
        _type_: _description_
    """
    file = build_test_data_file(unit_id_dict, port)
    with open(file, "r") as read_file:
        data = read_file.readlines()

    output_data = []
    input_data = []
    for line in data:
        if test in line:
            record = line.split(",")
            if axis == "X":
                output_data.append(float(record[7]))
            elif axis == "Y":
                output_data.append(float(record[8]))
            elif axis == "Z":
                output_data.append(float(record[9]))

            input_data.append(float(record[6]))
    return output_data, input_data
