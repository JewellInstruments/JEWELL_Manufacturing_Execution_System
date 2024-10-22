import sys

from PyQt5 import QtWidgets, uic, QtCore, QtGui

from system import settings

from instrumentation import motor_control
from instrumentation import instrument_config
from instrumentation import power_supply


class Manual_Stand_Control_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Manual_Stand_Control_Window, self).__init__()

        # get the path to the ui file
        ui_file = settings.MANUAL_STAGEWINDOW_FILEPATH

        # load the ui file
        uic.loadUi(ui_file, self)

        # MENU BAR ACTIONS
        ############################################################################
        #
        # self.actSave = self.findChild(QtWidgets.QAction, 'actionSave')
        # self.actSave.triggered.connect(self.Finish_Setup)
        ############################################################################

        # BUTTONS
        ############################################################################

        self.execute_pb = self.findChild(QtWidgets.QPushButton, "execute_pb")
        self.execute_pb.clicked.connect(self.execute_command)

        self.exit_pb = self.findChild(QtWidgets.QPushButton, "exit_pb")
        self.exit_pb.clicked.connect(self.exit)

        self.power_pb = self.findChild(QtWidgets.QPushButton, "power_pb")
        self.power_pb.clicked.connect(self.set_power_state)

        self.hotkey_0_pb = self.findChild(QtWidgets.QPushButton, "hotkey_0_pb")
        self.hotkey_0_pb.clicked.connect(self.move_absolute_0)

        self.hotkey_180_pb = self.findChild(QtWidgets.QPushButton, "hotkey_180_pb")
        self.hotkey_180_pb.clicked.connect(self.move_absolute_180)

        self.hotkey_90_pb = self.findChild(QtWidgets.QPushButton, "hotkey_90_pb")
        self.hotkey_90_pb.clicked.connect(self.move_absolute_90)

        self.hotkey_60_pb = self.findChild(QtWidgets.QPushButton, "hotkey_60_pb")
        self.hotkey_60_pb.clicked.connect(self.move_absolute_60)

        self.hotkey_45_pb = self.findChild(QtWidgets.QPushButton, "hotkey_45_pb")
        self.hotkey_45_pb.clicked.connect(self.move_absolute_45)

        self.hotkey_30_pb = self.findChild(QtWidgets.QPushButton, "hotkey_30_pb")
        self.hotkey_30_pb.clicked.connect(self.move_absolute_30)

        self.hotkey_145_pb = self.findChild(QtWidgets.QPushButton, "hotkey_145_pb")
        self.hotkey_145_pb.clicked.connect(self.move_absolute_145)

        self.hotkey_8_pb = self.findChild(QtWidgets.QPushButton, "hotkey_8_pb")
        self.hotkey_8_pb.clicked.connect(self.move_absolute_8)

        self.hotkey_3_pb = self.findChild(QtWidgets.QPushButton, "hotkey_3_pb")
        self.hotkey_3_pb.clicked.connect(self.move_absolute_3)

        self.hotkey_1_pb = self.findChild(QtWidgets.QPushButton, "hotkey_1_pb")
        self.hotkey_1_pb.clicked.connect(self.move_absolute_1)

        self.hotkey_neg90_pb = self.findChild(QtWidgets.QPushButton, "hotkey_neg90_pb")
        self.hotkey_neg90_pb.clicked.connect(self.move_absolute_neg90)

        self.hotkey_neg60_pb = self.findChild(QtWidgets.QPushButton, "hotkey_neg60_pb")
        self.hotkey_neg60_pb.clicked.connect(self.move_absolute_neg60)

        self.hotkey_neg45_pb = self.findChild(QtWidgets.QPushButton, "hotkey_neg45_pb")
        self.hotkey_neg45_pb.clicked.connect(self.move_absolute_neg45)

        self.hotkey_neg30_pb = self.findChild(QtWidgets.QPushButton, "hotkey_neg30_pb")
        self.hotkey_neg30_pb.clicked.connect(self.move_absolute_neg30)

        self.hotkey_neg145_pb = self.findChild(
            QtWidgets.QPushButton, "hotkey_neg145_pb"
        )
        self.hotkey_neg145_pb.clicked.connect(self.move_absolute_neg145)

        self.hotkey_neg8_pb = self.findChild(QtWidgets.QPushButton, "hotkey_neg8_pb")
        self.hotkey_neg8_pb.clicked.connect(self.move_absolute_neg8)

        self.hotkey_neg3_pb = self.findChild(QtWidgets.QPushButton, "hotkey_neg3_pb")
        self.hotkey_neg3_pb.clicked.connect(self.move_absolute_neg3)

        self.hotkey_neg1_pb = self.findChild(QtWidgets.QPushButton, "hotkey_neg1_pb")
        self.hotkey_neg1_pb.clicked.connect(self.move_absolute_neg1)

        ############################################################################

        # LINE EDITS
        ############################################################################

        self.command_le = self.findChild(QtWidgets.QLineEdit, "command_le")
        self.command_le.returnPressed.connect(self.execute_command)

        self.angle_le = self.findChild(QtWidgets.QLineEdit, "angle_le")
        self.channel_le = self.findChild(QtWidgets.QLineEdit, "channel_le")
        self.output_le = self.findChild(QtWidgets.QLineEdit, "output_le")
        self.supply_1_volts_le = self.findChild(
            QtWidgets.QLineEdit, "supply_1_volts_le"
        )
        self.supply_2_volts_le = self.findChild(
            QtWidgets.QLineEdit, "supply_2_volts_le"
        )
        self.current_limit_1_le = self.findChild(
            QtWidgets.QLineEdit, "current_limit_1_le"
        )
        self.current_limit_2_le = self.findChild(
            QtWidgets.QLineEdit, "current_limit_2_le"
        )

        self.shortcut_left = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Left"), self)
        self.shortcut_left.activated.connect(self.move_relative_last_stored_left)

        self.shortcut_right = QtWidgets.QShortcut(
            QtGui.QKeySequence("Ctrl+Right"), self
        )
        self.shortcut_right.activated.connect(self.move_relative_last_stored_right)

        ############################################################################

        # TEXT EDITS
        ############################################################################

        self.message_te = self.findChild(QtWidgets.QTextEdit, "message_te")

        ############################################################################

        # COMBO BOXES
        ############################################################################

        # self.instrumentation_dict['Stage'] = motor_initialization.automation1_configure_stage()
        self.instrumentation_dict = instrument_config.instrumentation_setup()

        self.angle = 0.0  # degrees

        self.POWER_STATUS = "OFF"

        self.show()

    def keyPressEvent(self, event):
        widget = QtWidgets.QApplication.focusWidget()
        if widget == "command_le":
            self.message_te.append(
                "Arrow keys are not able to move the stage while the command box is active."
            )
        else:
            # if up arrow key is pressed
            if event.key() == QtCore.Qt.Key_Up:
                self.move_absolute_0()

            # if down arrow key is pressed
            elif event.key() == QtCore.Qt.Key_Down:
                self.move_absolute_180()

    def set_power_state(self):
        V_1 = float(self.supply_1_volts_le.text())
        V_2 = float(self.supply_2_volts_le.text())
        mA_1 = float(self.current_limit_1_le.text())
        mA_2 = float(self.current_limit_2_le.text())

        if self.POWER_STATUS == "OFF":
            self.message_te.append("Turning power On.")
            self.POWER_STATUS = "ON"
        else:
            self.message_te.append("Turning power OFF.")
            self.POWER_STATUS = "OFF"

        power_supply.set_power_supply_state(
            self.instrumentation_dict["Supply"], self.POWER_STATUS, V_1, V_2, mA_1, mA_2
        )

        return

    def execute_command(self):
        command = self.command_le.text().upper()
        self.command_le.selectAll()

        final_angle = 0

        if command[:2] == "PA":
            try:
                angle = float(command[2:])
                if abs(angle) < 360.0:
                    self.message_te.append(f"Moving to {angle} degrees.")
                    final_angle = motor_control.move_stage_to_angle(
                        self.instrumentation_dict["Stage"], angle
                    )
                    self.angle_le.setText(f"{final_angle:.5f}")
                    self.angle = angle
                else:
                    self.message_te.append(
                        "Cannot move to an angle beyond 360 degrees."
                    )

            except Exception as e:
                print(e)

        elif command[:2] == "PR":
            try:
                angle = float(command[2:])
                if abs(angle) < 360.0:
                    self.message_te.append(
                        f"Moving {angle} degrees from current position."
                    )
                    # print("Moving")
                    final_angle = motor_control.move_stage_incremental(
                        self.instrumentation_dict["Stage"], angle
                    )
                    self.angle_le.setText(f"{final_angle:.5f}")
                    self.angle = angle
                else:
                    self.message_te.append(
                        "Cannot move to an angle beyond 360 degrees."
                    )
            except Exception as e:
                print(e)
        elif command[:2] == "DH":
            self.message_te.append("Redefining home")
            motor_control.define_home(self.instrumentation_dict["Stage"])
            final_angle = motor_control.move_stage_incremental(
                self.instrumentation_dict["Stage"], 0
            )
            self.angle_le.setText(f"{final_angle:.5f}")

        else:
            self.message_te.append("Command not understood.")

        return

    def move_relative_last_stored_left(self):
        angle = abs(self.angle)
        self.message_te.append(f"Moving {angle} degrees from current position.")
        # print("Moving")
        final_angle = motor_control.move_stage_incremental(
            self.instrumentation_dict["Stage"], -angle
        )
        self.angle_le.setText(f"{final_angle:.5f}")

    def move_relative_last_stored_right(self):
        angle = abs(self.angle)
        self.message_te.append(f"Moving {angle} degrees from current position.")
        # print("Moving")
        final_angle = motor_control.move_stage_incremental(
            self.instrumentation_dict["Stage"], angle
        )
        self.angle_le.setText(f"{final_angle:.5f}")

    def move_absolute_0(self):
        angle = 0.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(
            self.instrumentation_dict["Stage"], angle
        )
        self.angle_le.setText(f"{final_angle:.5f}")

    def move_absolute_180(self):
        angle = 180.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(
            self.instrumentation_dict["Stage"], angle
        )
        self.angle_le.setText(f"{final_angle:.5f}")

    def move_absolute_90(self):
        angle = 90.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(
            self.instrumentation_dict["Stage"], angle
        )
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_60(self):
        angle = 60.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(
            self.instrumentation_dict["Stage"], angle
        )
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_45(self):
        angle = 45.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(
            self.instrumentation_dict["Stage"], angle
        )
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_30(self):
        angle = 30.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(
            self.instrumentation_dict["Stage"], angle
        )
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_145(self):
        angle = 14.5
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(
            self.instrumentation_dict["Stage"], angle
        )
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_8(self):
        angle = 8.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(
            self.instrumentation_dict["Stage"], angle
        )
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_3(self):
        angle = 3.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(
            self.instrumentation_dict["Stage"], angle
        )
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_1(self):
        angle = 1.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(
            self.instrumentation_dict["Stage"], angle
        )
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_neg90(self):
        angle = -90.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(
            self.instrumentation_dict["Stage"], angle
        )
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_neg60(self):
        angle = -60.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(
            self.instrumentation_dict["Stage"], angle
        )
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_neg45(self):
        angle = -45.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(
            self.instrumentation_dict["Stage"], angle
        )
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_neg30(self):
        angle = -30.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(
            self.instrumentation_dict["Stage"], angle
        )
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_neg145(self):
        angle = -14.5
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(
            self.instrumentation_dict["Stage"], angle
        )
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_neg8(self):
        angle = -8.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(
            self.instrumentation_dict["Stage"], angle
        )
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_neg3(self):
        angle = -3.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(
            self.instrumentation_dict["Stage"], angle
        )
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_neg1(self):
        angle = -1.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(
            self.instrumentation_dict["Stage"], angle
        )
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def exit(self):
        self.close()
        return


# application execution method


def manual_stage_control_window():
    app = QtWidgets.QApplication(sys.argv)
    window = Manual_Stand_Control_Window()  # noqa: F841
    app.exec_()


if __name__ == "__main__":
    manual_stage_control_window()
