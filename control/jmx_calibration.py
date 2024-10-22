import os
import sys
import datetime
import logging
import math

from system import settings
from system import countdown

from system import stage_configuration

from instrumentation import chamber
from instrumentation import motor_control
from instrumentation import data_aq_read
from instrumentation import data_aq_init
from instrumentation import thermometry

from analytics import numerical_methods
from analytics import statistical_methods
from analytics import linear_algebra

from network import get_specs
from network import filesystem


def analog_mems_calibration(
    specs: get_specs.mems_specs,
    instrumentation: dict,
    unit_id_dict: dict,
    axis_override: int = 0,
) -> None:
    """this function handles the control of the calibration of the analog mems sensors.

    Args:
        specs (get_specs.mems_specs): product definition used for calibration.
        instrumentation (dict): all the instrumentation serial port objects in a dict.
        unit_id_dict (dict): unit_id, serial number, part number, rma number all in a
        useable dict.
    """

    initialize_calibration_data_file(unit_id_dict, specs)

    # determine whether to override the starting axis.
    if axis_override != 0:
        axis = axis_override
    else:
        axis = 0

    home_stage(instrumentation)

    allow_sensors_to_warm_up(specs)

    if True:
        print("Testing operational voltage sweep")
        success_flag = operational_voltage_test(specs, instrumentation, unit_id_dict)

    # use while loop so top level can override which axis to start with.
    while axis < specs.axes_no:
        for cycle in range(len(specs.cycles)):
            # test SETS and ZTS in chamber. Skip if product does not require.
            print(f"Testing the {stage_configuration.AXES_DECODER[str(axis)]} axis")
            if axis > 0:
                reset_axis(stage_configuration.AXES_DECODER[str(axis)], instrumentation)
            if specs.test_temp:
                if stage_configuration.CHAMBER_AVAILABLE:
                    print(settings.TERMINAL_SPACER)
                    print("Testing sensor metrics over temperature.")
                    for temp_index in range(len(specs.cal_temps_array)):
                        temp_tol = specs.cal_temps_array[temp_index]
                        temperature = specs.cal_temp_tol_array[temp_index]

                        chamber.ramp_to_temp(
                            instrumentation["Chamber"],
                            instrumentation["DataAq"],
                            temperature,
                            temp_tol,
                        )

                        chamber.soak_at_temp(
                            instrumentation["Chamber"],
                            instrumentation["DataAq"],
                            temperature,
                            specs.soak_time,
                            temp_tol,
                        )

                        if specs.test_linearity:
                            print(settings.TERMINAL_SPACER)
                            print(
                                "Testing the linearity/bias/transverse axis misalignment of the sensor."
                            )
                            success_flag = test_linearity(
                                specs, instrumentation, unit_id_dict, axis, cycle
                            )
                        else:
                            print(settings.TERMINAL_SPACER)
                            print("Testing the Full Scale Output of the sensor.")
                            success_flag = test_full_scale(
                                specs, instrumentation, unit_id_dict, axis
                            )
                        print(f"Test v: {success_flag}")
                        print(settings.TERMINAL_SPACER)

                        # test bias (zero tilt) for JMx sensor. Skip if product does not require.
                        if specs.test_bias:
                            print(settings.TERMINAL_SPACER)
                            print("Testing Zero Tilt")
                            success_flag = test_zero_tilt_misalignment(
                                specs, instrumentation, unit_id_dict, axis
                            )
                        else:
                            success_flag = False
                            print(settings.TERMINAL_SPACER)
                            print("Zero Tilt are not tested for this sensor.")
                        print(f"Test Zero Tilt: {success_flag}")
                        print(settings.TERMINAL_SPACER)
                else:
                    print(settings.TERMINAL_SPACER)
                    print(
                        "Unable to test over temperature. Chamber not installed at this station. Retrieve and review temp test data or enter manually."
                    )
                    load_temp_test_data_manually(specs, unit_id_dict)
            else:
                print(settings.TERMINAL_SPACER)
                print("Unit not tested over temperature.")
                # test linearity or FSO. Skip if product does not require.
                if specs.test_linearity:
                    print(settings.TERMINAL_SPACER)
                    print(
                        "Testing the linearity/bias/transverse axis misalignment of the sensor."
                    )

                    success_flag = test_linearity(
                        specs, instrumentation, unit_id_dict, axis, cycle
                    )
                else:
                    print(settings.TERMINAL_SPACER)
                    print("Testing the Full Scale Output of the sensor.")
                    success_flag = test_full_scale(
                        specs, instrumentation, unit_id_dict, axis
                    )
                print(f"Test succeeded: {success_flag}")
                print(settings.TERMINAL_SPACER)

            # test bias (zero tilt) for JMx sensor. Skip if product does not require.
            if specs.test_bias and specs.test_linearity is False:
                print(settings.TERMINAL_SPACER)
                print("Testing Zero Tilt")
                success_flag = test_zero_tilt_misalignment(
                    specs, instrumentation, unit_id_dict, axis
                )
            else:
                success_flag = False
                print(settings.TERMINAL_SPACER)
                print("Zero Tilt are not tested for this sensor.")
            print(f"Test Zero Tilt: {success_flag}")
            print(settings.TERMINAL_SPACER)

            # Test the Y axis transverse axis misalignment (pendulous axis). Skip if product does not require.
            if specs.test_pend_axis and specs.test_linearity is False:
                print(settings.TERMINAL_SPACER)
                print("Testing Transverse Axis Misalignment")
                input(
                    "Please mount the sensor such that the non sensitive axis is under test."
                )
                success_flag = test_transverse_axis_misalignment(
                    specs, instrumentation, unit_id_dict, axis
                )
            else:
                success_flag = False
                print(settings.TERMINAL_SPACER)
                print("Transverse Axis Misalignment is not tested for this sensor.")
            print(f"Test Transverse Axis Misalignment: {success_flag}")
            print(settings.TERMINAL_SPACER)

            # Test repeatability. Skip if product does not require.
            if specs.test_repeatability:
                print(settings.TERMINAL_SPACER)
                print("Testing Repeatability")
            else:
                success_flag = False
                print(settings.TERMINAL_SPACER)
                print("Repeatability is not tested for this sensor.")
            print(settings.TERMINAL_SPACER)

            # test bandwidth. Skip if product does not require.
            if specs.test_bandwidth:
                print(settings.TERMINAL_SPACER)
                print("Testing Bandwidth")
                test_bandwidth(specs, unit_id_dict, axis)
            else:
                success_flag = False
                print(settings.TERMINAL_SPACER)
                print("Bandwidth is not tested for this sensor.")
            print(settings.TERMINAL_SPACER)

            # test noise. Skip if product does not require.
            if specs.test_hysteresis:
                print(settings.TERMINAL_SPACER)
                print("Testing Noise")
                success_flag = test_noise(specs, instrumentation, unit_id_dict, axis)
            else:
                success_flag = False
                print(settings.TERMINAL_SPACER)
                print("Noise is not tested for this sensor.")
            print(settings.TERMINAL_SPACER)

            # Test resolution. Skip if product does not require.
            if specs.test_resolution:
                print(settings.TERMINAL_SPACER)
                print("Testing Resolution")
            else:
                success_flag = False
                print(settings.TERMINAL_SPACER)
                print("Resolution is not tested for this sensor.")
            print(settings.TERMINAL_SPACER)

            print(settings.TERMINAL_SPACER)

        axis += 1
        if axis_override != 0 and axis >= specs.axes_no:
            # should the axis counter exceed the number of axes, reset to zero.
            axis = 0

    return


