import sys
import math
import logging

from system import stage_configuration

from network import get_specs

from analytics import linear_algebra
from analytics import statistical_methods


def compute_full_scale_output(data_max: float, data_min: float) -> float:
    """compute the full scale output of a sensor.

    Args:
        data_max (float): _description_
        data_min (float): _description_

    Returns:
        float: _description_
    """

    return (data_max - data_min) / 2.0


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
        math.asin(
            (data_90_pos - data_90_neg)
            / (2.0 * stage_configuration.LOCAL_G_VALUE * scale_factor)
        )
    )


def compute_output_axis(data_0: float, data_180: float, scale_factor: float) -> float:
    """This function computes the output axis misalignment

    Args:
        data_0 (float): output data from sensor while at 0 degrees
        data_180 (float): output data from sensor while at 180 degrees.
        scale_factor (float): the scale factor of the UUT in V/g.

    Returns:
        float: output axis misalignment in volts
    """
    return math.degrees(
        math.asin(
            (data_0 - data_180)
            / (2.0 * stage_configuration.LOCAL_G_VALUE * scale_factor)
        )
    )


def compute_input_axis_misalignment(Moa: float, Mpa: float) -> float:
    """calculate the input axis misalignment of servo-forced balanced sensor.

    Args:
        Moa (float): Output axis misalignment in degrees
        Mpa (float): Pendulous axis misalignment in degrees

    Returns:
        float: input axis misalignment in degrees
    """

    return math.sqrt(Mpa**2 + Moa**2)


def compute_bias(data_0: float, data_180: float, scale_factor: float) -> float:
    """This function computes the bias

    Args:
        data_0 (float): output data from sensor while at 0 degrees.
        data_180 (float): output data from sensor while at 180 degrees.
        scale_factor (float): the scale factor of the UUT in V/g.

    Returns:
        float: bias in volts.
    """
    return (data_0 + data_180) / (2.0 * scale_factor)


def polynomial(data: list, coefficients: list) -> list:
    """build polynomial using coefficients which provide the c0,c1,c2..cn in a list respectively.

    Args:
        data (list): data to be used for the basis of the polynomial function
        coefficients (list): list of coefficients for the polynomial. y = c0 + cn*x**n for n in len(coefficients)

    Returns:
        list: output data from the polynomial using data as the basis and coefficients as the coefficients.
    """
    return [
        sum(coefficients[m] * data[i] ** m for m in range(len(coefficients)))
        for i in range(len(data))
    ]


def nonlinearity(x_data: list, y_data: list, coefficients: list) -> float:
    """calculate the maximum deviation from a best fit straight line.

    Args:
        x_data (list): x data to be used in the curve fitting process.
        y_data (list): y data to be used in the curve fitting process.
        coefficients (list): coefficients to be used for the polynomial.

    Returns:
        float: maximum deviation from the best fit straight line as a percent of the full range.
    """

    max_err = 0
    try:
        y_data_fit = polynomial(x_data, coefficients)
        err = []
        for i in range(len(x_data)):
            buf = abs(y_data_fit[i] - y_data[i])
            err.append(100 * buf / (max(y_data) - min(y_data)))
        max_err = max(err)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logging.warning(f"{e} -> Line {exc_tb.tb_lineno}")
    finally:
        return max_err


def validate_angle(angle: float) -> int:
    """validate the angle is not none"""
    return 1 if angle is not None else 0


