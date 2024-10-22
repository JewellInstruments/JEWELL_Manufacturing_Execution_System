import datetime
import json
import logging
import os
import sys
import socket


from system import version

# from system import log_config

from network import filesystem


#####################################################################################################################
# GLOBAL SETTINGS

__PROGRAM_NAME__ = "MEMs ATP Program"

__VERSION__ = version.__VERSION__

__AUTHOR__ = "Jewell Instruments LLC"

DATETIME_STR = "%Y-%m-%d %H:%M:%S"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

HOST_NAME = socket.gethostname()

LOG_LEVEL = logging.DEBUG
LOG_DATE_TIME = "%Y%m%d%H%M%S"
HOME_PATH = os.path.expanduser("~")
LOG_ID = datetime.datetime.now().strftime("%Y%m%d%H%M%S")


filesystem.init_directory(f"{HOME_PATH}\\{HOST_NAME}\\log_{LOG_ID}")

date_time = datetime.datetime.now().strftime(LOG_DATE_TIME)
log_file = os.path.join(f"{HOME_PATH}\\{HOST_NAME}\\log_{LOG_ID}", f"log_{date_time}")

log_format = "%(asctime)s (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"

logging.basicConfig(
    filename=os.path.join(log_file, "error.log"), level=LOG_LEVEL, format=log_format
)

logging.getLogger(__name__).addHandler(logging.StreamHandler(sys.stdout))

DATA_DIRECTORY_ROOT = "X:\\Production\\MEMs Sensors\\MEMS_SHIPPING_RECORDS"

MASTER_JSON_DIR = "X:\\Engineering\\Software\\Production_Software_settings"
master_sys_config_file = os.path.join(MASTER_JSON_DIR, "Master_Config", "master.json")
with open(master_sys_config_file, "r") as file:
    master_json_data = json.load(file)

# API_URL = "http://qed8:8000/api/"
# M2M_API_URL = "http://qed8:8001/api/"

API_URL = "http://192.168.3.11/api"
M2M_API_URL = "http://192.168.3.11/api/"

os.environ["API_USER"] = "ljameson@jewellinstruments.com"
os.environ["API_PASSWORD"] = "Jed1Mast3r97!"

# write a small util function to try to write, if fails, refesh auth token, if that all fails, log in.


TERMINAL_SPACER = 40 * "#" + "\n"

# MASTER CONFIGURATION
######################################################################################

EMAIL_HOST = master_json_data["EMAIL_HOST"]
EMAIL_PORT = master_json_data["EMAIL_PORT"]
QA_EMAIL = master_json_data["QUALITY_EMAIL"]

STOCK_JOBS_ROOT = master_json_data["STOCK_JOBS_DATA_REPO_NAME"]

#####################################################################################################################


# WINDOW SETTINGS
#####################################################################################################################

# setup where the program will get the source files for the windows

EXE_BASE_PATH = "C:\\Program Files (x86)\\{0}\\{0}\\".format(__PROGRAM_NAME__)
SYST_BASE_PATH = "C:\\WINDOWS\\system32"
TEST_BASE_PATH = (
    "X:\\Engineering\\Software\\Production_Software_Source_Code\\MEMs_ATP_Program"
)

base_path = os.getcwd()
logging.info(base_path)
base = ""
base = EXE_BASE_PATH if base_path == SYST_BASE_PATH else base_path
logging.info(base)
WINDOWS_BASE = os.path.join(base, "window")
WINDOW_FILEPATH = os.path.join(WINDOWS_BASE, "main_window", "main_window.ui")
MANUAL_STAGE_WINDOW_FILEPATH = os.path.join(
    WINDOWS_BASE, "manual_stage_control", "manual_stage_control.ui"
)
# MODULE_CAL_ICON_PATH = os.path.join(base, "icon.ico")
LOGO_SOURCE = os.path.join(base, "Jewell_Instruments_Logo.png")

TUTORIALS_ROOT = ""

#####################################################################################################################


# EMAIL SETTINGS
#####################################################################################################################

EMAIL_HOST = "d190768a.ess.barracudanetworks.com"
EMAIL_PORT = 25
# notify IT before using email addr.
# IT needs to activate and let the email server know the email is valid
# __EMAIL__ = f"{__STAGE_NAME__}@jewellinstruments.com"
SOFTWARE_ENG_EMAIL = "swengineer@jewellinstruments.com"

#####################################################################################################################

white_text = "\033[00m"
red_text = "\033[91m"
green_text = "\033[92m"


#####################################################################################################################
