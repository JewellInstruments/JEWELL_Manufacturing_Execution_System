import random
import time
import logging

from system import countdown
from system import serial_protocols
from system import settings

from instrumentation import data_aq_read


def ramp_to_temp(
    chamber_port: serial_protocols.socket_open,
    data_aq_port: serial_protocols.serial_open,
    temp: float,
    temp_tol: float,
) -> None:
    """_summary_

    Args:
        chamber_port (serial_protocols.socket_open): _description_
        data_aq_port (serial_protocols.serial_open): _description_
        temp (float): _description_
        temp_tol (float): _description_
    """

    print(f"\nRamping to {temp} C")

    current_temp = 22.5
    return

    while True:
        if temp < current_temp:
            current_temp = current_temp - 2 * random.random()
        else:
            current_temp = current_temp + 2 * random.random()

        if abs(current_temp - temp) < temp_tol:
            break

        set_chamber_set_point(chamber_port, 22.5)
        current_temp = data_aq_read.get_plate_temp(data_aq_port, spoof_temp=temp)

        print(
            "Plate Temp 1: {:.2f} C, Plate Temp 2: {:.2f} C".format(
                current_temp, current_temp
            ),
            end="\r",
        )
        time.sleep(0.1)

    return


def soak_at_temp(
    chamber_port: serial_protocols.socket_open,
    data_aq_port: serial_protocols.serial_open,
    temp: float,
    soak_time: float,
    temp_tol: float,
) -> None:
    """_summary_

    Args:
        chamber_port (serial_protocols.socket_open): _description_
        data_aq_port (serial_protocols.serial_open): _description_
        temp (float): _description_
        soak_time (float): _description_
        temp_tol (float): _description_
    """

    print(f"\nSoaking at {temp} C for {soak_time} min")

    current_temp = data_aq_read.get_plate_temp(data_aq_port)

    if (current_temp - temp) > temp_tol:
        print("We are out of temp tol")
        set_chamber_set_point(chamber_port, temp)

    countdown.countdown(soak_time * 60)

    return


def set_chamber_set_point(
    chamber_port: serial_protocols.socket_open, set_point: float
) -> None:
    """set the chamber temperature in C.

    Args:
        chamber_port (serial_protocols.socket_open): _description_
        set_point (float): temperature to go to in C
    """

    if settings.CHAMBER_COMS_TYPE == "TCP/IP":
        serial_protocols.socket_write(chamber_port, f"SOURce:CLOop1:SPOint {set_point}")
    else:
        error_message = f"Chamber Communication type {settings.CHAMBER_COMS_TYPE} not setup at this time."
        print(error_message)
        logging.error(settings.CHAMBER_COMS_TYPE)
    set_point = read_chamber_set_point(chamber_port)

    return


def read_chamber_set_point(chamber_port: serial_protocols.socket_open) -> float:
    """_summary_

    Args:
        chamber_port (serial_protocols.socket_open): _description_

    Returns:
        float: chamber current set point in C
    """

    if settings.CHAMBER_COMS_TYPE == "TCP/IP":
        serial_protocols.socket_write(chamber_port, "SOURce:CLOop1:SPOint?")
    else:
        error_message = f"Chamber Communication type {settings.CHAMBER_COMS_TYPE} not setup at this time."
        print(error_message)
        logging.error(settings.CHAMBER_COMS_TYPE)
    return serial_protocols.socket_read(chamber_port)


def read_chamber_air_temp(chamber_port: serial_protocols.socket_open) -> float:
    """read the air temperature (C) in the chamber.

    Args:
        chamber_port (serial_protocols.socket_open): _description_

    Returns:
        float: chamber air temp in C
    """
    if settings.CHAMBER_COMS_TYPE == "TCP/IP":
        serial_protocols.socket_write(chamber_port, "SOURCE:CLOOP1:PVALUE?")
    else:
        error_message = f"Chamber Communication type {settings.CHAMBER_COMS_TYPE} not setup at this time."
        print(error_message)
        logging.error(settings.CHAMBER_COMS_TYPE)

    return float(serial_protocols.socket_read(chamber_port))