def reset_axis(message: str, instrumentation: dict) -> None:
    """reset and display message.

    Args:
        message (str): _description_
    """

    _ = motor_control.move_stage_to_angle(instrumentation["Stage"], 0)
    print(f"\nReset axis to the {message}")

    input("Press enter to continue")

    return


def load_temp_test_data_manually(
    specs: get_specs.mems_specs, unit_id_dict: dict
) -> None:
    for port in unit_id_dict:
        serial_no = unit_id_dict[port]["serial_no"]
        print(f"Enter data for {serial_no}.")

        for temp in specs.cal_temps:
            data = input(f"Enter data for {temp}: ")
            print(data)
    return


def get_data_from_sensors(
    unit_id_dict: dict,
    specs: get_specs.mems_specs,
    instrumentation: dict,
    angle: float = 0,
    mode: str = "Voltage",
) -> dict:

    channels = len(unit_id_dict)
    data = data_aq_read.read_data_from_data_aq(
        instrumentation["DataAq"], mode=mode, channels=channels
    )

    plate_temp, pilar_temp = thermometry.get_system_temperatures()

    position = motor_control.get_position_from_stage(instrumentation["Stage"])
    if specs.sensor_type == "accelerometer":
        actual_position = math.sin(math.radians(position))
    else:
        actual_position = position

    return {
        port: {
            "X": data[port][0],
            "Y": data[port][1],
            "Z": 0,
            "T": data[port][2],
            "A": actual_position,
            "P": plate_temp,
        }
        for port in unit_id_dict
    }


