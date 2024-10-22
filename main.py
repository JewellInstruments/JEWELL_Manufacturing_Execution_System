"""
Author: Nicholas Green
Date: 7/9/24
About: This program will handle pre-cal of sensors for a given family
"""

import json
import os
import socket
import time
from threading import Thread

import requests
from LoginPopup import Ui_Dialog
from network import api_calls
from PySide6 import QtCore
from PySide6.QtCore import QTimer, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QWidget
from RUBY_UI import Ui_MainWindow


class LoginWindow(QDialog):
    CloseSignal = Signal(api_calls.APIHandler, bool)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.widget = Ui_Dialog()
        self.widget.setupUi(self)

        self.widget.passwordLineEdit.setEchoMode(
            self.widget.passwordLineEdit.EchoMode.Password
        )
        self.widget.loginButton.clicked.connect(self.attemptLogin)
        self.widget.cancelButton.clicked.connect(self.closePopup)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

    def closePopup(self):
        self.CloseSignal.emit(None, False)
        self.close()

    def attemptLogin(self):
        handler = api_calls.APIHandler(
            login_email=self.widget.usernameLineEdit.text().split("@")[0]
            + "@jewellinstruments.com",
            login_pass=self.widget.passwordLineEdit.text(),
        )
        if handler.login():
            self.CloseSignal.emit(handler, True)
            self.close()


