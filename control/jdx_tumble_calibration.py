import logging
import sys
import datetime

from analytics import analyze_cal_data

from control import jdx_calibration

from instrumentation import motor_control

# from network import commit_calibration_data
from network import get_specs

from system import digital_coms
from system import countdown
from system import settings


def jdx_tumble_calibration(
    specs: get_specs.mems_specs,
    unit_id_dict: dict,
    instrumentation: dict,
) -> None:
    """tumble calibration per ES

    Args:
        specs (get_specs.mems_specs): _description_
        port_dict (dict): _description_
        instrumentation (dict): _description_
    """

    port_dict = jdx_calibration.configure_jdx(
        specs, unit_id_dict, "Temp Test", sensor_class_code=10
    )

    try:
        tumble_matrix_plus, tumble_matrix_minus = jdx_tumble_sequence(
            specs, port_dict, instrumentation
        )
        # print(tumble_matrix_plus)
        # print(tumble_matrix_minus)
        orthonormal_matrix, offset_matrix = analyze_cal_data.analyze_jdx_tumble_data(
            specs, port_dict, tumble_matrix_plus, tumble_matrix_minus
        )

        for port in port_dict:

            digital_coms.load_tumble_data_to_sensor(
                port_dict[port], orthonormal_matrix[port], offset_matrix[port]
            )

        # commit_calibration_data.write_tumble_data_to_api(
        #     tumble_matrix_plus, tumble_matrix_minus, unit_id_dict
        # )

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e)
        logging.warning(e)

    return None


def jdx_tumble_sequence(
    specs: get_specs.mems_specs, port_dict: dict, instrumentation: dict
) -> tuple[dict, dict]:
    """Move to prescribed angles and take data

    Args:
        specs (get_specs.mems_specs): class of specs for unit
        port_dict (dict): dict of open serial ports to sensors
        instrumentation (dict): dict of open serial ports to instrumentation
    """

    motor_control.move_stage_to_angle(instrumentation["Stage"], 0)

    input("Press Enter to start.")

    print(f"Mount each sensor in the {specs.mount[0]} orientation")

    tumble_matrix_plus = {}
    tumble_matrix_minus = {}
    for key in port_dict:
        tumble_matrix_plus[key] = []
        tumble_matrix_minus[key] = []

    for axis in range(2):
        motor_control.move_stage_to_angle(instrumentation["Stage"], 90)

        countdown.countdown(specs.settle_time)

        data_p90 = jdx_calibration.get_data_from_sensors(
            port_dict, instrumentation["Stage"], instrumentation["DataAq"]
        )

        for port in port_dict:
            current_time = datetime.datetime.now().strftime(settings.DATETIME_FORMAT)
            print(
                "{} - {} - Angle: {:.5f}, Plate Temp: {}, X: {:.5f}, Y: {:.5f}, Z: {:.5f}, T: {:.5f}".format(
                    current_time,
                    port,
                    data_p90[port]["A"],
                    data_p90[port]["P"],
                    data_p90[port]["X"],
                    data_p90[port]["Y"],
                    data_p90[port]["Z"],
                    data_p90[port]["T"],
                )
            )

        motor_control.move_stage_to_angle(instrumentation["Stage"], -90)

        countdown.countdown(specs.settle_time)

        data_n90 = jdx_calibration.get_data_from_sensors(
            port_dict, instrumentation["Stage"], instrumentation["DataAq"]
        )

        for port in port_dict:
            current_time = datetime.datetime.now().strftime(settings.DATETIME_FORMAT)
            print(
                "{} - {} - Angle: {:.5f}, Plate Temp: {}, X: {:.5f}, Y: {:.5f}, Z: {:.5f}, T: {:.5f}".format(
                    current_time,
                    port,
                    data_n90[port]["A"],
                    data_n90[port]["P"],
                    data_n90[port]["X"],
                    data_n90[port]["Y"],
                    data_n90[port]["Z"],
                    data_n90[port]["T"],
                )
            )

        for key in port_dict:
            tumble_matrix_plus[key].append(
                [data_p90[key]["X"], data_p90[key]["Y"], data_p90[key]["Z"]]
            )
            tumble_matrix_minus[key].append(
                [data_n90[key]["X"], data_n90[key]["Y"], data_n90[key]["Z"]]
            )

        if axis < 1:
            motor_control.move_stage_to_angle(instrumentation["Stage"], 0)
            input(
                f"Mount each sensor in the {specs.mount[axis]} orientation. Then press enter."
            )

    motor_control.move_stage_to_angle(instrumentation["Stage"], 180)

    countdown.countdown(specs.settle_time)

    data_180 = jdx_calibration.get_data_from_sensors(
        port_dict, instrumentation["Stage"], instrumentation["DataAq"]
    )

    for port in port_dict:
        current_time = datetime.datetime.now().strftime(settings.DATETIME_FORMAT)
        print(
            "{} - {} - Angle: {:.5f}, Plate Temp: {}, X: {:.5f}, Y: {:.5f}, Z: {:.5f}, T: {:.5f}".format(
                current_time,
                port,
                data_180[port]["A"],
                data_180[port]["P"],
                data_180[port]["X"],
                data_180[port]["Y"],
                data_180[port]["Z"],
                data_180[port]["T"],
            )
        )

    motor_control.move_stage_to_angle(instrumentation["Stage"], 0)

    countdown.countdown(specs.settle_time)

    data_0 = jdx_calibration.get_data_from_sensors(
        port_dict, instrumentation["Stage"], instrumentation["DataAq"]
    )

    for port in port_dict:
        current_time = datetime.datetime.now().strftime(settings.DATETIME_FORMAT)
        print(
            "{} - {} - Angle: {:.5f}, Plate Temp: {}, X: {:.5f}, Y: {:.5f}, Z: {:.5f}, T: {:.5f}".format(
                current_time,
                port,
                data_0[port]["A"],
                data_0[port]["P"],
                data_0[port]["X"],
                data_0[port]["Y"],
                data_0[port]["Z"],
                data_0[port]["T"],
            )
        )

    motor_control.move_stage_to_angle(instrumentation["Stage"], 0)

    for key in port_dict:
        tumble_matrix_plus[key].append(
            [data_0[key]["X"], data_0[key]["Y"], data_0[key]["Z"]]
        )
        tumble_matrix_minus[key].append(
            [data_180[key]["X"], data_180[key]["Y"], data_180[key]["Z"]]
        )

        # print(f"Mount each sensor in the Z orientation - {specs.mount3}")

    return tumble_matrix_plus, tumble_matrix_minus
