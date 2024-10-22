import logging
import sys
import time

from system import serial_protocols


def get_position_data_from_jdx(
    port: serial_protocols.serial_open, dummy_angle: float = 0
) -> tuple[float, float, float, float]:
    """_summary_

    Args:
        port (serial_protocols.serial_open): _description_
        dummy_angle (float, optional): _description_. Defaults to 0.

    Returns:
        tuple[float, float, float, float]: _description_
    """

    x = 0.0
    y = 0.0
    z = 0.0
    t = 0.0

    try:
        data = serial_protocols.serial_write_read(port, ";000,v,v\r\n", use_visa=False)
        time.sleep(0.05)
        # print(data)
        data = data.rstrip().replace("+", "").split(",")

        # data = [dummy_angle + random.randint(-10, 10)/1000. for _ in range(3)]

        sensor_type = data[2]

        x = float(data[3])
        if sensor_type == "52":
            y = float(data[4])
            t = float(data[5])
        elif sensor_type == "R":
            y = float(data[4])
            z = float(data[5])
            t = float(data[5])
        else:
            z = float(data[5])
            t = float(data[6])

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        err = f"Error occurred at {exc_tb.tb_lineno} - {e}"
        print(err)
        logging.warning(err)

    return x, y, z, t


def unlock_jdx(port: serial_protocols.serial_open) -> None:
    """_summary_

    Args:
        port (serial_protocols.serial_open): _description_
    """

    try:
        print("Unlocking JDx...")

        unlock_cmd = "<733G3ND4RY>"  # consider pulling this from the database.

        data = serial_protocols.serial_write_read(
            port, f";000,{unlock_cmd}\r\n", use_visa=False
        )
        time.sleep(0.25)
        data = data.rstrip().replace("+", "").split(",")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()

        err = f"Error occurred at {exc_tb.tb_lineno} - {e}"
        print(err)

        logging.warning(err)


def set_decimation(port: serial_protocols.serial_open, decimation: int) -> None:
    """_summary_

    Args:
        port (serial_protocols.serial_open): _description_
        decimation (int): _description_
    """

    try:
        print("Setting decimation for JDx...")

        data = serial_protocols.serial_write_read(
            port, f";000,d,{decimation}\r\n", use_visa=False
        )
        time.sleep(0.25)
        data = data.rstrip().replace("+", "").split(",")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e)

        logging.warning(e)


def turn_streaming_off(port: serial_protocols.serial_open) -> None:
    """_summary_

    Args:
        port (serial_protocols.serial_open): _description_
    """

    try:
        print("Turning Streaming off...")

        data = serial_protocols.serial_write_read(port, ";000,s,0\r\n", use_visa=False)
        time.sleep(0.25)
        data = data.rstrip().replace("+", "").split(",")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e)

        logging.warning(e)


def set_identity_matrix(port: serial_protocols.serial_open) -> None:

    try:
        print("Setting to all comps off...")

        data = serial_protocols.serial_write_read(
            port, ";000,m,e,!\r\n", use_visa=False
        )
        time.sleep(0.25)
        data = data.rstrip().replace("+", "").split(",")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e)

        logging.warning(e)


def set_factory_personality(port: serial_protocols.serial_open) -> None:
    """_summary_

    Args:
        port (serial_protocols.serial_open): _description_
    """

    try:
        print("Settings factory personality...")

        data = serial_protocols.serial_write_read(port, ";000,p,0\r\n", use_visa=False)
        time.sleep(0.25)
        data = data.rstrip().replace("+", "").split(",")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e)

        logging.warning(e)


def set_output(port: serial_protocols.serial_open, sensor_class_code: int) -> None:
    """_summary_

    Output / Style Code	Description
    0	Acceleration Only
    1	Simple, Flat
    2	Simple Wall Y (Y axis points up)
    3	Simple Wall X (X axis points up)
    4	Complex Flat Phi  Z
    5	Complex Wall Phi  Y
    6	Complex Wall Phi  X
    7	Direct Angular Floor  Z
    8	Direct Angular Wall  Y
    9	Direct Angular Wall  X
    10	Raw ADC Sample Counts**
    11	Raw and Flat
    20	JDA 1-Axis Y
    21	JDA 1-Axis Z
    22	JDI 1-Axis Y
    23	JDI 1-Axis Z
    41	JDA 1-Axis X
    42	JDA 2-Axis
    43	JDA 3-Axis
    50	JDx ALL  (Not sure what this is)
    51	JDI 1-Axis X
    52	JDI 2-Axis X,Y
    53	JDI 3-Axis X,Y,Z



    Args:
        port (serial_protocols.serial_open): _description_
    """

    try:
        print("Setting output...")

        data = serial_protocols.serial_write_read(
            port, f";000,m,o,{sensor_class_code}\r\n", use_visa=False
        )
        time.sleep(0.25)
        data = data.rstrip().replace("+", "").split(",")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e)

        logging.warning(e)


def set_output_bandwidth(port: serial_protocols.serial_open, bandwidth: int) -> None:
    """_summary_

    Args:
        port (serial_protocols.serial_open): _description_
        bandwidth (int): _description_
    """

    try:
        print(f"Setting bandwidth to {bandwidth}...")

        data = serial_protocols.serial_write_read(
            port, f";000,m,{bandwidth}\r\n", use_visa=False
        )
        time.sleep(0.25)
        data = data.rstrip().replace("+", "").split(",")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e)

        logging.warning(e)