def read_chamber_identification(chamber_port: serial_protocols.socket_open) -> str:
    """read the identification of the Watow F4T controller on the chamber.
        "Watlow Electric","F4T1L4EAA1H1AAA",38505,"4.08"\n'

    Args:
        chamber_port (serial_protocols.socket_open): _description_

    Returns:
        str: identification string.
    """

    if settings.CHAMBER_COMS_TYPE == "TCP/IP":
        serial_protocols.socket_write(chamber_port, "*IDN?")
    else:
        error_message = f"Chamber Communication type {settings.CHAMBER_COMS_TYPE} not setup at this time."
        print(error_message)
        logging.error(settings.CHAMBER_COMS_TYPE)
    data = serial_protocols.socket_read(chamber_port)
    return data


#############################################################
"""
Old protocols used for the TUJR chambers.

"""


# # setup the chamber serial port

# def _setup_chamber_port():

#     port = instr_settings.instrument_settings.CHAM_COM
#     addr = instr_settings.instrument_settings.CHAM_ADDR
#     baud = instr_settings.instrument_settings.CHAM_BAUD
#     dev = None
#     try:
#         dev = serial_protocols._setup_MODBUS_intsr(port, addr, baud)
#     except Exception as e:
#         logging.warning(e)
#     return dev


# # get the chamber ID (spoofing as of 5/5/22)

# def _get_chamber_ID(dev):

#     serial_num = ""
#     try:
#         serial_num_1 = 1e3*serial_protocols._read_MODBUS_instr(dev, 1)
#         serial_num_2 = 1e3*serial_protocols._read_MODBUS_instr(dev, 2)

#         serial_num = str(serial_num_1) + str(serial_num_2)
#     except Exception as e:
#         logging.warning(e)

#     return serial_num


# # get mean plate temp

# def _get_mean_plate_temp(TempPort):

#     T_chan = None
#     if instr_settings.instrument_settings.USE_NI_USB == True:
#         T_plate_1 = thermometry._read_NI_USB_6510(instr_settings.instrument_settings.dev0)
#         T_plate_2 = thermometry._read_NI_USB_6510(instr_settings.instrument_settings.dev1)
#         T_chan = stats.mean([T_plate_1, T_plate_2])
#     else:
#         T_chan = float(os.environ.get("PLATETEMP"))
#         # thermometry._read_DGH_D5331(TempPort, channels=instr_settings.instrument_settings.NUM_TC)

#     return T_chan


# # read air temp from controller

# def _read_air_temp(dev):

#     Air_temp = 1e3*serial_protocols._read_MODBUS_instr(dev, 100)
#     return Air_temp


# # set the temp on a watlow f4 controller using modbus rtu

# def _set_chamber_set_point(dev, T_set_point):

#     if T_set_point > app_settings.MAX_CHAMBER_TEMP or T_set_point < app_settings.MIN_CHAMBER_TEMP:
#         return 0
#     else:
#         serial_protocols._write_to_MODBUS_instr(dev, 300, T_set_point) # set the current set point
#         time.sleep(0.05)
#         T_sp_ver = 1e3*serial_protocols._read_MODBUS_instr(dev, 300)

#         if T_sp_ver != T_set_point:
#             _set_chamber_set_point(dev, T_set_point)
#             os.environ['ATTEMPTS'] = "{}".format(1+int(os.environ.get('ATTEMPTS')))
#             if int(os.environ.get('ATTEMPTS')) > 3:
#                 return 0
#     return 1


# # get the current set point on the chamber

# def _get_current_set_point(dev):

#     T_sp = 1e3*serial_protocols._read_MODBUS_instr(dev, 300)
#     return T_sp


# # log data to data file with a timestamp

# def _log_data_to_file(file_to_write, string):

#     """
#     inputs:
#         file_to_write -> filepath to write to
#         string -> string to inplant in the file
#     """

#     logging.info("Logging data...")
#     cdt = datetime.datetime.now().strftime("%Y-%d-%m %H:%M:%S")

#     # check if the file exists
#     if os.path.isfile(file_to_write):
#         pass
#     else:
#         # if the file does not exist, write a header
#         with open(file_to_write, "w") as write_file:
#             write_file.write("Timestamp,T Plate (C),Air Temp (C),T Set Point (C),T Next Set Point (C),T avg 0.5 (C),T avg 3.75 (C),T avg 7.5 (C),T avg 15 (C)\n")

#     # open the file and write the string into the
#     with open(file_to_write, "a") as write_file:
#         write_file.write("{},{}".format(cdt, string))


# # thermal stability verification.

# def _check_for_stability(array, T_stable, tol):

#     """
#     Input:
#         array -> array of floats
#         T_stable -> stability point
#         tol -> variance around stability that is acceptable

