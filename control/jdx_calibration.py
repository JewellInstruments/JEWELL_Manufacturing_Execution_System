import datetime
import logging
import math
import os
import sys

from instrumentation import chamber
from instrumentation import thermometry
from instrumentation import motor_control

from system import digital_coms
from system import settings
from system import serial_protocols
from system import countdown
from system import stage_configuration

from network import get_specs
from network import filesystem


deactivated_sensors_list = []


def create_calibration_data_file(unit_id_dict: dict) -> None:
    """create the calibration data file

    Args:
        data_from_sensors (dict): _description_
        unit_id_dict (dict): _description_
    """

    for port in unit_id_dict.keys():
        if port not in deactivated_sensors_list:
            file = filesystem.build_test_data_file(unit_id_dict, port)

            with open(file, "w") as write_file:
                write_file.write(
                    "datetime,test,axis,cycle,temp,angle,xoutput,youtput,zoutput,utemp,ptemp\n"
                )


def digital_mems_calibration(
    specs: get_specs.mems_specs,
    unit_id_dict: dict,
    port_dict: dict,
    instrumentation: dict,
) -> None:
    """MEMs calibration sequence for digital units.

    Args:
        specs (get_specs.mems_specs): _description_
        unit_id_dict (dict): _description_
        port_dict (dict): _description_
        instrumentation (dict): _description_
    """
    try:

        initialize_calibration_data_file(unit_id_dict, specs)

        for cycle in range(len(specs.cycles)):

            if specs.cycles[cycle] == 1:
                print("Starting calibration of sensors")
                cycle_through_axes(
                    specs, unit_id_dict, port_dict, instrumentation, cycle
                )
                for port in port_dict.keys():
                    print(f"Loading LUT to sensor {port}")
                    file = filesystem.build_test_data_file(unit_id_dict, port)
                    digital_coms.load_lut_table_to_sensor(port, file)

            else:
                print("Starting verification of sensors")
                cycle_through_axes(
                    specs, unit_id_dict, port_dict, instrumentation, cycle
                )

            # reset_axis(specs.mount, instrumentation)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logging.warning(e)
        print(f"\t{e} -> Line {exc_tb.tb_lineno}")

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


def cycle_through_axes(
    specs: get_specs.mems_specs,
    unit_id_dict: dict,
    port_dict: dict,
    instrumentation: dict,
    cycle: int,
) -> None:
    """cycle atp through the axes as defined by the spec sheet.

    Args:
        specs (get_specs.mems_specs): _description_
        unit_id_dict (dict): _description_
        port_dict (dict): _description_
        instrumentation (dict): _description_
    """
    try:
        for axis in range(specs.axes_no):
            print(f"Testing the {axis} axis")

            jdx_polarity_verification(specs, port_dict, instrumentation, axis)

            cycle_through_temps(
                specs, unit_id_dict, cycle, port_dict, instrumentation, axis
            )

            if axis < specs.axes_no:
                reset_axis(specs.mount, instrumentation)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logging.warning(e)
        print(f"\t{e} -> Line {exc_tb.tb_lineno}")

    return


def cycle_through_temps(
    specs: get_specs.mems_specs,
    unit_id_dict: dict,
    cycle: int,
    port_dict: dict,
    instrumentation: dict,
    axis: int,
) -> None:
    """_summary_

    Args:
        specs (get_specs.mems_specs): _description_
        unit_id_dict (dict): _description_
        cycle (int): _description_
        port_dict (dict): _description_
        instrumentation (dict): _description_
        axis (int): _description_
    """
    try:
        if cycle == 0:
            temps_array = specs.cal_temps

            temp_tol_array = specs.cal_temp_tol

        else:
            temps_array = specs.verify_temps

            temp_tol_array = specs.verify_temp_tol

        for temp_idx in range(len(temps_array)):
            print(f"Sending chamber to {temps_array[temp_idx]} C")

            chamber.ramp_to_temp(
                instrumentation["Chamber"],
                instrumentation["DataAq"],
                temps_array[temp_idx],
                temp_tol_array[temp_idx],
            )

            chamber.soak_at_temp(
                instrumentation["Chamber"],
                instrumentation["DataAq"],
                temps_array[temp_idx],
                specs.soak_time,
                temp_tol_array[temp_idx],
            )

            print(
                f"Done soaking at {temps_array[temp_idx]}. moving on to data collection."
            )

            cycle_through_angles(
                specs, unit_id_dict, port_dict, instrumentation, axis, cycle, temp_idx
            )

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logging.warning(e)
        print(f"\t{e} -> Line {exc_tb.tb_lineno}")

    return