def calculate_bias_over_temp(
    data: list, specs: get_specs.mems_specs, axis_index: int
) -> tuple[float, float]:
    """_summary_

    Args:
        data (list): _description_
        specs (get_specs.mems_specs): _description_
        axis_index (int): _description_

    Returns:
        tuple[float, float]: _description_
    """
    bts = 0.0
    average_plate_temp = []
    bias = []
    # loop over all the data for that axis.
    for arr in data:
        # initialize some lists for data
        plate_temp = []
        output = []
        angle = []

        zero_tilt = []

        # select the zero tilt based on which axis one is looking at.
        if axis_index == 0:
            zero_tilt.append(arr[len(arr) // 2][9])
        elif axis_index == 1:
            zero_tilt.append(arr[len(arr) // 2][10])
        elif axis_index == 2:
            zero_tilt.append(arr[len(arr) // 2][11])
        else:
            zero_tilt.append(arr[len(arr) // 2][12])

        # bulb up the data arrays by looping over each record.
        for record in arr:
            # print(record)
            plate_temp.append(record[8])
            angle.append(record[7])
            # select the correct output based on axis of interest.
            if axis_index == 0:
                output.append(record[9])
                bts_limit = specs.bts0
                bias_limit = specs.bias0
            elif axis_index == 1:
                output.append(record[10])
                bts_limit = specs.bts1
                bias_limit = specs.bias0
            elif axis_index == 2:
                output.append(record[11])
                bts_limit = specs.bts2
                bias_limit = specs.bias0
            else:
                output.append(record[9])

        # use the first order regression to get the bias (y intercept)
        soln, *_ = linear_algebra.solve_least_sqrs(angle, output, order=1)
        # print(soln)

        bias.append(soln[0])
        average_plate_temp.append(statistical_methods.mean(plate_temp))

    # perform a cubic regression using the plate temp and the bias.
    coefficients, *_ = linear_algebra.solve_least_squares(
        average_plate_temp, bias, order=3
    )

    # use the cubic regreesion model to solve for the bias at 25 C.
    bias_25C = polynomial([25], coefficients)

    bias_25C = bias_25C[0]

    # bias temperature sensitivity in units of ppm/C
    bts = 1e6 * (
        abs(
            (zero_tilt[0] - zero_tilt[-1])
            / (average_plate_temp[0] - average_plate_temp[-1])
        )
    )

    # display the results

    if abs(bias_25C) > bias_limit:
        print(
            "Bias at 25 C for the {} axis: \033[91m{:.4f}\033[00m (deg)".format(
                stage_configuration.AXES_DECODER[str(axis_index)], bias_25C
            )
        )
    else:
        print(
            "Bias at 25 C for the {} axis: \033[92m{:.4f}\033[00m (deg)".format(
                stage_configuration.AXES_DECODER[str(axis_index)], bias_25C
            )
        )

    if abs(bts) > bts_limit:
        print(
            "BTS for the {} axis: \033[91m{:.4f}\033[00m (ppm/C)".format(
                stage_configuration.AXES_DECODER[str(axis_index)], bts
            )
        )
    else:
        print(
            "BTS for the {} axis: \033[92m{:.4f}\033[00m (ppm/C)".format(
                stage_configuration.AXES_DECODER[str(axis_index)], bts
            )
        )

    return bias_25C, bts


def calculate_accuracy(
    data: list, specs: get_specs.mems_specs, axis_index: int
) -> float:
    """_summary_

    Args:
        data (list): _description_
        specs (get_specs.mems_specs): _description_
        axis_index (int): _description_

    Returns:
        float: _description_
    """
    bias_25C, bts = calculate_bias_over_temp(data, specs, axis_index)

    accuracy = []

    for arr in data:
        # initialize some lists for data
        output = 0.0
        angle = 0.0

        # buld up the data arrays by looping over each record.
        for record in arr:
            # print(record)
            angle = record[7]
            # select the correct output based on axis of interest.
            if axis_index == 0:
                output = record[9]
                accry_limit = specs.accy0
            elif axis_index == 1:
                output = record[10]
                accry_limit = specs.accy1
            elif axis_index == 2:
                output = record[11]
                accry_limit = specs.accy2
            else:
                output = record[9]

            accuracy.append(abs(angle - (output + bias_25C)))

    relative_accuracy = max(accuracy)

    if abs(relative_accuracy) > accry_limit:
        print(
            "Relative accuracy for the {} axis: \033[91m{:.4f}\033[00m (deg)".format(
                stage_configuration.AXES_DECODER[str(axis_index)], relative_accuracy
            )
        )
    else:
        print(
            "Relative accuracy for the {} axis: \033[92m{:.4f}\033[00m (deg)".format(
                stage_configuration.AXES_DECODER[str(axis_index)], relative_accuracy
            )
        )

    return relative_accuracy


def calculate_linearity(
    data: list, specs: get_specs.mems_specs, axis_index: int
) -> float:
    """_summary_

    Args:
        data (list):  A, X, Y, Z, UT, PT,
        specs (get_specs.mems_specs): _description_
        axis_index (int): _description_

    Returns:
        float: _description_
    """
    calculated_angle = 0.0
    max_nonlinearity = 0.0
    nonlinearity = []

    linearity_limit = specs.linearity[axis_index]

    for arr in data:
        # initialize some lists for data
        output = []
        angle = []

        # build up the data arrays by looping over each record.
        for record in arr:
            # print(record)
            angle.append(record[0])
            # select the correct output based on axis of interest.
            if axis_index == 0:
                output.append(record[1])
            elif axis_index == 1:
                output.append(record[2])
            elif axis_index == 2:
                output.append(record[3])
            else:
                output.append(record[1])

        # print(angle)
        # print(output)
        coefficients, *_ = linear_algebra.solve_least_squares(output, angle, order=1)

        calculated_angle = polynomial(output, coefficients)

        nonlinearity.extend(
            100.0 * abs(calculated_angle[i] - angle[i]) / (max(angle) - min(angle))
            for i in range(len(angle))
        )
    max_nonlinearity = max(nonlinearity)

    if max_nonlinearity > linearity_limit:
        print(
            "linearity for the {} axis: \033[91m{:.4f}\033[00m (% FS)".format(
                stage_configuration.AXES_DECODER[str(axis_index)], max_nonlinearity
            )
        )
    else:
        print(
            "linearity for the {} axis: \033[92m{:.4f}\033[00m (% FS)".format(
                stage_configuration.AXES_DECODER[str(axis_index)], max_nonlinearity
            )
        )

    return max_nonlinearity


def calculate_verification_accuracy(
    data: list, specs: get_specs.mems_specs, axis_index: int
) -> None:
    """_summary_

    Args:
        data (list): _description_
        specs (get_specs.mems_specs): _description_
        axis_index (int): _description_
    """
    error = []
    for arr in data:
        # build up the data arrays by looping over each record.
        for record in arr:
            # print(record)
            angle = record[0]
            # select the correct output based on axis of interest.
            if axis_index == 0:
                output = record[1]
            elif axis_index == 1:
                output = record[2]
            elif axis_index == 2:
                output = record[3]
            error.append(angle - output)

    if abs(max(error)) > specs.accuracy[axis_index]:
        print(
            f"Max Error ({specs.output_units}) for {axis_index} Axis: \033[91m{max(error):.5f}\033[00m"
        )
    else:
        print(
            f"Max Error ({specs.output_units}) for {axis_index} Axis: \033[92m{max(error):.5f}\033[00m"
        )


def calculate_cross_axis_error(
    data: list, specs: get_specs.mems_specs, axis_index: int
) -> None:
    """_summary_

    Args:
        data (list): _description_
        specs (get_specs.mems_specs): _description_
        axis_index (int): _description_
    """
    error = []
    for arr in data:
        # build up the data arrays by looping over each record.
        for record in arr:
            if axis_index == 0:
                output = record[2]
            elif axis_index == 1:
                output = record[1]
            elif axis_index == 2:
                output = record[1]
            error.append(output)

    if abs(max(error)) > specs.mpa[axis_index]:
        print(
            f"Max Cross Axis Error ({specs.output_units}) for {axis_index} Axis: \033[91m{max(error):.5f}\033[00m"
        )
    else:
        print(
            f"Max Cross Axis Error ({specs.output_units}) for {axis_index} Axis: \033[92m{max(error):.5f}\033[00m"
        )