#     output:
#         1 if stable
#         0 if not stable
#     """

#     diff_T_arr = []
#     for i in range(len(array)):
#         diff_T = abs(array[i] - T_stable)
#         diff_T_arr.append(diff_T)

#     if tol > max(diff_T_arr):
#         return 1
#     else:
#         return 0


# # ramp to a temperature

# def _ramp_protocol(ChamPort, DAQPort, TempPort, ramp_time_sec, T_sp_curr, T_sp_low, T_sp_high, T_sp_mid, T_avg_05_arr, T_avg_375_arr, T_avg_750_arr, T_avg_150_arr):

#     # loop for that time
#     t0_ramp = time.time()
#     t_ramp = 0

#     t0_buffer = time.time()
#     t_buffer = 0

#     if T_sp_curr < T_sp_mid:
#         sign_flag = -1
#     else:
#         sign_flag = 1

#     logging.info("Starting ramp protocol")

#     while t_ramp < abs(ramp_time_sec):

#         T_sp_next = T_sp_curr - 1.0

#         # write to the controller
#         set_temp_flag = _set_chamber_set_point(ChamPort, T_sp_next)
#         if set_temp_flag == 0:
#             # _chamber_shut_down()
#             return

#         T_sp_curr = T_sp_next

#         logging.info("Settings set point to: {} C".format(T_sp_curr))

#         T_air = _read_air_temp(ChamPort)

#         t_buffer = 0
#         t0_buffer = time.time()
#         while t_buffer < 60:

#             try:
#                 # get plate temp and capture
#                 if (app_settings.__TEST_MODE__):
#                     T_plate = T_sp_curr + 0.1*random.random()
#                 else:
#                     T_plate = _get_mean_plate_temp(TempPort)

#                 T_avg_05, T_avg_05_arr = num_meths._moving_average_filter(T_avg_05_arr, T_plate, app_settings.size_05)
#                 T_avg_375, T_avg_375_arr = num_meths._moving_average_filter(T_avg_375_arr, T_plate, app_settings.size_375)
#                 T_avg_750, T_avg_750_arr = num_meths._moving_average_filter(T_avg_750_arr, T_plate, app_settings.size_750)
#                 T_avg_150, T_avg_150_arr = num_meths._moving_average_filter(T_avg_150_arr, T_plate, app_settings.size_150)

#                 # log data
#                 write_data = app_settings.str_to_write.format(
#                                         T_plate,
#                                         T_air,
#                                         T_sp_curr,
#                                         T_sp_next,
#                                         T_avg_05,
#                                         T_avg_375,
#                                         T_avg_750,
#                                         T_avg_150
#                                     )

#                 _log_data_to_file(app_settings.file, write_data)
#                 time.sleep(app_settings.log_buffer_time) # sleep for 5 seconds

#                 logging.info("Running for: {:.2f}/{:.2f}\n".format(t_ramp, abs(ramp_time_sec)))

#                 t_ramp = time.time() - t0_ramp
#             except KeyboardInterrupt:
#                 t_ramp = abs(ramp_time_sec) + 1
#                 break
#             except Exception as e:
#                 logging.warning(e)

#             t_buffer = time.time() - t0_buffer

#         if sign_flag == -1:
#             if T_avg_05 < T_sp_low:
#                 break
#         else:
#             if T_avg_05 < T_sp_high:
#                 break

#     return T_avg_05_arr, T_avg_375_arr, T_avg_750_arr, T_avg_150_arr


# # stablize at a temperature after ramping

# def _stablization_protocol(ChamPort, DAQPort, TempPort, T_sp_mid, T_sp_curr, T_avg_05_arr, T_avg_375_arr, T_avg_750_arr, T_avg_150_arr):

#     logging.info("Launching stablization stage...")

#     t_stabe = 0
#     t0_stabe = time.time()
#     stable_flag = 0

#     t_adjustment = 0
#     t0_adjustment = time.time()

#     T_sp_next = T_sp_curr

#     while stable_flag == 0:

#         try:
#             # get plate temp
#             T = 0

#             logging.info("Checking stability")
#             stable_flag = _check_for_stability(T_avg_150_arr, T_sp_mid, app_settings.temp_tol_band)

#             t_adjustment = time.time() - t0_adjustment

#             T_sp_curr = _get_current_set_point(ChamPort)

#             T_sp_next = T_sp_curr

