from analytics import analyze_cal_data

from control import jdx_calibration

# from control import jdx_tumble_calibration

from instrumentation import data_aq_init
from instrumentation import motor_control

# from network import commit_calibration_data
from network import get_specs


def jdx_atp(
    specs: get_specs.mems_specs, unit_id_dict: dict, instrumentation: dict
) -> None:  # noqa: E501
    """acceptance testing protocol for the jdx sub assembly.

    Args:
        specs (get_specs.mems_specs): class object containing all the product definitions and testing parameters
        unit_id_dict (dict): a dict with the port_x as the key, and unit_id, part no, serial no, RMA no in a list as a value.
        instrumentation (dict): dict with all the active instrumentation connections.
    """

    # configure the data acquisition system for thermometry.
    data_aq_init.config_data_aq_for_temp(
        instrumentation["DataAq"], full_setup=True, thermistor=False
    )

    motor_control.move_stage_to_angle(instrumentation["Stage"], 0)

    # open serial ports to the units under test.
    active_ports = jdx_calibration.configure_jdx(
        specs, unit_id_dict, "Temp Test", sensor_class_code=10
    )

    # start the tumble calibration.
    # jdx_tumble_calibration.jdx_tumble_calibration(
    #     specs, active_ports, instrumentation, unit_id_dict
    # )

    # start the atp protocol for jdi/jda.
    jdx_calibration.digital_mems_calibration(
        specs, unit_id_dict, active_ports, instrumentation
    )
    return

    # publish calibration charts if they passed all analysis metrics.
    # commit_calibration_data.publish_calibration_data(specs, unit_id_dict)

    # analyze data. There is a standard analysis method detailed in doc <>.
    # analyze_cal_data.analyze_jdx_calibration_data(specs, unit_id_dict)


def jdx_linearity_verification(
    specs: get_specs.mems_specs, unit_id_dict: dict, instrumentation: dict
) -> None:
    """_summary_

    Args:
        specs (get_specs.mems_specs): class object containing all the product definitions and testing parameters
        unit_id_dict (dict): a dict with the port_x as the key, and unit_id, part no, serial no, RMA no in a list as a value.
        instrumentation (dict): dict with all the active instrumentation connections.
    """

    jdx_calibration.initialize_calibration_data_file(unit_id_dict, specs)

    active_ports = jdx_calibration.configure_jdx(specs, unit_id_dict, "Linearity", 52)

    motor_control.move_stage_to_angle(instrumentation["Stage"], 0)

    for axis in range(specs.axes_no + 1):
        jdx_calibration.cycle_through_angles(
            specs, unit_id_dict, active_ports, instrumentation, axis, cycle=2, temp=2
        )

        motor_control.move_stage_to_angle(instrumentation["Stage"], 0)
        if axis != specs.axes_no:
            jdx_calibration.reset_axis("Y Axis", instrumentation)

    analyze_cal_data.analyze_jdx_calibration_data(specs, unit_id_dict, "Verification")