class MainWindow(QMainWindow):
    def __init__(
        self,
        app: QApplication = None,
        partsJson: str = None,
        assyJson: str = None,
        subroutines: str = None,
    ) -> None:
        # window initialization
        super().__init__()
        self.app = app
        self.widget = Ui_MainWindow()
        self.widget.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

        # info for parts, assembly method, job searches, and serial numbers
        with open(partsJson) as RUBY_json:
            self.preDefinedParts = json.load(RUBY_json)
        with open(assyJson) as backend:
            self.support = json.load(backend)
        subroutines = __import__(subroutines)
        self.subroutine = subroutines.Subroutine(self)

        # auto updates target part number when new part is selected in dropdown
        self.widget.JobNumberComboBox.currentTextChanged.connect(self.setTargetJob)

        # prev / next buttons handle incrementing through assy process, next button disabled until ready checked
        self.widget.PauseButton.clicked.connect(self.pauseProgram)
        self.widget.ReadyToggle.stateChanged.connect(self.enableNextButton)
        self.widget.PreviousButton.clicked.connect(self.prevAssyStage)
        self.widget.NextButton.clicked.connect(self.nextAssyStage)

        # buttons for beginning assy at various stages in case of interruptions / errors
        self.widget.CalToggle.stateChanged.connect(self.enableCalButton)
        self.widget.VeriToggle.stateChanged.connect(self.enableVerificationButton)
        self.widget.SBRButton.clicked.connect(
            lambda: self.assemblyStage(self.support["assy"]["kanban"], True)
        )
        self.widget.SBTButton.clicked.connect(
            lambda: self.assemblyStage(self.support["assy"]["sbt1a"], True)
        )
        self.widget.CalibrationButton.clicked.connect(
            lambda: self.assemblyStage(self.support["assy"]["preCalSetup"], True)
        )
        self.widget.VerificationButton.clicked.connect(
            lambda: self.assemblyStage(self.support["assy"]["preVerSetup"], True)
        )

        # setup inacivity timer and show login page
        self.assyTimer.timeout.connect(lambda: self.UpdateStageStatus("Needs Operator"))
        self.assyTimer.setSingleShot(True)
        self.showLogin()

    def pauseProgram(self):
        popup = LoginWindow()
        popup.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        popup.widget.passwordLabel.hide()
        popup.widget.passwordLineEdit.hide()
        popup.widget.usernameLabel.hide()
        popup.widget.usernameLineEdit.hide()
        popup.widget.loginButton.clicked.connect(popup.close)
        popup.widget.loginButton.setText("Resume")
        popup.widget.cancelButton.setText("Quit Program")
        popup.widget.cancelButton.clicked.connect(quit)
        popup.exec()

    def enableVerificationButton(self, status):
        self.widget.VerificationButton.setEnabled(status)
        self.widget.SBTButton.setEnabled(status)

    def enableCalButton(self, status):
        self.widget.CalibrationButton.setEnabled(status)
        self.widget.VeriToggle.setEnabled(status)
        if self.widget.VeriToggle.isChecked():
            self.widget.VeriToggle.setChecked(status)

    def UpdateStageStatus(self, status):
        dict = {
            "stage_name": self.stage_name,
            "last_update": time.time(),
            "part_number": self.targetPart,
            "job_number": self.jobOrder,
            "axis": "x",
            "cycle": 0,
            "temperature": 22.5,
            "status": status,
            "current_user": self.handler.login_email.split("@")[0],
        }
        if self.jobOrder is None:
            dict["job_number"] = "N/A"
        if self.targetPart is None:
            dict["part_number"] = "N/A"
        # call website api
        self.handler.update(f"cal_stage_status/{self.stage_name}/", dict)

    # function to handle program setup once login in successful
    def onLoginComplete(self, handler: api_calls.APIHandler, success: bool):
        if not success or not handler:
            quit()
        self.handler = handler
        stage_configuration_response = handler.get(
            f"stage_configuration/?computer_name={socket.gethostname()}"
        )

        if stage_configuration_response.status_code != 200:
            print("computer host name not linked to any workstage")
            quit()

        stage_configuration_data = stage_configuration_response.data[-1]
        if stage_configuration_data["stage_name"] != "MEMSSTAGE1":
            print("computer host name does not belong to necessary workstage")
            quit()

        # information needed for talking to instruments, updating workstation status
        self.stage_data_aq_addr = stage_configuration_data["data_aq_com"]
        self.stage_power_supply_addr = stage_configuration_data["supply_com"]
        self.stage_name = stage_configuration_data["stage_name"]

        # search for active jobs in department, filter by allowable base numbers
        for base_part in self.support["basenumbers"]:
            dept = self.support["dept"]
            response = requests.get(
                f"http://192.168.3.11/m2mapi/Jodrtg/{dept}/{base_part}"
            )
            if response.status_code == 200:
                for i in eval(response.content):
                    self.widget.JobNumberComboBox.addItem(i["fjobno"])

        return

    # shows the login dialogue
    def showLogin(self):
        popup = LoginWindow()
        popup.setModal(True)
        popup.CloseSignal.connect(self.onLoginComplete)
        popup.exec()

    # function to set part / job number fields when selected from active jobs
    def setTargetJob(self):
        self.jobOrder = self.widget.JobNumberComboBox.currentText()
        if self.jobOrder == "N/A":
            self.widget.ProgramStatusLabel.setText(
                "Waiting for operator to select job order"
            )
            return
        response = requests.get(
            f"http://192.168.3.11/m2mapi/ShopFloorManager/{self.jobOrder}"
        )
        temp = json.loads(response.content)
        self.widget.PartNumberLineEdit.setText(temp["fpartno"].strip())
        self.targetPart = temp["fpartno"].strip()
        self.desiredPart = self.preDefinedParts.get(temp["fpartno"].strip())
        self.widget.ProgramStatusLabel.setText(
            "Waiting for operator to begin assy process"
        )

    # enables the next button in the gui
    def enableNextButton(self, status):
        self.widget.NextButton.setEnabled(status)

    # calls assembly functionality based on given stage info
    def assemblyStage(self, stage: dict, direction: bool):
        # stage setup
        if self.desiredPart is None:
            print("given part does not exist in defined parts")
            return
        if stage["prevStage"] is None:
            self.widget.PreviousButton.setEnabled(False)
        else:
            self.widget.PreviousButton.setEnabled(True)
        if stage["nextStage"] is None:
            self.widget.NextButton.setEnabled(False)
        self.widget.ReadyToggle.setChecked(False)
        self.currentStage = stage
        self.widget.stackedWidget.setCurrentIndex(0)

        # skip stages that the given model <D, S, L> is not allowed in
        if self.desiredPart["model"].split("-")[3][0] not in stage["allowedModels"]:
            if direction:
                self.nextAssyStage()
            else:
                self.prevAssyStage()
            return

        # do whatever stage needs to do
        self.widget.ProgramStatusLabel.setText(stage["miniStatus"])
        self.UpdateStageStatus("Operator At Stage")
        self.widget.TextLabel.setText(stage["text"])
        pixmap = QPixmap(stage["image"])
        self.widget.ImageLabel.setPixmap(pixmap)
        self.assyTimer.start(stage["timeout"] * 60000)

        # if stage has subroutine function, call it
        if self.auxThread and self.auxThread.is_alive():
            return

        def temp():
            if stage.get("func"):
                self.subroutine.funcDict[stage["func"]]()

        self.auxThread = Thread(target=temp)
        self.auxThread.start()

    # controls assembly stage
    def nextAssyStage(self):
        self.assyTimer.stop()
        if self.currentStage["nextStage"] is not None:
            self.assemblyStage(
                self.support["assy"][self.currentStage["nextStage"]], True
            )

    # controls assembly stage
    def prevAssyStage(self):
        self.assyTimer.stop()
        if self.currentStage["prevStage"] is not None:
            self.assemblyStage(
                self.support["assy"][self.currentStage["prevStage"]], False
            )

    # class items, holds supporting fields needed for assembly
    desiredPart: dict = None  # supporting info for part number being built
    targetPart: str = None  # part number being built
    jobOrder: str = None  # job order being built for
    auxThread: Thread | None = None  # thread used for cal routines
    handler = None  # api handler based on jewell intranet website
    assyTimer = QTimer()  # used for inacivity timeouts at each stage in assembly
    stage_data_aq_addr: str = None  # ip addr of DAQ in workstation
    stage_power_supply_addr: str = None  # ip addr of power supply in workstation
    stage_name: str = None  # name of the workstation in use
    currentStage: dict = None  # tracks the current assy stage
    preDefinedParts: dict = (
        None  # contains generic info about part numbers in the family
    )
    support: dict = None  # contains assy info


def main():
    os.system("cls")
    start_time = time.time()
    app = QApplication()
    window = MainWindow(
        app, "RUBY_PN_CONSTANTS.json", "RUBY_ASSY_CONSTANTS.json", "RubySubroutines"
    )
    window.show()
    app.exec()
    stop_time = (time.time() - start_time) / 60.0
    print(f"Run time: {stop_time:.2f} (min)")
    return


if __name__ == "__main__":
    main()