#             if t_adjustment > app_settings.adjustmen_time:

#                 logging.info("Makinging adjustment to set point...")
#                 T_sp_next = T_sp_curr - (T_avg_375 - T_sp_mid)

#                 # write T_sp_next to controller
#                 set_temp_flag = _set_chamber_set_point(ChamPort, T_sp_next)
#                 if set_temp_flag == 0:
#                     # _chamber_shut_down()
#                     return

#                 T_sp_curr = T_sp_next

#                 t_adjustment = 0
#                 t0_adjustment = time.time()

#             T_air = _read_air_temp(ChamPort)


#             # get plate temp and capture
#             if (app_settings.__TEST_MODE__):
#                 T_plate = T_sp_curr + 0.1*random.random()
#             else:
#                 T_plate = _get_mean_plate_temp(TempPort)
#             T_avg_05, T_avg_05_arr = num_meths._moving_average_filter(T_avg_05_arr, T_plate, app_settings.size_05)
#             T_avg_375, T_avg_375_arr = num_meths._moving_average_filter(T_avg_375_arr, T_plate, app_settings.size_375)
#             T_avg_750, T_avg_750_arr = num_meths._moving_average_filter(T_avg_750_arr, T_plate, app_settings.size_750)
#             T_avg_150, T_avg_150_arr = num_meths._moving_average_filter(T_avg_150_arr, T_plate, app_settings.size_150)

#             # log data

#             write_data = app_settings.str_to_write.format(
#                                     T_plate,
#                                     T_air,
#                                     T_sp_curr,
#                                     T_sp_next,
#                                     T_avg_05,
#                                     T_avg_375,
#                                     T_avg_750,
#                                     T_avg_150
#                                 )

#             _log_data_to_file(app_settings.file, write_data)

#             time.sleep(app_settings.log_buffer_time) # sleep for 5 seconds
#         except KeyboardInterrupt:
#             break
#         except Exception as e:
#             print(e)
#             break

#     return T_avg_05_arr, T_avg_375_arr, T_avg_750_arr, T_avg_150_arr


# # move to a temp.

# def _move_to_temperature(ChamPort, DAQPort, TempPort, temp, temp_tol, rate):

#     """
#     inputs:
#         ChamPort -> chamber communication, serial object
#         temp -> temp to achieve, double (C)
#         temp_tol -> acceptance interval, tuple of floats (low, high) (C)
#         rate -> rate at which to ramp the chamber, float (C/min)
#     returns:
#         T_avg_05_arr, T_avg_375_arr, T_avg_750_arr, T_avg_150_arr
#     """

#     # initialization of local vars
#     T_plate = 0. # instaneous plate temp (C)
#     T_sp_curr = 0. # current set point (C)
#     T_sp_next = 0. # next set point (C)

#     T_avg_05, T_avg_05_arr = 0., [] # running average value (C) and array for 0.5 min
#     T_avg_375, T_avg_375_arr = 0., [] # running average value (C) and array for 3.75 min
#     T_avg_750, T_avg_750_arr = 0., [] # running average value (C) and array for 7.5 min
#     T_avg_150, T_avg_150_arr = 0., [] # running average value (C) and array for 15 min

#     delta_T = abs(temp_tol[1] - temp_tol[0])

#     T_sp_low = temp - abs(temp_tol[0])
#     T_sp_high = temp + abs(temp_tol[1])
#     T_sp_mid = (T_sp_high + T_sp_low)/2.

#     # get the current set point
#     T_sp_curr = _get_current_set_point(ChamPort)

#     # calculate how long to run for.
#     ramp_time_sec = (T_sp_mid - T_sp_curr)*60/rate # time in seconds

#     # determine whether a positive or negative shift is needed
#     if ramp_time_sec < 0:
#         direction_value = -1
#     else:
#         direction_value = 1

#     if T_sp_mid < 0:
#         scaling = 3.
#         T_sp_overshoot = T_sp_low - scaling*delta_T
#     else:
#         scaling = 2.
#         if direction_value < 0:
#             T_sp_overshoot = T_sp_low - scaling*delta_T
#         else:
#             T_sp_overshoot = T_sp_high + scaling*delta_T

#     print("SP Low: {}".format(T_sp_low))
#     print("SP High: {}".format(T_sp_high))
#     print("SP Mid: {}".format(T_sp_mid))
#     print("SP Overshoot: {}".format(T_sp_overshoot))
#     print("Ramp time in min: {}".format(abs(ramp_time_sec/60)))
#     print("")

