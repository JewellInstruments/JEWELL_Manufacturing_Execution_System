import sys

from PyQt5 import QtWidgets, uic

# import system.settings as settings

# import instrumentation.motor_init as motor_initialization
# import instrumentation.motor_control as motor_control
# import instrumentation.instrument_config as instrument_config
# import instrumentation.power_supply as power_supply

from system import serial_protocols


class Data_Aq_Control_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Data_Aq_Control_Window, self).__init__()

        # get the path to the ui file
        ui_file = "X:\Engineering\Software\Production_Software_Source_Code\MEMs_ATP_Program\window\manual_stand_control\data_aq.ui"

        # load the ui file
        uic.loadUi(ui_file, self)

        self.channel_selector_dl = self.findChild(
            QtWidgets.QDial, "channel_selector_dl"
        )
        self.channel_selector_dl.setMinimum(1)
        self.channel_selector_dl.setMaximum(10)
        self.channel_selector_dl.setValue(1)
        self.channel_selector_dl.valueChanged.connect(self.sliderMoved)

        self.channel_le = self.findChild(QtWidgets.QDial, "channel_le")

        self.output_le = self.findChild(QtWidgets.QDial, "output_le")

        self.daq = serial_protocols.serial_open("COM5", 9600)

        # serial_protocols.serial_read(self.daq)

    def sliderMoved(self):
        channel = 101
        serial_protocols.serial_write(self.daq, f"ROUT:MON @{channel}")


# application execution method


def data_aq_control_window():
    app = QtWidgets.QApplication(sys.argv)
    window = Data_Aq_Control_Window()  # noqa: F841
    app.exec_()


if __name__ == "__main__":
    data_aq_control_window()
