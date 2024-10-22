from system import stage_configuration

import automation1


def automation1_configure_stage() -> automation1.Controller.connect_usb:
    """Connect to Aerotech Automation1 controller with USB protocol.

    Returns:
        a1.Controller.connect_usb: Controller object used to send and receive commands.
    """

    axis = stage_configuration.STAGE_AXIS

    controller = automation1.Controller.connect_usb()
    controller.start()

    controller.runtime.commands.motion.enable(axis)

    return controller


def automation1_close_connection(
    controller: automation1.Controller.connect_usb,
) -> None:
    """close connection to automation1 controller.

    Args:
        controller (automation1.Controller.connect_usb): open connection to close
    """
    controller.disconnect()