def home_stage(instrumentation: dict) -> None:
    """
    A base function to move the stage to home after each test is complete.
    """

    angle_0: float = 0.0
    motor_control.move_stage_to_angle(instrumentation["Stage"], angle_0)


def move_to_angle_and_collect_data(
    specs: get_specs.mems_specs, instrumentation: dict, unit_id_dict: dict, angle: float
) -> dict:
    """Command the rotary stage to an angle and collect data for each sensor.

    Returns:
        dict: Outputs from each sensor in a dict keyed by the port they are connected to
    """
    if specs.sensor_type == "accelerometer":
        display_angle = math.sin(math.radians(angle))
    else:
        display_angle = angle
    display_units = specs.input_units
    print(f"\nMoving stage to {display_angle:.6f} ({display_units})")
    motor_control.move_stage_to_angle(instrumentation["Stage"], angle)

    print(
        f"Sitting at angle {display_angle:.6f} ({display_units}) for {specs.settle_time} s."
    )
    countdown.countdown(specs.settle_time)

    print("Collecting data")
    return get_data_from_sensors(unit_id_dict, specs, instrumentation, angle=angle)


def test_static_metrics(
    specs: get_specs.mems_specs,
    instrumentation: dict,
    unit_id_dict: dict,
    axis: int,
    test: str,
) -> list[dict, dict]:
    """move to an angle and collect/log data, then move to second angle and collect/log data.

    Args:
        specs (get_specs.mems_specs): _description_
        instrumentation (dict): _description_
        unit_id_dict (dict): _description_
        axis (int): _description_
        test (str): _description_

    Returns:
        bool: _description_
    """

    if test == "Z-Transverse Axis Misalignment":
        angle_1: float = 0.0
        angle_2: float = 180.0
    elif test == "Y-Transverse Axis Misalignment":
        angle_1: float = -90.0
        angle_2: float = 90
    elif test == "Full-Scale":
        angle_1: float = max(specs.cal_points_array)
        angle_2: float = min(specs.cal_points_array)

    data_from_sensors_1: dict = move_to_angle_and_collect_data(
        specs, instrumentation, unit_id_dict, angle_1
    )

    log_calibration_data(
        unit_id_dict,
        data_from_sensors_1,
        axis,
        0,
        0,
        test,
        specs.input_units,
        specs.output_units,
    )

    data_from_sensors_2: dict = move_to_angle_and_collect_data(
        specs, instrumentation, unit_id_dict, angle_2
    )

    log_calibration_data(
        unit_id_dict,
        data_from_sensors_2,
        axis,
        0,
        0,
        test,
        specs.input_units,
        specs.output_units,
    )

    home_stage(instrumentation)

    return data_from_sensors_1, data_from_sensors_2


def test_zero_tilt_misalignment(
    specs: get_specs.mems_specs, instrumentation: dict, unit_id_dict: dict, axis: int
) -> bool:
    """
    This will collect data for each sensor under test at 0 degrees and 180 degrees.

    Returns:
        boolean: pass/fail
    """

    if specs.output_type == "analog voltage":
        data_from_sensors_0, data_from_sensors_180 = test_static_metrics(
            specs, instrumentation, unit_id_dict, axis, "Z-Transverse Axis Misalignment"
        )

        axis_flag = stage_configuration.AXES_DECODER[str(axis)]

        bias = {
            port: numerical_methods.compute_bias(
                data_from_sensors_0[port][axis_flag],
                data_from_sensors_180[port][axis_flag],
                1,
            )
            for port in unit_id_dict
        }

        output_axis_misalignment = {
            port: numerical_methods.compute_output_axis(
                data_from_sensors_0[port][axis_flag],
                data_from_sensors_180[port][axis_flag],
                1,
            )
            for port in unit_id_dict
        }

    for port in bias:
        print(
            f"Bias for {port}: {bias[port]:.6f}, Moa = {output_axis_misalignment[port]:.3f}"
        )

    return True


