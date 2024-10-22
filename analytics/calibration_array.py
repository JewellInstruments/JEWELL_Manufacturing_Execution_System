import math

def build_calibration_array(input_range: float, points: int, input_type: str) -> list:
    """build the array of points in degrees used for calibration if not specified.

    Args:
        input_range (float): range of the sensor either in g's or degrees.
        points (int): number of calibration points (must be odd and greater than 3)
        input_type (str): either accelerometer or inclinometer,

    Returns:
        list: list of points to move the stage to in degrees
    """
    if (
        input_type == 'accelerometer'
        and input_range > 1
        or input_type not in ['accelerometer', 'inclinometer']
    ):
        return []
    elif input_type == 'accelerometer':
        return  [
            math.degrees(math.asin(-input_range + 2*input_range*i/(points-1)))  \
                for i in range(points)]
    else:
        return  [-input_range + 2*input_range*i/(points-1) for i in range(points)]