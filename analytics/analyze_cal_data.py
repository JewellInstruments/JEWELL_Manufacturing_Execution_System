from analytics import linear_algebra
from analytics import numerical_methods

from network import get_calibration_data
from network import get_specs
from network import filesystem


from system import stage_configuration
from system import settings


def analyze_jmx_calibration_data(
    specs: get_specs.mems_specs, unit_id_dict: dict
) -> None:
    """_summary_

    Args:
        specs (get_specs.mems_specs): _description_
        unit_id_dict (dict): _description_
    """

    # numerical_methods.compute_full_scale_output()

    for port in unit_id_dict:
        serial_no = unit_id_dict[port]["serial_no"]
        print(f"\nAnalyzing calibration/verification data for {serial_no}")

        file = filesystem.build_test_data_file(unit_id_dict, port)
        with open(file, "r") as read_file:
            file_data = read_file.readlines()

        for axis_index in range(specs.axes_no):

            axis = stage_configuration.AXES_DECODER[str(axis_index)]

            for cycle in range(len(specs.cycles)):

                for temp_index in range(len(specs.cal_temps)):

                    print(settings.TERMINAL_SPACER)
                    print(
                        f"Studying the {axis} axis, cycle {specs.cycles[cycle]} for temp {specs.cal_temps[temp_index]}"
                    )

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

                    for line in file_data:  # search all records in the data file.
                        if (
                            "Linearity" in line
                        ):  # only get the record in the file where the test was linearity.

                            record = line.split(",")
                            if (
                                int(record[3]) == axis_index
                                and int(record[4]) == cycle
                                and int(record[5]) == temp_index
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
                            if int(record[4]) == cycle and int(record[5]) == temp_index:
                                if int(record[3]) == axis_index:
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
                            if int(record[4]) == cycle and int(record[5]) == temp_index:
                                # print(record)
                                if int(record[3]) == axis_index:
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

                    if axis == "X":
                        output_data = x_output_data
                    elif axis == "Y":
                        output_data = y_output_data
                    else:
                        output_data = z_output_data

                    coefficients, sigma, r2 = linear_algebra.solve_least_squares(
                        input_data, output_data, 1
                    )

                    if (
                        coefficients[1] < specs.scale_factor_low_limit
                        or coefficients[1] > specs.scale_factor_high_limit
                    ):
                        state_color = settings.red_text
                    else:
                        state_color = settings.green_text

                    print(
                        f"Scale factor ({specs.output_units}/g): {state_color}{coefficients[1]:.6f}{settings.white_text}"
                    )

                    max_nonlieanrity = numerical_methods.nonlinearity(
                        input_data, output_data, coefficients
                    )
                    if abs(max_nonlieanrity) > specs.linearity[axis_index]:
                        state_color = settings.red_text
                    else:
                        state_color = settings.green_text

                    print(
                        f"Linearity (% FRO): {state_color}{max_nonlieanrity:.2f}{settings.white_text}"
                    )

                    bias = numerical_methods.compute_bias(
                        output_up, output_down, coefficients[1]
                    )
                    if abs(bias) > specs.bias:
                        state_color = settings.red_text
                    else:
                        state_color = settings.green_text

                    print(f"Bias (g): {state_color}{bias:.6f}{settings.white_text}")

                    Mza = numerical_methods.compute_output_axis(
                        output_up, output_down, coefficients[1]
                    )
                    if abs(Mza) > specs.moa:
                        state_color = settings.red_text
                    else:
                        state_color = settings.green_text

                    print(
                        f"Z-Transverse Axis Misalignment (deg): {state_color}{Mza:.2f}{settings.white_text}"
                    )

                    Mya = numerical_methods.compute_pendulous_axis_misalignment(
                        pendulous_left, pendulous_right, coefficients[1]
                    )

                    if abs(Mya) > specs.mpa:
                        state_color = settings.red_text
                    else:
                        state_color = settings.green_text

                    print(
                        f"Y-Transverse Axis Misalignment (deg): {state_color}{Mya:.2f}{settings.white_text}"
                    )
                    print(settings.TERMINAL_SPACER)

    return


def analyze_jdx_calibration_data(
    specs: get_specs.mems_specs, unit_id_dict: dict, test: str = "Temperature"
) -> None:
    """Analyze digital MEMs calibration data per ES 9411

    Args:
        specs (_type_): _description_
        unit_id_array (_type_): _description_
    """

    for port in unit_id_dict:
        serial_no = unit_id_dict[port]["serial_no"]
        part_no = unit_id_dict[port]["part_no"]
        # unit_id = unit_id_dict[port]["unit_id"]
        print(f"\nAnalyzing calibration/verification data for {serial_no}")

        cycle_idx = 2  # only look at the verification data.

        for axis_idx in range(specs.axes_no + 1):
            axis_test_data = []

            if test == "Temperature":
                for temp_idx in range(len(specs.verify_temps)):
                    data = get_calibration_data.get_calibration_data(
                        part_no, serial_no, axis_idx, cycle_idx, temp_idx
                    )

                    axis_test_data.append(data)
            else:
                temp_idx = 2
                data = get_calibration_data.get_calibration_data(
                    part_no, serial_no, axis_idx, cycle_idx, temp_idx
                )

                axis_test_data.append(data)

            # numerical_methods.calculate_bias_over_temp(axis_test_data, specs, axis_idx)

            if test == "Temperature":
                numerical_methods.calculate_accuracy(axis_test_data, specs, axis_idx)
            else:
                print("Testing residuals")
                numerical_methods.calculate_verification_accuracy(
                    axis_test_data, specs, axis_idx
                )

            numerical_methods.calculate_linearity(axis_test_data, specs, axis_idx)
            numerical_methods.calculate_cross_axis_error(
                axis_test_data, specs, axis_idx
            )

    return


def analyze_jdx_tumble_data(
    specs: get_specs.mems_specs,
    unit_id_dict: dict,
    tumble_matrix_plus: dict,
    tumble_matrix_minus: dict,
) -> tuple[dict, dict]:
    """analyze the jdx orthonormalization data and generate the matrices for each sensor as per ES 9409.

    Args:
        specs (get_specs.mems_specs): product definition
        unit_id_dict (dict): units mapped to which port they are on

    Returns:
        tuple[dict, dict]: returns the orthonormalization (3x3) and offset matrices (3x1)
    """  # noqa: E501

    orthonormal_matrix = {}
    offset_matrix = {}
    for key in unit_id_dict:
        w = linear_algebra.subtract_matrix(
            tumble_matrix_plus[key], tumble_matrix_minus[key]
        )
        w_inverse = linear_algebra.invert_matrix(w)
        orthonormal_matrix[key] = linear_algebra.scale_matrix(
            w_inverse, 2.0 * specs.nominal_ADC
        )

        w = linear_algebra.add_matrix(tumble_matrix_plus[key], tumble_matrix_minus[key])
        offset_matrix[key] = [1.0 / 3.0 * w[i][i] for i in range(3)]

        print(f"Orthonormalization matrix for {key} is...")
        linear_algebra.display_matrix(orthonormal_matrix[key], specs)

        print(f"Offset matrix for {key} is...")
        print(offset_matrix[key])

    return orthonormal_matrix, offset_matrix