def test_transverse_axis_misalignment(
    specs: get_specs.mems_specs, instrumentation: dict, unit_id_dict: dict, axis: int
) -> bool:
    """
    This will collect data for each sensor under test at -90 degrees and 90 degrees.

    Returns:
        boolean: pass/fail
    """

    if specs.output_type == "analog voltage":
        data_from_sensors_90_n, data_from_sensors_90_p = test_static_metrics(
            specs, instrumentation, unit_id_dict, axis, "Y-Transverse Axis Misalignment"
        )

        axis_flag = stage_configuration.AXES_DECODER[str(axis)]

        pendulous_axis_misalignment = {
            port: numerical_methods.compute_pendulous_axis_misalignment(
                data_from_sensors_90_n[port][axis_flag],
                data_from_sensors_90_p[port][axis_flag],
                1,
            )
            for port in unit_id_dict
        }
        for port in pendulous_axis_misalignment:
            print(f"Mpa for {port}: {pendulous_axis_misalignment[port]:.3f}")
    return True


def test_linearity(
    specs: get_specs.mems_specs, instrumentation: dict, unit_id_dict: dict, axis: int, cycle: int
) -> bool:
    """This will test the linearity of each sensor over a prescribed range and number
    of points.

    Returns:
        boolean: pass/fail
    """
    cycle = 0
    temp = 0
    input_current_tested = False

    if specs.output_type == "analog voltage":

        data_from_sensors_pend_ccw: dict = move_to_angle_and_collect_data(
            specs, instrumentation, unit_id_dict, -90
        )

        log_calibration_data(
            unit_id_dict,
            data_from_sensors_pend_ccw,
            axis,
            cycle,
            temp,
            "Y-Transverse Axis Misalignment",
            specs.input_units,
            specs.output_units,
        )

    for point in specs.cal_points_array:
        if specs.test_input_current:
            print("Checking input current for all sensors.")
            if (
                abs(point) == max(specs.cal_points_array)
                and input_current_tested is False
            ):
                test_input_current(specs, instrumentation, unit_id_dict)
                input_current_tested = True

        if specs.output_type == "analog voltage":
            data_from_sensors: dict = move_to_angle_and_collect_data(
                specs, instrumentation, unit_id_dict, point
            )

            log_calibration_data(
                unit_id_dict,
                data_from_sensors,
                axis,
                cycle,
                temp,
                "Linearity",
                specs.input_units,
                specs.output_units,
            )

    if specs.output_type == "analog voltage":

        data_from_sensors_pend_cw: dict = move_to_angle_and_collect_data(
            specs, instrumentation, unit_id_dict, 90
        )

        log_calibration_data(
            unit_id_dict,
            data_from_sensors_pend_cw,
            axis,
            cycle,
            temp,
            "Y-Transverse Axis Misalignment",
            specs.input_units,
            specs.output_units,
        )

        data_from_sensors_180: dict = move_to_angle_and_collect_data(
            specs, instrumentation, unit_id_dict, 180
        )

        log_calibration_data(
            unit_id_dict,
            data_from_sensors_180,
            axis,
            cycle,
            temp,
            "Z-Transverse Axis Misalignment",
            specs.input_units,
            specs.output_units,
        )

        data_from_sensors_0: dict = move_to_angle_and_collect_data(
            specs, instrumentation, unit_id_dict, 0
        )

        log_calibration_data(
            unit_id_dict,
            data_from_sensors_0,
            axis,
            cycle,
            temp,
            "Z-Transverse Axis Misalignment",
            specs.input_units,
            specs.output_units,
        )

    home_stage(instrumentation)

    axis_flag = stage_configuration.AXES_DECODER[str(axis)]

    scale_factor = {}
    # y_intercept = {}
    nonlinearity = {}
    # bias = {}
    # Mza = {}
    # Mya = {}
    for port in unit_id_dict:
        output_data, input_data = filesystem.get_test_data_from_file(
            unit_id_dict, port, axis_flag, "Linearity"
        )

        coefficients, *_ = linear_algebra.solve_least_squares(
            input_data, output_data, order=1
        )
        max_nonlieanrity = numerical_methods.nonlinearity(
            input_data, output_data, coefficients
        )
        # print(coefficients)
        scale_factor[port] = coefficients[1]
        # y_intercept[port] = coefficients[1]
        nonlinearity[port] = max_nonlieanrity

    for port in unit_id_dict:
        print(
            f"Scale Factor ({specs.output_units}/g) for {port}: {scale_factor[port]:.3f}"
        )
        # print(f"Y-Intercept (g) for {port}: {y_intercept[port]:.6f}")
        print(f"Max Nonlinearity (% FRO) for {port}: {nonlinearity[port]:.2f}")

    return True


