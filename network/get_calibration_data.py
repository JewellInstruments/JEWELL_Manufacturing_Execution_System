import os


def get_calibration_data(
    part_no: str, serial_no: str, axis_index: int, cycle_index: int, temp_index: int
) -> tuple[dict, list]:
    """pull calibration data for a unit_id.

    Args:
        unit_id (int): _description_
        axis_index (int): _description_
        cycle_index (int): _description_
        temp_index (int): _description_

    Returns:
        tuple[dict, list]: _description_
    """
    filepath = os.environ.get("SO_FILEPATH")
    file = os.path.join(
        filepath,
        f"part_no_{part_no}_serialno_{serial_no}.csv",
    )

    # Datetime	Stage	Test	Axis Index	Cycle Index	Temp Index	Input (deg)	X Output (deg)	Y Output (deg)	Z Output (deg)	Unit Temp (C)	Plate Temp (C)

    # print(axis_index)
    # print(cycle_index)
    # print(temp_index)
    with open(file, "r") as read_file:
        data = read_file.readlines()

    calibration_data = []
    for line in data[1:]:
        record = line.rstrip().split(",")
        # print(record)

        if int(record[3]) == axis_index:
            if int(record[4]) == cycle_index:
                if int(record[5]) == temp_index:
                    # A, X, Y, Z, UT, PT,
                    calibration_data.append(
                        [
                            float(record[6]),
                            float(record[7]),
                            float(record[8]),
                            float(record[9]),
                            float(record[10]),
                            float(record[11]),
                        ]
                    )

    return calibration_data


def get_tumble_data(unit_id: int) -> tuple[dict, list]:
    """retrieve data from the api.

    Args:
        unit_id (int): _description_

    Returns:
        tuple[dict, list]: _description_
    """

    return {}, []
