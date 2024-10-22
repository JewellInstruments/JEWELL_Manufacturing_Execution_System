from analytics import analyze_cal_data

from control import jmx_calibration

from instrumentation import data_aq_init

from network import commit_calibration_data
from network import get_specs


def jmx_atp(
    specs: get_specs.mems_specs, unit_id_dict: dict, instrumentation: dict
) -> None:  # noqa: E501
    """acceptance testing protocol for the jdx sub assembly.

    Args:
        specs (get_specs.mems_specs): _description_
        unit_id_dictL (dict): _description_
        instrumentation (dict): _description_
    """

    mode = "Current" if specs.output_type == "jmx_current" else "Voltage"
    channels = len(unit_id_dict)
    data_aq_init.config_data_aq_for_voltage(
        instrumentation["DataAq"], mode=mode, channels=channels
    )

    jmx_calibration.analog_mems_calibration(
        specs, instrumentation, unit_id_dict, axis_override=0
    )

    # publish calibration charts if they passed all analysis metrics.
    print("Publishing calibration records to api")
    commit_calibration_data.publish_calibration_data(specs, unit_id_dict)

    # analyze data. There is a standard analysis method detailed in doc <>.
    analyze_cal_data.analyze_jmx_calibration_data(specs, unit_id_dict)
