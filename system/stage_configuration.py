import json
import os

from network import api_calls

from analytics import conversion

__STAGE_NAME__ = api_calls.get_stage_name()

stage_config_data = api_calls.get_stage_configuration()

assets = api_calls.get_equipment_on_stage(__STAGE_NAME__)


# SERIAL_PORT_MAPPER_RS232 = stage_config_data["rs232_ports"]
# SERIAL_PORT_MAPPER_RS485 = stage_config_data["rs485_ports"]
# SERIAL_PORT_MAPPER_RS422 = stage_config_data["rs422_ports"]


SERIAL_PORT_MAPPER_RS232 = {
    "PORT_1": "COM46",
    "PORT_2": "COM33",
    "PORT_3": "COM34",
    "PORT_4": "COM38",
    "PORT_5": "COM45",
    "PORT_6": "COM35",
    "PORT_7": "COM36",
    "PORT_8": "COM37",
}
SERIAL_PORT_MAPPER_RS422 = {
    "PORT_1": "COM31",
    "PORT_2": "COM32",
    "PORT_3": "COM39",
    "PORT_4": "COM44",
    "PORT_5": "COM40",
    "PORT_6": "COM41",
    "PORT_7": "COM42",
    "PORT_8": "COM43",
}

SERIAL_PORT_MAPPER_RS485 = {
    "PORT_1": "COM27",
    "PORT_2": "COM28",
    "PORT_3": "COM24",
    "PORT_4": "COM25",
    "PORT_5": "COM29",
    "PORT_6": "COM30",
    "PORT_7": "COM23",
    "PORT_8": "COM26",
}


# PORT_TO_COM = dict([(value, key) for key, value in SERIAL_PORT_MAPPER_RS232.items()])


field_decoding_file = os.path.join(os.getcwd(), "system", "field_decoding.json")
with open(field_decoding_file, "r") as file:
    field_json_data = json.load(file)


AXES_DECODER = field_json_data["axes"]  # {0: "X", 1: "Y", 2: "Z"}

MOUNTING_DECODER = field_json_data["mounting"]

TEST_NUMBER = "C-{}"

TIMEOUT = 60  # seconds
# Manchester, New Hampshire
latitude = 42.93658100275377  # degrees
height = 170  # meters
# LOCAL_G_VALUE = 9.81
LOCAL_G_VALUE = conversion.local_gravity_correction(latitude, height)  # m/s^2
# print(LOCAL_G_VALUE_)
#####################################################################################################################


# data aq system setup information
#####################################################################################################################

DATA_ATTEMPTS = 5  # number of tries before pausing and asking for help.
DAQ_IDN = "KEITHLEY"  # get from API
DAQ_BAUD = 9600
NUMBER_OF_CARDS = 2
DAQ_TIMEOUT = 10  # seconds
DAQ_ERROR_VALUE = 1e9  # volts
DAQ_PORT = stage_config_data["data_aq_com"]


TEMP_CHAN_PLATE = "119"
TEMP_CHAN_AIR = "120"
TEMP_CHAN = "119"
TEMP_UNITS = "C"
TEMP_PROBE = "T"
TEMP_CJC = "22.5"
NUM_TEMP_CHANS = 2

DIFF_PORT_CONFIG = {
    "PORT_1": ["101", "102", "103"],
    "PORT_2": ["104", "105", "106"],
    "PORT_3": ["107", "108", "109"],
    "PORT_4": ["110", "111", "112"],
    "PORT_5": ["113", "114", "115"],
    "PORT_6": ["116", "117", "118"],
}

SINGLE_PORT_CONFIG = {
    "PORT_1": ["201", "202", "203"],
    "PORT_2": ["204", "205", "206"],
    "PORT_3": ["207", "208", "209"],
    "PORT_4": ["210", "211", "212"],
    "PORT_5": ["213", "214", "215"],
    "PORT_6": ["216", "217", "218"],
}

#####################################################################################################################

# chamber setup information
#####################################################################################################################

CHAMBER_AVAILABLE = stage_config_data["chamber_installed"]
CHAMBER_TCP_ADDR = stage_config_data["chamber_com"]
CHAMBER_TCP_PORT = 5025
ROOM_TEMP = 22.5  # C
CHAMBER_COMS_TYPE = "TCP/IP"  # stage_config_data["chamber_com"]

#####################################################################################################################

# power supply setup information
#####################################################################################################################

DPS_PORT = stage_config_data["supply_com"]
DPS_BAUD = 9600
POWER_SUPPLY = stage_config_data["supply_type"].upper()
CURRENT_POS = 0.8  # A
CURRENT_NEG = 0.8  # A

#####################################################################################################################

# Stage setup information
#####################################################################################################################

STAGE_AXIS = "U"
STAGE_SPEED = 25  # rev/min
REVERSE_POLARITY = False
STAGE_POINTS_TO_READ = 10  # points
STAGE_ACCURACY = stage_config_data["stage_accuracy"]  # degrees
CONTROLLER_TYPE = stage_config_data["stage_type"]
STAGE_BAUD = 9600
STAGE_PORT = stage_config_data["stage_com"]

#####################################################################################################################
