import sys
import logging

from mcculw import ul
from mcculw.enums import TempScale

from analytics import statistical_methods


def read_temp_from_channel(channel: int) -> float:
    """read the temp from a single channel. if that doesn't work, leave temp as -999.

    Args:
        channel (int): _description_

    Returns:
        float: _description_
    """
    temp = -999.0
    try:
        temp = ul.t_in(0, channel, TempScale.CELSIUS)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        err = f"Error occurred at {exc_tb.tb_lineno} - {e}"
        print(err)
        logging.warning(err)
    return temp


def get_system_temperatures() -> list[float, float]:
    """Get all the thermometry from Digilent thermometry module.

    Args:

    Returns:
        list: plate temp and pilar temp
    """
    temp_1 = read_temp_from_channel(0)
    temp_2 = read_temp_from_channel(1)
    temp_3 = read_temp_from_channel(2)
    temp_4 = read_temp_from_channel(3)
    temp_5 = read_temp_from_channel(4)
    temp_6 = read_temp_from_channel(5)

    plate_temp = statistical_methods.mean([temp_1, temp_2, temp_3])

    pilar_temp = statistical_methods.mean([temp_4, temp_5, temp_6])

    return plate_temp, pilar_temp