#     ##########################################
#     # RAMP STAGE

#     T_avg_05_arr, T_avg_375_arr, T_avg_750_arr, T_avg_150_arr = _ramp_protocol(ChamPort, DAQPort, TempPort, ramp_time_sec, T_sp_curr, T_sp_low, T_sp_high, T_sp_mid, T_avg_05_arr, T_avg_375_arr, T_avg_750_arr, T_avg_150_arr)

#     ##########################################

#     ##########################################
#     # STABLIZATION STAGE

#     TT_avg_05_arr, T_avg_375_arr, T_avg_750_arr, T_avg_150_arr = _stablization_protocol(ChamPort, DAQPort, TempPort, T_sp_mid, T_sp_curr, T_avg_05_arr, T_avg_375_arr, T_avg_750_arr, T_avg_150_arr)

#     ##########################################

#     logging.info("Plate temp is stable")
#     return T_avg_05_arr, T_avg_375_arr, T_avg_750_arr, T_avg_150_arr


# # soak at a temp for some time

# def soak_at_temp(ChamPort, DAQPort, TempPort, temp, temp_tol, soak_time, T_avg_05_arr, T_avg_375_arr, T_avg_750_arr, T_avg_150_arr):

#     """
#     soak at a temperature
#     """

#     ##########################################
#     # INITIALIZATION OF LOCAL VARS

#     T_plate = 0. # instaneous plate temp (C)
#     T_sp_next = T_sp_curr

#     delta_T = abs(temp_tol[1] - temp_tol[0])

#     T_sp_low = temp - abs(temp_tol[0])
#     T_sp_high = temp + abs(temp_tol[1])
#     T_sp_mid = (T_sp_high + T_sp_low)/2.

#     if T_sp_mid < 0:
#         scaling = 3.
#         T_sp_overshoot = scaling*delta_T - T_sp_low
#     else:
#         scaling = 2.
#         T_sp_overshoot = scaling*delta_T + T_sp_high

#     ##########################################

#     ##########################################
#     # SOAK STAGE

#     t_soak = 0
#     t0_soak = time.time()

#     t_adjustment = 0
#     t0_adjustment = time.time()

#     logging.info("Starting soak for {} min".format(soak_time/60))
#     while t_soak < soak_time:

#         t_adjustment = time.time() - t0_adjustment

#         T_sp_curr = _get_current_set_point(ChamPort)

#         T_sp_next = T_sp_curr

#         if t_adjustment > app_settings.adjustmen_time:

#             T_sp_next = T_sp_curr - (T_avg_375 - T_sp_mid)

#             # write T_sp_next to controller
#             set_temp_flag = _set_chamber_set_point(ChamPort, T_sp_next)
#             if set_temp_flag == 0:
#                 # _chamber_shut_down()
#                 return

#             T_sp_curr = T_sp_next

#             # reset the timers
#             t_adjustment = 0
#             t0_adjustment = time.time()

#         # get plate temp and capture
#         if (app_settings.__TEST_MODE__):
#             T_plate = T_sp_curr + 0.1*random.random()
#         else:
#             T_plate = _get_mean_plate_temp(TempPort)

#         T_avg_05, T_avg_05_arr = num_meths._moving_average_filter(T_avg_05_arr, T_plate, app_settings.size_05)
#         T_avg_375, T_avg_375_arr = num_meths._moving_average_filter(T_avg_375_arr, T_plate, app_settings.size_375)
#         T_avg_750, T_avg_750_arr = num_meths._moving_average_filter(T_avg_750_arr, T_plate, app_settings.size_750)
#         T_avg_150, T_avg_150_arr = num_meths._moving_average_filter(T_avg_150_arr, T_plate, app_settings.size_150)

#         T_air = _read_air_temp(ChamPort)

#         # log data
#         write_data = app_settings.str_to_write.format(
#                                 T_plate,
#                                 T_air,
#                                 T_sp_curr,
#                                 T_sp_next,
#                                 T_avg_05,
#                                 T_avg_375,
#                                 T_avg_750,
#                                 T_avg_150
#                             )

#         _log_data_to_file(app_settings.file, write_data)

#         time.sleep(app_settings.log_buffer_time) # sleep for 5 seconds

#     ##########################################

#     return T_avg_05_arr, T_avg_375_arr, T_avg_750_arr, T_avg_150_arr