def test_full_scale(
    specs: get_specs.mems_specs, instrumentation: dict, unit_id_dict: dict, axis: int
) -> bool:
    """This will test the full scale output of each sensor over a prescribed range
    and number of points.

    Returns:
        boolean: pass/fail
    """
    if specs.output_type == "analog voltage":
        data_from_sensors_max, data_from_sensors_min = test_static_metrics(
            specs, instrumentation, unit_id_dict, axis, "Full-Scale"
        )

    axis_flag = stage_configuration.AXES_DECODER[str(axis)]

    full_scale_output = {
        port: numerical_methods.compute_full_scale_output(
            data_from_sensors_max[port][axis_flag],
            data_from_sensors_min[port][axis_flag],
        )
        for port in unit_id_dict
    }
    for port in full_scale_output:
        print(f"Mpa for {port}: {full_scale_output[port]}")

    return True


def log_calibration_data(
    unit_id_dict: dict,
    data_dict: dict,
    axis_index: int,
    cycle_index: int,
    temp_index: int,
    test_type: str = "",
    input_units: str = "g",
    output_units: str = "VDC",
) -> None:
    """log data from all units into csv file.

    Args:
        unit_id_dict (dict): _description_
        data_dict (dict): _description_
        axis_index (int): _description_
        cycle_index (int): _description_
        temp_index (int): _description_
        test_type (str, optional): _description_. Defaults to "".
    """
    try:

        for port in data_dict:
            file = filesystem.build_test_data_file(unit_id_dict, port)

            current_time = datetime.datetime.now().strftime(settings.DATETIME_FORMAT)

            print_data_to_terminal(data_dict, port, input_units, output_units)

            with open(file, "a") as write_file:
                write_file.write(
                    f'{current_time},{stage_configuration.__STAGE_NAME__},{test_type},{axis_index},{cycle_index},{temp_index},{data_dict[port]["A"]},{data_dict[port]["X"]},{data_dict[port]["Y"]},{data_dict[port]["Z"]},{data_dict[port]["T"]},{data_dict[port]["P"]}\n'
                )
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        err = f"Error occurred at {exc_tb.tb_lineno} - {e}"
        print(err)
        logging.warning(err)


def print_data_to_terminal(
    data_dict: dict, port: str, input_units: str, output_units: str
) -> None:
    """standardize how data is displayed for the JMx series sensors when testing.

    Args:
        data_dict (dict): data dict for all the sensors. in the form of {PORT_<1,2,3...>: {x: x, y: y, z: z, t: t, a: a... }, ...
        port (str): which port is being printed.
    """
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(
        f'{date_time} - Port: {port}\nInput ({input_units}): {data_dict[port]["A"]:.6f}\tX axis ({output_units}): {data_dict[port]["X"]:.6f}\tY axis ({output_units}): {data_dict[port]["Y"]:.6f}\tZ axis ({output_units}): {data_dict[port]["Z"]:.6f}\tUnit Temp (C): {data_dict[port]["T"]:.2f}\tPlate Temp (C): {data_dict[port]["P"]:.2f}'
    )
    return


