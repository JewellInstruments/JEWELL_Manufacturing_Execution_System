import sys
import serial.tools.list_ports

from PyQt5 import QtWidgets, uic, QtCore, QtGui

from system import settings
from system import serial_protocols
from system import stage_configuration

from instrumentation import motor_initialization
from instrumentation import motor_control


class Manual_Stage_Control_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Manual_Stage_Control_Window, self).__init__()

        # get the path to the ui file
        ui_file = settings.MANUAL_STAGE_WINDOW_FILEPATH

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

        self.connect_pb = self.findChild(QtWidgets.QPushButton, "connect_pb")
        self.connect_pb.clicked.connect(self.connect_to_controller)

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

        self.controller_type_cb = self.findChild(
            QtWidgets.QComboBox, "controller_type_cb"
        )
        self.controller_type_cb.setCurrentText(stage_configuration.CONTROLLER_TYPE)

        self.com_ports_cb = self.findChild(QtWidgets.QComboBox, "com_ports_cb")
        ports = [port.name for port in serial.tools.list_ports.comports()]
        self.com_ports_cb.addItems(ports)
        if stage_configuration.STAGE_PORT != "":
            self.com_ports_cb.setCurrentText(stage_configuration.STAGE_PORT)

        ############################################################################
        ############################################################################

        # self.connect_to_controller()

        self.angle = 0.0  # degrees

        self.show()

    def connect_to_controller(self):
        if self.controller_type_cb.currentText() == "Automation1":
            self.controller = motor_initialization.automation1_configure_stage()
        elif self.controller_type_cb.currentText() == "Ensemble":
            port = self.com_ports_cb.currentText()
            self.controller = serial_protocols.serial_open(port, 9600)
        else:
            self.message_te.append("Please select which controller is connected.")

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
                        self.controller, angle
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
                        self.controller, angle
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
            motor_control.define_home(self.controller)
            final_angle = motor_control.move_stage_incremental(self.controller, 0)
            self.angle_le.setText(f"{final_angle:.5f}")

        else:
            self.message_te.append("Command not understood.")

        return

    def move_relative_last_stored_left(self):
        angle = abs(self.angle)
        self.message_te.append(f"Moving {angle} degrees from current position.")
        # print("Moving")
        final_angle = motor_control.move_stage_incremental(self.controller, -angle)
        self.angle_le.setText(f"{final_angle:.5f}")

    def move_relative_last_stored_right(self):
        angle = abs(self.angle)
        self.message_te.append(f"Moving {angle} degrees from current position.")
        # print("Moving")
        final_angle = motor_control.move_stage_incremental(self.controller, angle)
        self.angle_le.setText(f"{final_angle:.5f}")

    def move_absolute_0(self):
        angle = 0.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(self.controller, angle)
        self.angle_le.setText(f"{final_angle:.5f}")

    def move_absolute_180(self):
        angle = 180.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(self.controller, angle)
        self.angle_le.setText(f"{final_angle:.5f}")

    def move_absolute_90(self):
        angle = 90.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(self.controller, angle)
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_60(self):
        angle = 60.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(self.controller, angle)
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_45(self):
        angle = 45.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(self.controller, angle)
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_30(self):
        angle = 30.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(self.controller, angle)
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_145(self):
        angle = 14.5
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(self.controller, angle)
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_8(self):
        angle = 8.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(self.controller, angle)
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_3(self):
        angle = 3.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(self.controller, angle)
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_1(self):
        angle = 1.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(self.controller, angle)
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_neg90(self):
        angle = -90.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(self.controller, angle)
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_neg60(self):
        angle = -60.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(self.controller, angle)
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_neg45(self):
        angle = -45.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(self.controller, angle)
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_neg30(self):
        angle = -30.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(self.controller, angle)
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_neg145(self):
        angle = -14.5
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(self.controller, angle)
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_neg8(self):
        angle = -8.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(self.controller, angle)
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_neg3(self):
        angle = -3.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(self.controller, angle)
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def move_absolute_neg1(self):
        angle = -1.0
        self.message_te.append(f"Moving to {angle} degrees.")
        final_angle = motor_control.move_stage_to_angle(self.controller, angle)
        self.angle_le.setText(f"{final_angle:.5f}")
        self.angle = angle

    def exit(self):
        self.close()
        return


# application execution method


def manual_stage_control_window():
    app = QtWidgets.QApplication(sys.argv)
    _ = Manual_Stage_Control_Window()
    app.exec_()
