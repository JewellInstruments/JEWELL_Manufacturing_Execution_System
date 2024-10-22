from network import api_calls

from analytics import calibration_array


class mems_specs:
    def __init__(self, part_no: str):
        data_basic = api_calls.get_basic_data(part_no)
        data_test = api_calls.get_tests_to_preform(part_no)

        self.part_no = data_basic["part_no"]
        self.model_no = data_basic["model_no"]
        self.sensor_type = data_basic["sensor_type"].lower()
        self.digital_type = data_basic["digital_type"]
        self.output_type = data_basic["output_type"]
        self.input_units = data_basic["input_units"]
        self.output_units = data_basic["output_units"]
        self.thermal_destress = data_basic["thermal_destress"]
        self.cycles = data_basic["cycles"].split(",")
        self.soak_time = data_basic["soaktime"]
        self.linearity_points = data_basic["linpts"]
        self.extra_points = data_basic["extpts"]
        self.settle_time = data_basic["settletime"]
        self.num_temps = data_basic["num_temps"]
        self.cal_temps = data_basic["cal_temps"].split(",")
        self.cal_temp_tol = data_basic["cal_temp_tol"].split(",")
        self.verify_temps = data_basic["verify_temps"].split(",")
        self.verify_temp_tol = data_basic["verify_temp_tol"].split(",")
        self.start_stop_step_temps = data_basic["start_stop_step_temps"]
        self.test_voltage = data_basic["test_voltage"]
        self.input_current = data_basic["input_current"]
        self.baud = data_basic["baud"]
        self.data_bits = data_basic["data_bits"]
        self.stop_bits = data_basic["stop_bits"]
        self.parity = data_basic["parity"]
        self.sample_rate = data_basic["sample_rate"]
        self.filtering = data_basic["filtering"]
        self.linearity = data_basic["linearity"]
        self.axes_no = data_basic["axes_no"]
        self.range = data_basic["range"]
        self.fso = data_basic["fso"]
        self.bias = 0.01  # data_basic["bias"] # there is a bug with the API not setting the bias terms
        self.scale_factor = data_basic["scalefct"]
        self.sf_tol = 0.25
        self.scale_factor_low_limit = data_basic["scalefct"][0] * (1 - self.sf_tol)
        self.scale_factor_high_limit = data_basic["scalefct"][0] * (1 + self.sf_tol)
        self.moa = data_basic["moa"][0]
        self.mpa = data_basic["mpa"][0]
        self.sfts = data_basic["sfts"]
        self.bts = data_basic["bts"]
        self.hysteresis = data_basic["hystrs"]
        self.repeatability = data_basic["rptblty"]
        self.accuracy = data_basic["accy"]
        self.resolution = data_basic["rsltn"]

        self.nominal_ADC = 256000
        # dimensionless, used as a tolerance in the orthonormalization matrix.
        self.orthonormal_element_limit = 0.03  # dimensionless,
        # each non-diagonal element should be with +/-. each diagonal element should be within +/- of 1.

        points = self.linearity_points + 2 * self.extra_points
        self.cal_points_array = calibration_array.build_calibration_array(
            self.range[0], points, self.sensor_type
        )

        self.bandwidth = data_basic["bandwidth"]
        self.bandwidth_tolerance_low = data_basic["bandwidth_tolerance_low"]
        self.bandwidth_tolerance_high = data_basic["bandwidth_tolerance_high"]

        self.test_bias = data_test["test_bias"]
        self.test_linearity = data_test["test_linearity"]
        self.test_pend_axis = data_test["test_pend_axis"]
        self.test_repeatability = data_test["test_rptblty"]
        self.test_hysteresis = data_test["test_hystrs"]
        self.test_resolution = data_test["test_rsltn"]
        self.test_temp = data_test["test_over_temp"]
        self.test_temp_sensor = data_test["test_temp_sensor"]
        self.test_sfts = data_test["test_sfts"]
        self.test_bts = data_test["test_bts"]
        self.test_input_current = False
        self.tare = data_test["tare"]
        self.renormalize = data_test["renormalize"]
        self.nist_cal = data_test["nist_cal"]
        self.test_bandwidth = False

        self.mount = ["X", "Y", "Z"]

        self.serial_protocol = "RS485"