def test_noise(
    specs: get_specs.mems_specs, instrumentation: dict, unit_id_dict: dict, axis: int
) -> bool:
    if specs.output_type == "analog voltage":
        # configure DAQ for noise (VAC)
        mode = "Current" if specs.output_type == 3 else "Voltage"
        channels = 1

        data_aq_init.config_data_aq_for_voltage(
            instrumentation["DataAq"], mode, channels, False, "AC"
        )

        data = data_aq_read.read_data_from_data_aq(
            instrumentation["DataAq"], mode, channels
        )

        noise_data = {
            port: {
                "X": data[port][0],
                "Y": data[port][1],
                "Z": 0,
                "T": data[port][3],
                "A": 0,
                "P": statistical_methods.mean(data["PTEMP"]),
            }
            for port in unit_id_dict
        }

        # reconfigure DAQ for VDC
        data_aq_init.config_data_aq_for_voltage(
            instrumentation["DataAq"], mode, channels, False, "DC"
        )

        log_calibration_data(
            unit_id_dict, noise_data, axis, 0, 0, "Noise", specs.input_units, "VAC"
        )

    return True


def test_input_current(
    specs: get_specs.mems_specs, instrumentation: dict, unit_id_dict: dict
) -> None:

    return


def test_bandwidth(
    specs: get_specs.mems_specs,
    unit_id_dict: dict,
    axis_index: int = 0,
) -> None:
    filepath = os.environ.get("SO_FILEPATH")

    print(
        f"Bandwidth must be between {specs.bandwidth_tolerance_low} (Hz) and {specs.bandwidth_tolerance_high} (Hz)."
    )

    for port in unit_id_dict:
        serial_no = unit_id_dict[port]["serial_no"]
        part_no = unit_id_dict[port]["part_no"]
        file = os.path.join(
            filepath,
            f"partno_{part_no}_serialno_{serial_no}.csv",
        )

        while True:
            try:
                bandwidth = input(
                    f"Please enter the bandwidth (Hz) for Serial Number {serial_no}: "
                )
                bandwidth = float(bandwidth)
                if (bandwidth < specs.bandwidth_tolerance_low) or (
                    bandwidth > specs.bandwidth_tolerance_high
                ):
                    print("Bandwidth does not pass.")
                else:
                    print("Bandwidth passes!")
                    user_check = input(
                        f"Would you like to accept {bandwidth:.2f} (Hz) [y/n]: "
                    )
                    if user_check.upper() == "Y":
                        break
                    elif user_check.upper() == "N":
                        print("Okay, recycling back to input.")

                    else:
                        print(
                            "Please only use y or n. You are being recycled back to enter the bandwidth again."
                        )

            except ValueError:
                print("Could not covert bandwidth to a number. Please try again")

        current_time = datetime.datetime.now().strftime(settings.DATETIME_FORMAT)

        with open(file, "a") as write_file:
            write_file.write(
                f'{current_time},"Bandwidth",{axis_index},0,0,{bandwidth},0,0,0,0,0\n'
            )

    return


def initialize_calibration_data_file(
    unit_id_dict: dict, specs: get_specs.mems_specs
) -> None:
    """create the header for each calibration test file.

    Args:
        unit_id_dict (dict): unit id dict
        specs (get_specs.mems_specs): specs for settings units.
    """
    for port in unit_id_dict:
        file = filesystem.build_test_data_file(unit_id_dict, port)
        with open(file, "w") as write_file:
            write_file.write(
                f"Datetime,Stage,Test,Axis Index,Cycle Index,Temp Index,Input ({specs.input_units}),X Output ({specs.output_units}),Y Output ({specs.output_units}),Z Output ({specs.output_units}),Unit Temp (C),Plate Temp (C)\n"
            )


def operational_voltage_test(
    specs: get_specs.mems_specs, instrumentation: dict, unit_id_dict: dict
) -> bool:
    """This test will sweep the input supply to ensure the sensor will operate at all supply voltages listed.

    Args:
        specs (get_specs.mems_specs): _description_
        instrumentation (dict): _description_
        unit_id_dict (dict): _description_
        axis (int): _description_

    Returns:
        bool: _description_
    """
    """
        Go to max input
        start sweep and collect data for all sensors.
        monitor output of each for dip of 5% 
        reset power
        go home.
        log results to api. 
    
    """

    return True


def allow_sensors_to_warm_up(specs: get_specs.mems_specs) -> None:
    """allow sensor to warmup prior to testing.

    Args:
        specs (get_specs.mems_specs): class for test specs.
    """
    print(f"Sitting at home for {3*specs.settle_time} s.")
    countdown.countdown(3 * specs.settle_time)
