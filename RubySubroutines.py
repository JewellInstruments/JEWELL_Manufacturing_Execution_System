import datetime
import json
import time

from eseries import E96, find_nearest
from PySide6.QtWidgets import QLabel
from pyvisa import errors

import PreCalPrimitives as prim
from system import serial_protocols


class Subroutine:
    def __init__(self, window) -> None:
        self.window = window
        # func dict provides link between assyInfo json and actual function handlers - only used if assy stage requires subroutine (dynamic output or measurement)
        self.funcDict: dict = {
            "kanban": self.kanban,
            "sbr1a": self.populate_offset_SBR,
            "preCalSetup": self.preCalTimer,
            "cal": self.calibrationRoutine,
            "sbt1a": self.populate_SBT,
            "preVerSetup": self.preVerTimer,
            "ver": self.verificationRoutine,
            "results": self.uploadResults,
        }
        self.axis: dict = {0: "X", 1: "Y", 2: "Z"}  # enumeration for axis iteration
        self.serial = "ENG"
        self.publishInfo: dict = {
            "MEMSSTAGE1": {
                "timeIn": None,
                "timeOut": None,
                "CalMeasure": {},
                "VerMeasure": {},
                "timers": {
                    "start": None,
                    "last": None,
                    "SBR": None,
                    "PreCalSetup": None,
                    "SBT": None,
                    "PreVerSetup": None,
                    "Overall": None,
                },
                "sbt": {
                    "offset_X": 0,
                    "scale_X": 0,
                    "offset_Y": 0,
                    "scale_Y": 0,
                    "offset_Z": 0,
                    "scale_Z": 0,
                },
            }
        }

    def preCalTimer(self):
        self.publishInfo[self.window.stage_name]["timers"]["SBR"] = (
            time.time() - self.publishInfo[self.window.stage_name]["timers"]["last"]
        )
        self.publishInfo[self.window.stage_name]["timers"]["last"] = time.time()

    def preVerTimer(self):
        self.publishInfo[self.window.stage_name]["timers"]["SBT"] = (
            time.time() - self.publishInfo[self.window.stage_name]["timers"]["last"]
        )
        self.publishInfo[self.window.stage_name]["timers"]["last"] = time.time()

    # calls out needed part numbers based on top level assy, allocates serial number
    def kanban(self):
        # self.serial = prim.createSerialNumber(
        #     self.window.handler, self.window.targetPart, self.window.jobOrder
        # )
        self.serial = "2024W42-test1"
        self.publishInfo[self.window.stage_name]["timeIn"] = str(
            datetime.datetime.now()
        )
        self.publishInfo[self.window.stage_name]["timers"]["start"] = time.time()
        self.publishInfo[self.window.stage_name]["timers"]["last"] = time.time()
        model = self.window.desiredPart["model"]
        pca = self.window.desiredPart["pca"]
        connector = self.window.desiredPart["connector"]
        baseplate = "F848852"
        oRing = "F848856"
        pcaScrew = "848725"
        housingScrew = "848742"
        # tells the user the housing cover compatible with the connector
        match self.window.desiredPart["connector"]:
            case "F879929":
                housing = "F848853-002"
            case "F879930":
                housing = "F848853-001"
            case _:
                pass

        self.window.widget.TextLabel.setText(
            f"""To build model: {model} you will need:
            PCA: {pca}
            Baseplate: {baseplate}
            Connector: {connector}
            Housing: {housing}
            PCA screw (4x): {pcaScrew}
            Housing screw (4x): {housingScrew}
            O-ring: {oRing}
            SERIAL#: {self.serial}"""
        )

        jobTrackerDict = {
            "serial_number": self.serial,
            "model_number": self.window.targetPart,
            "compiled_data": self.publishInfo,
            "current_stage": self.window.stage_name,
            "job_number": self.window.jobOrder,
        }
        print(json.dumps(jobTrackerDict, indent=4))
        # self.window.handler.post("job_tracking/", jobTrackerDict)

    # calls out offset SBRs for single / dual supply boards
    def populate_offset_SBR(self):
        if self.window.desiredPart["generic"]:
            match self.window.desiredPart["singleSupply"]:
                case True:
                    self.window.widget.TextLabel.setText(
                        "Populate the following SBRs: R9, R16, R23 - 3.16k"
                    )
                case False:
                    self.window.widget.TextLabel.setText(
                        "Populate the following SBRs: R9, R16, R23 - 37.4k"
                    )

    # calculates the voltage offset SBT (nearest E96 value)(based on the REV 5 schematic for RUBY)
    def calculate_offset_SBT(self, offsetRatio: float, Rfollower: float, RVbias: float):
        print(
            -((offsetRatio * RVbias * Rfollower) / ((offsetRatio * Rfollower) - RVbias))
        )
        if (
            -((offsetRatio * RVbias * Rfollower) / ((offsetRatio * Rfollower) - RVbias))
            < 0
        ):
            return 0
        return find_nearest(
            E96,
            -(
                (offsetRatio * RVbias * Rfollower)
                / ((offsetRatio * Rfollower) - RVbias)
            ),
        )

    # calculates the voltage gain SBT (nearest E96 value)(based on the REV 5 schematic for RUBY)
    def calculate_gain_SBT(self, gain: float, Rgnd: float, Rsbr: float):
        print(-(gain * Rsbr * Rgnd) + (Rsbr * Rgnd) / ((gain * Rgnd) - Rgnd - Rsbr))
        if (-(gain * Rsbr * Rgnd) + (Rsbr * Rgnd) / ((gain * Rgnd) - Rgnd - Rsbr)) < 0:
            return 0
        return find_nearest(
            E96,
            ((-(gain * Rsbr * Rgnd) + (Rsbr * Rgnd)) / ((gain * Rgnd) - Rgnd - Rsbr)),
        )

    # function to calculate all the SBTs for RUBY (REV 5 schematic)
    def calibration_calculation(self, gain: float, offsetRatio: float, measured: dict):
        outputDict = {}
        outputDict["scale_X"] = self.calculate_gain_SBT(
            gain, measured["R_gnd_X"], measured["R_scale_X"]
        )
        outputDict["scale_Y"] = self.calculate_gain_SBT(
            gain, measured["R_gnd_Y"], measured["R_scale_Y"]
        )
        outputDict["scale_Z"] = self.calculate_gain_SBT(
            gain, measured["R_gnd_Z"], measured["R_scale_Z"]
        )
        outputDict["offset_X"] = self.calculate_offset_SBT(
            offsetRatio, measured["R_bias_X"], measured["R_offset_X"]
        )
        outputDict["offset_Y"] = self.calculate_offset_SBT(
            offsetRatio, measured["R_bias_Y"], measured["R_offset_Y"]
        )
        outputDict["offset_Z"] = self.calculate_offset_SBT(
            offsetRatio, measured["R_bias_Z"], measured["R_offset_Z"]
        )
        return outputDict

    # function to tell user SBTs to populate
    def populate_SBT(self):
        self.publishInfo[self.window.stage_name]["timers"]["last"] = time.time()
        self.window.widget.TextLabel.setText(
            f"""Populate SBTs: 
            R13 - {self.publishInfo[self.window.stage_name]["sbt"]["offset_X"]}
            R8 - {self.publishInfo[self.window.stage_name]["sbt"]["scale_X"]}
            R20 - {self.publishInfo[self.window.stage_name]["sbt"]["offset_Y"]}
            R15 - {self.publishInfo[self.window.stage_name]["sbt"]["scale_Y"]}
            R27 - {self.publishInfo[self.window.stage_name]["sbt"]["offset_Z"]}
            R22 - {self.publishInfo[self.window.stage_name]["sbt"]["scale_Z"]}"""
        )

    # changes mini status window in program to check errors, returns error signals for root cause tracker (cal and ver)
    def showPowerStatus(self, measured):
        statusList: list = []
        i = 1
        for key in self.window.support["powerInfo"]:
            label = f"InfoLabel{i}"
            targetMeasurement = self.window.support["powerInfo"][key]["target"]
            measurementTolerance = self.window.support["powerInfo"][key]["tolerance"]
            match prim.measurement_within_tol(
                measured[key], targetMeasurement, measurementTolerance
            ):
                case True:
                    child = self.window.findChild(QLabel, label)
                    if child is not None:
                        child.setText(
                            f"{key} ({measured[key]:.3f}) within tol: {targetMeasurement:.1f} +/- {measurementTolerance:.2f}"
                        )
                        child.setStyleSheet("background-color: green")
                case False:
                    child = self.window.findChild(QLabel, label)
                    if child is not None:
                        text = f"{key} ({measured[key]:.3f}) outside tol: {targetMeasurement:.1f} +/- {measurementTolerance:.2f}"
                        child.setText(text)
                        child.setStyleSheet("background-color: salmon")
                        statusList.append(text)
            i = i + 1

        return statusList

    # changes mini status window in program to check errors, returns error signals for root cause tracker (ver)
    def showResistorStatus(self, res_array):
        statusList: list = []
        tolerance = 1
        for i in range(int(self.window.desiredPart["model"].split("-")[1][0])):
            meas_gain = 1 + (
                res_array[f"R_scale_{self.axis[i]}"]
                / res_array[f"R_gnd_{self.axis[i]}"]
            )
            meas_offset = (
                res_array[f"R_bias_{self.axis[i]}"]
                / res_array[f"R_offset_{self.axis[i]}"]
            )
            label = f"InfoLabel{(i*2)+1}"
            match prim.measurement_within_tol(
                meas_gain, self.window.desiredPart["gain"], tolerance
            ):
                case True:
                    child = self.window.findChild(QLabel, label)
                    if child is not None:
                        child.setText(
                            f"{self.axis[i]} gain: {meas_gain:.3f} outside tol: {tolerance:.1f}"
                        )
                        child.setStyleSheet("background-color: green")
                case False:
                    child = self.window.findChild(QLabel, label)
                    if child is not None:
                        text = f"{self.axis[i]} gain: {meas_gain:.3f} outside tol: {tolerance:.1f}"
                        child.setText(text)
                        child.setStyleSheet("background-color: salmon")
                        statusList.append(text)
            label = f"InfoLabel{(i+1)*2}"
            match prim.measurement_within_tol(
                meas_offset, self.window.desiredPart["offsetRatio"], tolerance
            ):
                case True:
                    child = self.window.findChild(QLabel, label)
                    if child is not None:
                        child.setText(
                            f"{self.axis[i]} offset: {meas_offset:.3f} outside tol: {tolerance:.1f}"
                        )
                        child.setStyleSheet("background-color: green")
                case False:
                    child = self.window.findChild(QLabel, label)
                    if child is not None:
                        text = f"{self.axis[i]} offset: {meas_offset:.3f} outside tol: {tolerance:.1f}"
                        child.setText(text)
                        child.setStyleSheet("background-color: salmon")
                        statusList.append(text)

        return statusList

    # function to measure over channels of the DMM - scan params tuple format is func, start channel, end channel
    # do not include the same channel in multiple scans as it will overwrite the output dict
    def calibration_measurement(
        self,
        daq_addr: str,
        supply_addr: str,
        singleSupply: bool,
        supplyVoltage: float,
        supplyCurrent: float,
        voltageScan: tuple,
        resistanceScan: tuple,
        cycles: int,
    ):
        # talk to the daq and power supply
        retrying = 3
        while retrying:
            try:
                daq = serial_protocols.socket_open(daq_addr, 5025)
                retrying = 0
            except errors.VisaIOError:
                retrying -= 1
                if retrying == 0:
                    print("could not connect to DAQ, quitting program")
                    quit()
        retrying = 3
        while retrying:
            try:
                supply = serial_protocols.socket_open(supply_addr, 5555)
                retrying = 0
            except errors.VisaIOError:
                retrying -= 1
                if retrying == 0:
                    print("could not connect to power supply, quitting program")
                    quit()

        serial_protocols.socket_write(daq, "*RST\r\n")

        # scan channels for voltage and resistance measurements
        prim.powerSupplyChanOff(supply, 1)
        prim.powerSupplyChanOff(supply, 2)

        res_list = prim.createScanAndRead(
            daq, resistanceScan[0], resistanceScan[1], resistanceScan[2], cycles
        )

        prim.powerSupplyChanOn(supply, 1, supplyVoltage, supplyCurrent)
        if not singleSupply:
            prim.powerSupplyChanOn(supply, 2, supplyVoltage, supplyCurrent)

        volt_list = prim.createScanAndRead(
            daq, voltageScan[0], voltageScan[1], voltageScan[2], cycles
        )

        prim.powerSupplyChanOff(supply, 1)
        prim.powerSupplyChanOff(supply, 2)

        # clear daq buffer
        serial_protocols.socket_write(daq, ":TRAC:CLE\r\n")

        # average out the scans and put data into ordered dict
        outputDict = {}
        converterDict = {
            101: "GND",
            102: "mems_X",
            103: "mems_Y",
            104: "mems_Z",
            105: "mems_T",
            106: "PWR+",
            107: "VCC",
            108: "PWR-",
            109: "R_bias_X",
            110: "R_offset_X",
            111: "R_gnd_X",
            112: "R_scale_X",
            113: "R_bias_Y",
            114: "R_offset_Y",
            115: "R_gnd_Y",
            116: "R_scale_Y",
            117: "R_bias_Z",
            118: "R_offset_Z",
            119: "R_gnd_Z",
            120: "R_scale_Z",
        }
        res_channels = resistanceScan[2] - resistanceScan[1] + 1
        volt_channels = voltageScan[2] - voltageScan[1] + 1
        for i in range(res_channels):
            col = []
            for j in range(cycles):
                col.append(res_list[i + j * res_channels])
            outputDict[resistanceScan[1] + i] = sum(col) / len(col)

        for i in range(volt_channels):
            col = []
            for j in range(cycles):
                col.append(volt_list[i + j * volt_channels])
            outputDict[voltageScan[1] + i] = sum(col) / len(col)

        # attach channel reading to readable titles
        finalDict = {}
        for k, v in outputDict.items():
            finalDict[converterDict[k]] = v

        return finalDict

    # checks power distribution, calculates SBT values
    def calibrationRoutine(self):
        self.window.widget.PreviousButton.setEnabled(False)
        self.window.widget.ReadyToggle.setEnabled(False)
        self.publishInfo[self.window.stage_name]["timers"]["CalSetup"] = (
            time.time() - self.publishInfo[self.window.stage_name]["timers"]["last"]
        )
        self.publishInfo[self.window.stage_name]["CalMeasure"] = (
            self.calibration_measurement(
                self.window.stage_data_aq_addr,
                self.window.stage_power_supply_addr,
                self.window.desiredPart["singleSupply"],
                15,
                0.3,
                ("VOLT", 101, 108),
                ("RES", 109, 120),
                5,
            )
        )
        self.publishInfo[self.window.stage_name]["sbt"] = self.calibration_calculation(
            self.window.desiredPart["gain"],
            self.window.desiredPart["offsetRatio"],
            self.publishInfo[self.window.stage_name]["CalMeasure"],
        )

        # check if board power is bad or inconsistant
        status = self.showPowerStatus(
            self.publishInfo[self.window.stage_name]["CalMeasure"]
        )
        if status:
            postDict = {
                "part_no": self.window.widget.PartNumberLineEdit.text(),
                "work_order": self.window.widget.JobNumberComboBox.currentText(),
                "symptom": "\n".join(status),
                "diagnosis": "N/A",
                "notes": "auto generated by RUBY Pre-Cal Prog",
                "user": self.window.handler.login_email.split("@")[0],
            }
            print(postDict)
            # self.handler.post("root_cause_tracking/", postDict)
        self.window.UpdateStageStatus("Needs Operator")
        self.window.widget.ReadyToggle.setEnabled(True)
        self.window.widget.ProgramStatusLabel.setText("Calibration Finished")
        self.window.widget.TextLabel.setText("Remove PCA from B.O.N test fixture")
        self.window.widget.PreviousButton.setEnabled(True)
        print(self.publishInfo)

    # checks power distribution again, ensures SBTs provide gain within tolerance
    def verificationRoutine(self):
        self.window.widget.PreviousButton.setEnabled(False)
        self.window.widget.ReadyToggle.setEnabled(False)

        self.publishInfo[self.window.stage_name]["timers"]["VerSetup"] = (
            time.time() - self.publishInfo[self.window.stage_name]["timers"]["last"]
        )
        self.publishInfo[self.window.stage_name]["VerMeasure"] = (
            self.calibration_measurement(
                self.window.stage_data_aq_addr,
                self.window.stage_power_supply_addr,
                self.window.desiredPart["singleSupply"],
                15,
                0.3,
                ("VOLT", 101, 108),
                ("RES", 109, 120),
                5,
            )
        )
        status = self.showResistorStatus(
            self.publishInfo[self.window.stage_name]["VerMeasure"]
        )
        if status:
            postDict = {
                "part_no": self.window.widget.PartNumberLineEdit.text(),
                "work_order": self.window.widget.JobNumberComboBox.currentText(),
                "symptom": "\n".join(status),
                "diagnosis": "N/A",
                "notes": "auto generated by RUBY Pre-Cal Prog",
                "user": self.window.handler.login_email.split("@")[0],
            }
            print(postDict)
            # self.handler.post("root_cause_tracking/", postDict)
        self.window.UpdateStageStatus("Needs Operator")
        self.window.widget.ReadyToggle.setEnabled(True)
        self.window.widget.ProgramStatusLabel.setText("Verification Finished")
        self.window.widget.TextLabel.setText("Remove PCA from B.O.N test fixture")
        self.window.widget.PreviousButton.setEnabled(True)

    # uploads recorded cal data and build time to database
    def uploadResults(self):
        self.publishInfo[self.window.stage_name]["timeOut"] = str(
            datetime.datetime.now()
        )
        jobTrackerDict = {
            "serial_number": self.serial,
            "model_number": self.window.targetPart,
            "compiled_data": self.publishInfo,
            "current_stage": self.window.stage_name,
            "job_number": self.window.jobOrder,
        }
        self.window.widget.stackedWidget.setCurrentIndex(1)
        self.window.widget.TextLabel.setText(
            "This is a certified 2008 Honda Accord moment"
        )
        self.publishInfo[self.window.stage_name]["timers"]["Overall"] = (
            time.time() - self.publishInfo[self.window.stage_name]["timers"]["start"]
        )
        print(json.dumps(jobTrackerDict, indent=4))
        # self.window.handler.post("job_tracking/", jobTrackerDict)
        self.window.widget.SBRTimeLabel.setText(
            time.strftime(
                "%H:%M:%S",
                time.gmtime(self.publishInfo[self.window.stage_name]["timers"]["SBR"]),
            )
        )
        self.window.widget.CalTimeLabel.setText(
            time.strftime(
                "%H:%M:%S",
                time.gmtime(
                    self.publishInfo[self.window.stage_name]["timers"]["CalSetup"]
                ),
            )
        )
        self.window.widget.SBTTimeLabel.setText(
            time.strftime(
                "%H:%M:%S",
                time.gmtime(self.publishInfo[self.window.stage_name]["timers"]["SBT"]),
            )
        )
        self.window.widget.VerificationTimeLabel.setText(
            time.strftime(
                "%H:%M:%S",
                time.gmtime(
                    self.publishInfo[self.window.stage_name]["timers"]["VerSetup"]
                ),
            )
        )
        self.window.widget.OverallTimeLabel.setText(
            time.strftime(
                "%H:%M:%S",
                time.gmtime(
                    self.publishInfo[self.window.stage_name]["timers"]["Overall"]
                ),
            )
        )
