import logging
import math
import sys
import time

from system import serial_protocols
from system import stage_configuration

from analytics import statistical_methods

import automation1


# callable positioning commands and protocols. independent of controller.


def get_position_from_stage(port: serial_protocols.serial_open) -> float:
    """get the current motor position in degrees from the rotary stage or spoof.

    Returns:
            float: outputs the current position of the rotary stage.
    """
    if stage_configuration.CONTROLLER_TYPE == "Automation1":
        position = automation1_read_position(port)
        return statistical_methods.mean(position)
    elif stage_configuration.CONTROLLER_TYPE == "Ensemble":
        return ensemble_read_position(port)


def move_stage_to_angle(port: serial_protocols.serial_open, angle: float) -> float:
    """move the rotary stage to an angle and get the position.

    Args:
            port (serial_protocols.serial_open.connect_usb): serial port object for the rotary stage.
            angle (float): angle to move to in degrees

    Returns:
            float: angle the stage moved and settled at in degrees.
    """  # noqa: E501

    current_angle = None
    if stage_configuration.REVERSE_POLARITY is True:
        angle = -angle

    if stage_configuration.CONTROLLER_TYPE == "Automation1":
        current_angle, angle_uncertainty = automation1_move_to_angle(port, angle)
    elif stage_configuration.CONTROLLER_TYPE == "Ensemble":
        current_angle = ensemble_move_to_angle(port, angle)

    return current_angle


def move_stage_incremental(port: serial_protocols.serial_open, angle: float) -> float:
    """move the rotary stage to an angle and get the position.

    Args:
            port (serial_protocols.serial_open.connect_usb): serial port object for the rotary stage.
            angle (float): angle to move to in degrees

    Returns:
            float: angle the stage moved and settled at in degrees.
    """  # noqa: E501

    current_angle = 0.0
    if stage_configuration.REVERSE_POLARITY is True:
        angle = -angle

    if stage_configuration.CONTROLLER_TYPE == "Automation1":
        current_angle, angle_uncertainty = automation1_move_incremental_angle(
            port, angle
        )
    elif stage_configuration.CONTROLLER_TYPE == "Ensemble":
        current_angle = ensemble_move_incremental(port, angle)
        current_angle = ensemble_read_position(port)

    return current_angle


def define_home(port: serial_protocols.serial_open) -> None:
    if stage_configuration.CONTROLLER_TYPE == "Automation1":
        automation1_define_home(port)
    elif stage_configuration.CONTROLLER_TYPE == "Ensemble":
        ensemble_define_home(port)
    else:
        print("Controller not setup. ")


# Ensemble functions and protocols


def ensemble_move_absolute(port: serial_protocols.serial_open, angle: float) -> None:
    """command stage to angle in degrees.

    Args:
        port (serial_protocols.serial_open): open serial port connection to rotary stage
        angle (float): angle in degrees to move to.
    """
    speed = 20  # revs/sec
    # port.write(f"MOVEABS X {angle} XF {speed}\r\n".encode())
    serial_protocols.serial_write(
        port, f"MOVEABS X {angle} XF {speed}\r\n", use_visa=False
    )

    return


def ensemble_move_incremental(port: serial_protocols.serial_open, angle: float) -> None:
    """command stage to angle in degrees.

    Args:
        port (serial_protocols.serial_open): open serial port connection to rotary stage
        angle (float): angle in degrees to move to.
    """
    speed = 20  # revs/sec
    # port.write(f"MOVEINC X {angle} XF {speed}\r\n".encode())
    serial_protocols.serial_write(
        port, f"MOVEINC X {angle} XF {speed}\r\n", use_visa=False
    )

    return


def ensemble_define_home(port: serial_protocols.serial_open) -> None:
    # port.write("HOME(X)".encode())
    serial_protocols.serial_write(port, "HOME(X)\r\n", use_visa=False)

    return


def ensemble_read_position(port: serial_protocols.serial_open) -> float:
    """read the angle in degrees from the controller.

    Args:
        port (serial_protocols.serial_open): open serial port connection to rotary stage

    Returns:
        float: angle the stage is currently at in degrees.
    """
    try:
        # port.write("PCMD(X)\r\n".encode())
        serial_protocols.serial_write(port, "PCMD(X)\r\n", use_visa=False)
        angle = serial_protocols.serial_read(port, use_visa=False)
        if angle is not None:
            angle = angle.replace("%", "")
            angle = float(angle)
        else:
            angle = math.nan
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logging.warning(f"\t{e} -> Line {exc_tb.tb_lineno}")
        angle = math.nan

    return angle


