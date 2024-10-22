
import json
from network import api_calls

with open('RUBY_PN_CONSTANTS.json') as RUBY_json:
    preDefinedParts = json.load(RUBY_json)
#part_dict follows the structure used by mems linear control table
part_dict = {
    "user": 10,
    "part_no": "dummy",
    "model_no": "dummy",
    "epa_no": None,
    "eco_no": None,
    "revision": "1",
    "production_ready": True,
    "is_digital": False,
    "in_use": True,
    "specs": {
        "sensor_type": "Accelerometer",
        "input_units": "g",
        "output_units": "VDC",
        "output_type": "+/-5 VDC",
        "standards": ["ROHS", "REACH", "CE"],
        "thermal_destress": True,
        "bandwidth": 1000,
        "bandwidth_tolerance_low": 900,
        "bandwidth_tolerance_high": 1100,
        "cycles": [
            "Validate"
        ],
        "soak_time": 1,
        "linearity_points": 11,
        "extra_points": 1,
        "settle_time": 3,
        "num_temps": 1,
        "cal_temps": [22.5],
        "cal_temp_tol": 50.0,
        "verify_temps": [22.5],
        "verify_temp_tol": 50.0,
        "start_stop_step_temps": [-30, 20, 70],
        "override_temp_array": False,
        "test_voltage": 15.0,
        "input_current": 100.0,
        "axes_no": 3,
        "mount": ["connector right", "connector forward", "connector forward"],
        "range": [5],
        "bias": [0.02],
        "scale_factor": [0.0],
        "moa": [0.15],
        "mpa": [0.15],
        "sfts": [150.0],
        "bts": [0.25],
        "hysteresis": [0.07],
        "repeatability": [0.07],
        "accuracy": [0.0],
        "resolution": [0.02],
        "linearity": [0.06]
        },
    "digital": None,
    "physical": {
        "mass": 140.0,
        "mass_units": "grams",
        "shape": "rectangle",
        "seal_rating": "IP67",
        "connector": None
    },
    "tests": {
        "linearity": "Test and Report",
        "test_over_temp": "None",
        "test_bias": "Test and Report",
        "test_hystrs": "None",
        "test_rsltn": "None",
        "test_temp_sensor": "Test and Report",
        "test_rptblty": "None",
        "test_sfts": "None",
        "test_bts": "None",
        "tare": "None",
        "renormalize": False,
        "nist_cal": False
        }
    }

def model_to_dict(part):
    model = preDefinedParts[part]["model"]
    model = model.split("-")
    fro = 0
    #ex "JMHA-100-1-D-10.0" accelerometer, 1 axis, db9, dual +/-5V, 10g
    part_dict["part_no"] = part
    part_dict["model_no"] = preDefinedParts[part]["model"]
    match model[0]:
        case "JMHA":
            part_dict["specs"]["sensor_type"] = "Accelerometer"
            part_dict["specs"]["input_units"] = "g"
            part_dict["specs"]["bandwidth"] = 1000
            part_dict["specs"]["bandwidth_tolerance_low"] = 900
            part_dict["specs"]["bandwidth_tolerance_high"] = 1100
        case "JMHI":
            part_dict["specs"]["sensor_type"] = "Inclinometer"
            part_dict["specs"]["input_units"] = "deg"
            part_dict["specs"]["bandwidth"] = 5
            part_dict["specs"]["bandwidth_tolerance_low"] = 3
            part_dict["specs"]["bandwidth_tolerance_high"] = 7
    match model[1]:
        case "100":
            part_dict["specs"]["axes_no"] = 1
            part_dict["specs"]["mount"] = ["connector right"]
        case "200":
            part_dict["specs"]["axes_no"] = 2
            part_dict["specs"]["mount"] = ["connector right", "connector forward"]
        case "300":
            part_dict["specs"]["axes_no"] = 3
            part_dict["specs"]["mount"] = ["connector right", "connector forward", "connector forward"]
    match model[2]:
        case "1":
            part_dict["physical"]["connector"] = 4
        case "4":
            part_dict["physical"]["connector"] = 5
    match model[3]:
        case "D":
            part_dict["specs"]["output_units"] = "VDC"
            part_dict["specs"]["output_type"] = "+/-5 VDC"
            fro = 10
        case "S":
            part_dict["specs"]["output_units"] = "VDC"
            part_dict["specs"]["output_type"] = "0-5 VDC"
            fro = 5
        case "L":
            part_dict["specs"]["output_units"] = "mA"
            part_dict["specs"]["output_type"] = "4-20mA"
            fro = 16
    match model[4]:
        case _:
            part_dict["specs"]["range"] = [float(model[4])]
            part_dict["specs"]["scale_factor"] = [str(fro / float(model[4]))]
    return

def main():
    handler = api_calls.APIHandler(login_email="ngreen@jewellinstruments.com", login_pass="M0ldraxian")
    if(handler.login()):
        for i in preDefinedParts:
            model_to_dict(i)
            response = handler.post("mems_linear_control/?detailed=True", part_dict)
            print(response)
    return


if __name__ == "__main__":
    main()