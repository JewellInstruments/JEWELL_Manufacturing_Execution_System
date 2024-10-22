# from requests.compat import urljoin
# import requests

# specs_url = urljoin("http://qed8:8000/api/", "mems_linear_specs")
# specs = requests.get(specs_url, params={"part_no": "03550728-5371"})

import math


def compute_pendulous_axis_misalignment(
    data_90_neg: float, data_90_pos: float, scale_factor: float
) -> float:
    """This function computes the pendulous axis misalignment.

    Args:
        data_90_neg (float): output data from sensor while at -90 degrees
        data_90_pos (float): output data from sensor while at 90 degrees

    Returns:
        float: pendulous axis misalignment in degrees.
    """

    return math.degrees(
        math.asin((data_90_pos - data_90_neg) / (2.0 * 9.81 * scale_factor))
    )


data = compute_pendulous_axis_misalignment(-0.000487, -0.004088, 5.005006274)

print(data)

# for row in specs.json():
#     if row["part_no"] == "03550728-5371":
#         print(row)

# linearity_table = "mems_linear_thermal_data/"
# linearity_url = urljoin("http://qed8:8000/api/", linearity_table)

# data = {
#     "unit_id": 9999,
#     "axis_index": 1,
#     "temp_index": 1,
#     "cycle_index": 1,
#     "reference": 1,
#     "plate_temp": 1,
#     "x_output": 1,
#     "y_output": 1,
#     "z_output": 1,
#     "unit_temp": 1,
# }
# response = requests.post(linearity_url, data=data)
# print(response)
# print(response.json())


# DIFF_PORT_CONFIG = {
#     "PORT_1": ["101", "102", "103"],
#     "PORT_2": ["104", "105", "106"],
#     "PORT_3": ["107", "108", "109"],
#     "PORT_4": ["110", "111", "112"],
#     "PORT_5": ["113", "114", "115"],
#     "PORT_6": ["116", "117", "118"],
# }

# SINGLE_PORT_CONFIG = {
#     "PORT_1": ["201", "202", "203"],
#     "PORT_2": ["204", "205", "206"],
#     "PORT_3": ["207", "208", "209"],
#     "PORT_4": ["210", "211", "212"],
#     "PORT_5": ["213", "214", "215"],
#     "PORT_6": ["216", "217", "218"],
# }
# channels = 2
# chans_to_scan = []
# for port in range(channels):
#     for channel in range(len(DIFF_PORT_CONFIG["PORT_1"])):
#         chans_to_scan.append(DIFF_PORT_CONFIG[f"PORT_{port+1}"][channel])
# print(chans_to_scan)