def cycle_through_angles(
    specs: get_specs.mems_specs,
    unit_id_dict: dict,
    port_dict: dict,
    instrumentation: dict,
    axis: int,
    cycle: int,
    temp: int,
):
    """_summary_

    Args:
        specs (get_specs.mems_specs): _description_
        unit_id_dict (dict): _description_
        port_dict (dict): _description_
        instrumentation (dict): _description_
        axis (int): _description_
        cycle (int): _description_
        temp (int): _description_
    """
    try:

        for point_idx, point in enumerate(specs.cal_points_array, start=1):
            print(
                f"\nMoving to {point} degrees ({point_idx}/{len(specs.cal_points_array)})"
            )

            motor_control.move_stage_to_angle(instrumentation["Stage"], point)

            countdown.countdown(specs.settle_time)

            for _ in range(stage_configuration.DATA_ATTEMPTS):
                # get data from all sensors.

                data_from_sensors = get_data_from_sensors(
                    port_dict,
                    instrumentation["Stage"],
                    instrumentation["DataAq"],
                )

                # make sure the dataset from the all the sensors is not empty. i.e error.

                valid_data_flag = check_data_from_sensors(data_from_sensors)

                if valid_data_flag is True:
                    break

            # let the user see what the data from all the sensors looks like.
            display_results_from_sensor(data_from_sensors, specs, axis, cycle, temp)

            # write the data to a log file for each serial number tested.
            log_data_from_sensors(
                data_from_sensors,
                unit_id_dict,
                axis,
                cycle,
                temp,
                "Thermal Calibration",
            )

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logging.warning(e)
        print(f"\t{e} -> Line {exc_tb.tb_lineno}")

    return


def display_results_from_sensor(
    data_from_sensors: dict,
    specs: get_specs.mems_specs,
    axis: int,
    cycle: int,
    temp: int,
) -> None:
    """_summary_

    Args:
        data_from_sensors (dict): _description_
        specs (get_specs.mems_specs): _description_
        axis (int): _description_
        cycle (int): _description_
        temp (int): _description_
    """
    try:
        test_number = os.environ.get("TEST_NUMBER")

        if cycle == 0:
            num_temps = len(specs.cal_temps)
        else:
            num_temps = len(specs.verify_temps)

        print(
            f"\nStarting data collection for test {test_number} on the {axis} axis of cycle {cycle + 1}/{len(specs.cycles)} at temp {temp + 1}/{num_temps}\n"
        )

        for port in data_from_sensors.keys():
            if port not in deactivated_sensors_list:
                current_time = datetime.datetime.now().strftime(
                    settings.DATETIME_FORMAT
                )

                print(
                    "{} - {} - Angle: {:.5f}, Plate Temp: {:.2f}, X: {:.5f}, Y: {:.5f}, Z: {:.5f}, T: {:.2f}".format(
                        current_time,
                        port,
                        data_from_sensors[port]["A"],
                        data_from_sensors[port]["P"],
                        data_from_sensors[port]["X"],
                        data_from_sensors[port]["Y"],
                        data_from_sensors[port]["Z"],
                        data_from_sensors[port]["T"],
                    )
                )

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()

        print(e)

        logging.warning(e)


def log_data_from_sensors(
    data_from_sensors: dict,
    unit_id_dict: dict,
    axis: int,
    cycle: int,
    temp: int,
    test_name: str,
) -> None:
    """_summary_

    Args:
        data_from_sensors (dict): _description_
        unit_id_dict (dict): _description_
        part_no (str): _description_
        axis (int): _description_
        cycle (int): _description_
        temp (int): _description_
    """
    try:

        for port in data_from_sensors.keys():
            if port not in deactivated_sensors_list:
                file = filesystem.build_test_data_file(unit_id_dict, port)

                current_time = datetime.datetime.now().strftime(
                    settings.DATETIME_FORMAT
                )

                with open(file, "a") as write_file:
                    write_file.write(
                        f'{current_time},{stage_configuration.__STAGE_NAME__},{test_name},{axis},{cycle},{temp},{data_from_sensors[port]["A"]},{data_from_sensors[port]["X"]},{data_from_sensors[port]["Y"]},{data_from_sensors[port]["Z"]},{data_from_sensors[port]["T"]},{data_from_sensors[port]["P"]}\n'
                    )

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()

        print(e)

        logging.warning(e)


def get_data_from_sensors(
    port_dict: dict,
    stage_port: serial_protocols.serial_open,
    data_aq_port: serial_protocols.serial_open,
    angle: float = 0.0,
    spoof_temp: float = 0.0,
) -> None:
    """_summary_

    Args:
        port_dict (dict): _description_
        stage_port (serial_protocols.serial_open): _description_
        data_aq_port (serial_protocols.serial_open): _description_
        angle (float, optional): _description_. Defaults to 0.0.
        spoof_temp (float, optional): _description_. Defaults to 0.0.

    Returns:
        _type_: _description_
    """
    try:
        data = {}

        for port in port_dict.keys():
            if port not in deactivated_sensors_list:
                for _ in range(3):
                    x, y, z, t = digital_coms.get_position_data_from_jdx(
                        port_dict[port]
                    )

                angle = motor_control.get_position_from_stage(
                    stage_port,
                )

                plate_temp, pilar_temp = thermometry.get_system_temperatures()

            else:
                print(
                    f"skipping {port_dict[port].port} since it is in the dead sensor group."
                )

                x, y, z, t = 0.0, 0.0, 0.0, 0.0

                angle = math.nan

                plate_temp = 22.5

            data[port] = {
                "A": angle,
                "X": x,
                "Y": y,
                "Z": z,
                "T": t,
                "P": plate_temp,
            }

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()

        print(e)

        logging.warning(e)

        data = {}

    return data


