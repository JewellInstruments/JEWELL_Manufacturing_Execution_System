from network import api_calls
from network import get_specs
from network import filesystem

from analytics import linear_algebra
from analytics import numerical_methods

from system import stage_configuration


def write_tumble_data_to_api(data_1: dict, data_2: dict, unit_id_dict: dict) -> None:
    """write tumble cal data to api

    Args:
        data_1 (dict): _description_
        data_2 (dict): _description_
        unit_id_dict (dict): _description_
    """

    for key in data_1.keys():
        unit_id = unit_id_dict[key]["unit_id"]

        x_output = data_1[key][0]
        y_output = data_1[key][1]
        z_output = data_1[key][2]
        api_calls.write_jdx_tumble_calibration_data(
            unit_id,
            1,
            x_output,
            y_output,
            z_output,
        )

        x_output = data_2[key][0]
        y_output = data_2[key][1]
        z_output = data_2[key][2]
        api_calls.write_jdx_tumble_calibration_data(
            unit_id,
            -1,
            x_output,
            y_output,
            z_output,
        )
    return


def publish_calibration_data(specs: get_specs.mems_specs, unit_id_dict: dict) -> None:

    for port in unit_id_dict:
        file = filesystem.build_test_data_file(unit_id_dict, port)
        with open(file, "r") as read_file:
            data = read_file.readlines()

        for axis_index in range(specs.axes_no):

            axis = stage_configuration.AXES_DECODER[str(axis_index)]

            # going to need to handel jdx calibration data differently.

            for cycle in range(len(specs.cycles)):

                for temp_index in range(len(specs.cal_temps)):

                    x_output_data = []
                    y_output_data = []
                    z_output_data = []
                    unit_temp_data = []
                    plate_temp_data = []
                    input_data = []
                    cycle_index_data = []
                    temp_index_data = []
                    # output_up = []

                    z_transverse_axis_set = False
                    y_transverse_axis_set = False

                    for line in data:  # search all records in the data file.
                        if (
                            "Linearity" in line
                        ):  # only get the record in the file where the test was linearity.

                            record = line.split(",")
                            if (
                                int(record[3]) == axis_index and int(record[4]) == cycle
                            ):  # only get the linearity data for the axis under study.
                                cycle_index_data.append(record[4])
                                temp_index_data.append(record[5])
                                input_data.append(float(record[6]))
                                x_output_data.append(float(record[7]))
                                y_output_data.append(float(record[8]))
                                z_output_data.append(float(record[9]))
                                unit_temp_data.append(float(record[10]))
                                plate_temp_data.append(float(record[11]))

                        elif (
                            "Z-Transverse Axis Misalignment" in line
                        ):  # only get the record in the file where the test was Z-Transverse Axis Misalignment
                            record = line.split(",")
                            if int(record[4]) == cycle:
                                # print(record)
                                if axis_index == 0:
                                    value = float(record[7])
                                elif axis_index == 1:
                                    value = float(record[8])
                                else:
                                    value = float(record[9])

                                # print(value)
                                if z_transverse_axis_set is True:
                                    # print(value)
                                    output_down = value
                                else:
                                    output_up = value
                                z_transverse_axis_set = True
                        elif (
                            "Y-Transverse Axis Misalignment" in line
                        ):  # only get the record in the file where the test was Z-Transverse Axis Misalignment
                            record = line.split(",")
                            if int(record[4]) == cycle:
                                # print(record)
                                if axis_index == 0:
                                    value = float(record[8])
                                elif axis_index == 1:
                                    value = float(record[7])
                                else:
                                    value = float(record[7])
                                # print(value)

                                if y_transverse_axis_set is True:
                                    # print(value)
                                    pendulous_right = value
                                else:
                                    pendulous_left = value
                                y_transverse_axis_set = True

                    for row in range(len(input_data)):

                        api_calls.write_linearity_calibration_data(
                            unit_id_dict[port]["unit_id"],
                            axis,
                            temp_index,
                            cycle,
                            input_data[row],
                            plate_temp_data[row],
                            x_output_data[row],
                            y_output_data[row],
                            z_output_data[row],
                            unit_temp_data[row],
                        )

                    # may also want to keep this data for each cycle and temp.
                    api_calls.write_static_calibration_data(
                        unit_id_dict[port]["unit_id"],
                        axis,
                        output_up,
                        output_down,
                        pendulous_left,
                        pendulous_right,
                        0,
                        1,
                    )

                    if axis == "X":
                        output_data = x_output_data
                    elif axis == "Y":
                        output_data = y_output_data
                    else:
                        output_data = z_output_data

                    coefficients, sigma, r2 = linear_algebra.solve_least_squares(
                        input_data, output_data, 1
                    )

                    bias = numerical_methods.compute_bias(
                        output_up, output_down, coefficients[1]
                    )

                    Mza = numerical_methods.compute_output_axis(
                        output_up, output_down, coefficients[1]
                    )

                    Mya = numerical_methods.compute_pendulous_axis_misalignment(
                        pendulous_left, pendulous_right, coefficients[1]
                    )

                    api_calls.write_calibration_metrics(
                        unit_id_dict[port]["unit_id"],
                        axis,
                        cycle_index=cycle,
                        temp_index=temp_index,
                        scale_factor=coefficients[1],
                        moa=Mza,
                        mpa=Mya,
                        bias=bias,
                    )

    return