def ensemble_move_to_angle(port: serial_protocols.serial_open, angle: float) -> float:
    try:
        drive_check = ensemble_move_absolute(port, angle)

        current_angle = ensemble_read_position(port)
        # curr_angle = -curr_angle
        if drive_check == 0:
            return current_angle

        t0 = time.time()
        loop_time = 0
        while (
            loop_time < stage_configuration.TIMEOUT
            and abs(current_angle - angle) >= stage_configuration.STAGE_ACCURACY
        ):  # noqa: E501
            current_angle = ensemble_read_position(port)
            # curr_angle = -curr_angle
            loop_time = time.time() - t0
            if abs(current_angle - angle) > stage_configuration.STAGE_ACCURACY:
                logging.info("Target angle not reached")
            if loop_time > stage_configuration.TIMEOUT:
                logging.info("Timeout reached. ")
            else:
                logging.info("Timeout not reached, Stage is having trouble.")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logging.warning(f"\t{e} -> Line {exc_tb.tb_lineno}")

    return current_angle


# Automation1 functions and protocols


def automation1_read_position(controller: automation1.Controller) -> float:
    num_points = stage_configuration.STAGE_POINTS_TO_READ
    axis = stage_configuration.STAGE_AXIS

    frequency = automation1.DataCollectionFrequency.Frequency1kHz
    data_config = automation1.DataCollectionConfiguration(num_points, frequency)
    # Adding the following signals to be collected on the x-axis
    data_config.axis.add(automation1.AxisDataSignal.PositionCommand, axis)
    data_config.axis.add(automation1.AxisDataSignal.PositionFeedback, axis)
    data_config.axis.add(automation1.AxisDataSignal.PositionError, axis)
    # Adding the time signal from the controller.
    data_config.system.add(automation1.SystemDataSignal.DataCollectionSampleTime)

    controller.runtime.data_collection.start(
        automation1.DataCollectionMode.Snapshot, data_config
    )

    results = controller.runtime.data_collection.get_results(data_config, num_points)

    return results.axis.get(automation1.AxisDataSignal.PositionFeedback, axis).points


def automation1_move_absolute(controller: automation1.Controller, value: float):
    axis = stage_configuration.STAGE_AXIS
    controller.runtime.commands.motion.moveabsolute(
        axis, [value], [stage_configuration.STAGE_SPEED]
    )


def automation1_move_incremental(
    controller: automation1.Controller, value: float
) -> None:
    axis = stage_configuration.STAGE_AXIS
    controller.runtime.commands.motion.moveincremental(
        axis, [value], [stage_configuration.STAGE_SPEED]
    )


def automation1_move_to_angle(
    controller: automation1.Controller, value: float
) -> list[float, float]:
    automation1_move_absolute(controller, value)

    pos_fbk = automation1_read_position(controller)
    current_position = statistical_methods.mean(pos_fbk)

    while abs(value - current_position) > stage_configuration.STAGE_ACCURACY:
        try:
            pos_fbk = automation1_read_position(controller)
            current_position = statistical_methods.mean(pos_fbk)
            time.sleep(0.5)
        except KeyboardInterrupt:
            break

    print(f"Current Motor Position is: {current_position:.6f} (deg)")
    return statistical_methods.mean(
        pos_fbk
    ), statistical_methods.standard_deviation_from_mean(pos_fbk)


def automation1_move_incremental_angle(
    controller: automation1.Controller, value: float
) -> list[float, float]:
    pos_fbk = automation1_read_position(controller)
    current_position = statistical_methods.mean(pos_fbk)
    target_position = current_position + value

    automation1_move_incremental(controller, value)

    while abs(current_position - target_position) > stage_configuration.STAGE_ACCURACY:
        try:
            pos_fbk = automation1_read_position(controller)
            current_position = statistical_methods.mean(pos_fbk)
            time.sleep(0.5)
        except KeyboardInterrupt:
            break

    print(f"Current Motor Position is: {current_position:.6f} (deg)")
    return statistical_methods.mean(
        pos_fbk
    ), statistical_methods.standard_deviation_from_mean(pos_fbk)


def automation1_define_home(controller):
    axis = stage_configuration.STAGE_AXIS
    controller.runtime.commands.motion.home(axis)