def jdx_polarity_verification(
    specs: get_specs.mems_specs, port_dict: dict, instrumentation: dict, axis: int
) -> None:
    """_summary_

    Args:
        specs (get_specs.mems_specs): _description_
        port_dict (dict): _description_
        instrumentation (dict): _description_
        axis (int): _description_
    """
    try:
        print(
            "Moving one step in the positive direction. Each sensor should show a increase in ADC counts."
        )

        print("Collecting data")
        data_at_null = get_data_from_sensors(
            port_dict,
            instrumentation["Stage"],
            instrumentation["DataAq"],
        )
        display_results_from_sensor(data_at_null, specs, axis, 0, 1)

        angle = abs(specs.cal_points_array[1] - specs.cal_points_array[0])

        angle = motor_control.move_stage_to_angle(instrumentation["Stage"], angle)

        print("Collecting data")
        data_at_positive_tilt = get_data_from_sensors(
            port_dict,
            instrumentation["Stage"],
            instrumentation["DataAq"],
        )
        display_results_from_sensor(data_at_positive_tilt, specs, axis, 0, 1)

        validated_polarity(data_at_positive_tilt, data_at_null, axis)

        angle = motor_control.move_stage_to_angle(instrumentation["Stage"], 0)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logging.warning(e)
        print(f"\t{e} -> Line {exc_tb.tb_lineno}")

    return


def validated_polarity(
    data_at_positive_tilt: dict, data_at_null: dict, axis: int
) -> None:
    """_summary_

    Args:
        data_at_positive_tilt (dict): _description_
        data_at_null (dict): _description_
        axis (int): _description_
    """
    deactivated_sensors_list = []

    for port in data_at_positive_tilt.keys():
        if port not in deactivated_sensors_list:
            if axis == 0:
                delta = data_at_positive_tilt[port]["X"] - data_at_null[port]["X"]

            elif axis == 1:
                delta = data_at_positive_tilt[port]["Y"] - data_at_null[port]["Y"]

            elif axis == 2:
                delta = data_at_positive_tilt[port]["Z"] - data_at_null[port]["Z"]

            if delta > 0:
                print(f"{port} has the wrong polarity.")

            else:
                print(f"{port} is mounted correctly and functioning properly.")


def configure_jdx(
    specs: get_specs.mems_specs, unit_id_dict: dict, test: str, sensor_class_code: int
) -> dict:
    try:
        port_dict = {}

        for key in unit_id_dict.keys():
            # dev = mock_port(settings.SERIAL_PORT_MAPPER[key])
            if specs.serial_protocol == "RS232":
                port = stage_configuration.SERIAL_PORT_MAPPER_RS232[key]
            elif specs.serial_protocol == "RS485":
                port = stage_configuration.SERIAL_PORT_MAPPER_RS485[key]
            elif specs.serial_protocol == "LAN":
                pass

            # uncomment when ready to go to live testing.

            dev = serial_protocols.serial_open(
                port, 19200, bytesize=8, parity="E", use_visa=False
            )

            port_dict[key] = dev

            print(f"\nConfiguring sensor on {port}")

            digital_coms.turn_streaming_off(dev)

            digital_coms.unlock_jdx(dev)

            digital_coms.set_output(dev, sensor_class_code)

            if test == "Tumble Test":
                digital_coms.set_factory_personality(dev)

                digital_coms.set_identity_matrix(dev)

                digital_coms.set_decimation(dev, 25)
            else:
                digital_coms.set_decimation(dev, 1)

            digital_coms.set_output_bandwidth(dev, specs.bandwidth)

            digital_coms.set_RS485_termination(dev)

            digital_coms.nonvolatile_save(dev)

            digital_coms.turn_off_self_test(dev)

            digital_coms.clear_faults(dev)

            digital_coms.set_verbosity(dev)

            digital_coms.nonvolatile_save(dev)

            if test == "Tumble Test":
                digital_coms.erase_lut(dev)

            # digital_coms.soft_reset(dev)

            print(f"Done configuring sensor on {port}\n")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()

        print(e)

        logging.warning(e)

    return port_dict


class mock_port:
    def __init__(self, port):
        self.port = port

    def write(self, text):
        print(text)

    def readline(self):
        print("reading data")


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


def check_data_from_sensors(data: dict) -> bool:
    """_summary_

    Args:
        data (dict): _description_

    Returns:
        bool: _description_
    """
    return True if data is not {} else False