def set_RS485_termination(port: serial_protocols.serial_open) -> None:
    """_summary_

    Args:
        port (serial_protocols.serial_open): _description_
    """

    try:
        print("Setting RS485 termination off...")

        data = serial_protocols.serial_write_read(port, ";000,X,0\r\n", use_visa=False)
        time.sleep(0.25)
        data = data.rstrip().replace("+", "").split(",")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e)

        logging.warning(e)


def nonvolatile_save(port: serial_protocols.serial_open) -> None:
    """_summary_

    Args:
        port (serial_protocols.serial_open): _description_
    """

    try:
        print("Saving...")

        data = serial_protocols.serial_write_read(port, ";000,N,S\r\n", use_visa=False)
        time.sleep(0.25)
        data = data.rstrip().replace("+", "").split(",")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e)

        logging.warning(e)


def turn_off_self_test(port: serial_protocols.serial_open) -> None:
    """_summary_

    Args:
        port (serial_protocols.serial_open): _description_
    """

    try:
        print("Turning self test off...")

        data = serial_protocols.serial_write_read(port, ";000,T,0\r\n", use_visa=False)
        time.sleep(0.25)
        data = data.rstrip().replace("+", "").split(",")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e)

        logging.warning(e)


def clear_faults(port: serial_protocols.serial_open) -> None:
    """_summary_

    Args:
        port (serial_protocols.serial_open): _description_
    """

    try:
        print("Clearing faults...")

        data = serial_protocols.serial_write_read(port, ";000,c,f\r\n", use_visa=False)
        time.sleep(0.25)
        data = data.rstrip().replace("+", "").split(",")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e)

        logging.warning(e)


def set_verbosity(port: serial_protocols.serial_open) -> None:
    """_summary_

    Args:
        port (serial_protocols.serial_open): _description_
    """

    try:
        print("Setting verbosity...")

        data = serial_protocols.serial_write_read(port, ";000,|,1\r\n", use_visa=False)
        time.sleep(0.25)
        data = data.rstrip().replace("+", "").split(",")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e)

        logging.warning(e)


def erase_lut(port: serial_protocols.serial_open) -> None:
    """_summary_

    Args:
        port (serial_protocols.serial_open): _description_
    """

    try:
        print("Erasing LUT...")

        data = serial_protocols.serial_write_read(
            port, ";000,M,-,0\r\n", use_visa=False
        )
        time.sleep(0.25)
        data = data.rstrip().replace("+", "").split(",")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e)

        logging.warning(e)


def soft_reset(port: serial_protocols.serial_open) -> None:
    """_summary_

    Args:
        port (serial_protocols.serial_open): _description_
    """

    try:
        print("Resetting MCU...")

        data = serial_protocols.serial_write_read(
            port, ";000,>shutdown -r now\r\n", use_visa=False
        )

        time.sleep(0.25)
        data = data.rstrip().replace("+", "").split(",")
        time.sleep(0.05)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e)
        logging.warning(e)


def set_lut_table_record(
    port: serial_protocols.serial_open,
    axis: int,
    temp_idx: int,
    counts: int,
    angle: float,
) -> None:
    """_summary_

    Args:
        port (serial_protocols.serial_open): _description_
        file (str): _description_
    """
    try:
        print(f"Settings LUT record on {port.port}...")

        lut_idx = 1

        cmd = ";000,M,T,{},{},{},{:.0f},{:.5f}\r\n".format(
            axis, temp_idx, lut_idx, counts, angle
        )

        data = serial_protocols.serial_write_read(port, cmd)
        time.sleep(0.25)
        data = data.rstrip().replace("+", "").split(",")

        """

		response has ERROR, check command.

		"""

        time.sleep(0.05)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(e)

        logging.warning(e)


def load_lut_table_to_sensor(port: serial_protocols.serial_open, file: str) -> None:
    """_summary_

    Args:
        port (serial_protocols.serial_open): _description_
        file (str): _description_
    """

    with open(file, "r") as read_file:
        contents = read_file.readlines()

    axis_idx = 0

    for line in contents:
        record = line.rstrip().split(",")

        axis_idx = record[0]

        if record[1] == 0:  # lut cycle.
            temp_idx = record[2]

            angle = record[3]

            if axis_idx == 0:
                counts = record[4]

            elif axis_idx == 1:
                counts = record[5]

            elif axis_idx == 2:
                counts = record[6]

            set_lut_table_record(port, axis_idx, temp_idx, counts, angle)
    set_output(port, sensor_class_code=52)


def load_tumble_data_to_sensor(
    port: serial_protocols.serial_open, cal_matrix: list, offset_matrix: list
) -> None:
    """_summary_

    Args:
        port (serial.serial_open): _description_
        cal_matrix (list): _description_
    """

    print("Uploading calibration coefficients to sensor")

    for index in range(3):

        data = serial_protocols.serial_write_read(
            port,
            f";000,M,A,{index},{cal_matrix[index][0]},{cal_matrix[index][1]},{cal_matrix[index][2]}\r\n",
            use_visa=False,
        )
        time.sleep(0.15)
        data = data.rstrip().replace("+", "").split(",")

    data = serial_protocols.serial_write_read(
        port,
        f";000,M,B,{offset_matrix[0]},{offset_matrix[1]},{offset_matrix[2]}\r\n",
        use_visa=False,
    )
    time.sleep(0.15)
    data = data.rstrip().replace("+", "").split(",")
