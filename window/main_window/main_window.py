import sys
import logging
import os

from PyQt5 import QtWidgets, uic, QtCore

from system import settings

from network import api_calls
from network import filesystem


class LoginPopup(QtWidgets.QWidget):
    def __init__(self, parent):
        """
        pulled from https://stackoverflow.com/questions/67029993/pyqt-creating-a-popup-in-the-window
        """
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        # self.setAttribute(QtCore.Qt.WA_StyledBackground)
        # self.setAutoFillBackground(True)
        # self.setStyleSheet(
        #     """
        #     LoginPopup {
        #         background: rgba(64, 64, 64, 64);
        #     }
        #     QWidget#container {
        #         border: 2px solid darkGray;
        #         border-radius: 4px;
        #         background: rgb(64, 64, 64);
        #     }
        #     QWidget#container > QLabel {
        #         color: white;
        #     }
        #     QLabel#title {
        #         font-size: 20pt;
        #     }
        #     QPushButton#close {
        #         color: white;
        #         font-weight: bold;
        #         background: none;
        #         border: 1px solid gray;
        #     }
        # """
        # )

        fullLayout = QtWidgets.QVBoxLayout(self)

        self.container = QtWidgets.QWidget(
            autoFillBackground=True, objectName="container"
        )
        fullLayout.addWidget(self.container, alignment=QtCore.Qt.AlignCenter)
        self.container.setSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum
        )

        buttonSize = self.fontMetrics().height()
        self.closeButton = QtWidgets.QPushButton(
            "×", self.container, objectName="close"
        )
        self.closeButton.setFixedSize(buttonSize, buttonSize)
        self.closeButton.clicked.connect(self.reject)

        layout = QtWidgets.QVBoxLayout(self.container)
        layout.setContentsMargins(
            buttonSize * 2, buttonSize, buttonSize * 2, buttonSize
        )

        title = QtWidgets.QLabel(
            "Enter an email address",
            objectName="title",
            alignment=QtCore.Qt.AlignCenter,
        )
        layout.addWidget(title)

        layout.addWidget(QtWidgets.QLabel("EMAIL"))
        self.emailEdit = QtWidgets.QLineEdit()
        layout.addWidget(self.emailEdit)
        layout.addWidget(QtWidgets.QLabel("PASSWORD"))
        self.passwordEdit = QtWidgets.QLineEdit(echoMode=QtWidgets.QLineEdit.Password)
        layout.addWidget(self.passwordEdit)

        self.emailEdit.setText("ljameson")
        self.passwordEdit.setText("Jed1Mast3r97!")

        buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        layout.addWidget(buttonBox)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.okButton = buttonBox.button(buttonBox.Ok)
        self.okButton.setEnabled(False)

        self.emailEdit.textChanged.connect(self.checkInput)
        self.passwordEdit.textChanged.connect(self.checkInput)
        self.emailEdit.returnPressed.connect(lambda: self.passwordEdit.setFocus())
        self.passwordEdit.returnPressed.connect(self.accept)

        parent.installEventFilter(self)

        self.loop = QtCore.QEventLoop(self)
        self.emailEdit.setFocus()

    def checkInput(self):
        self.okButton.setEnabled(bool(self.username() and self.password()))

    def username(self):
        return self.emailEdit.text()

    def password(self):
        return self.passwordEdit.text()

    def accept(self):
        if self.username() and self.password():
            self.loop.exit(True)

    def reject(self):
        self.loop.exit(False)

    def close(self):
        self.loop.quit()

    def showEvent(self, event):
        self.setGeometry(self.parent().rect())

    def resizeEvent(self, event):
        r = self.closeButton.rect()
        r.moveTopRight(self.container.rect().topRight() + QtCore.QPoint(-5, 5))
        self.closeButton.setGeometry(r)

    def eventFilter(self, source, event):
        if event.type() == event.Resize:
            self.setGeometry(source.rect())
        return super().eventFilter(source, event)

    def exec_(self):
        self.show()
        self.raise_()
        res = self.loop.exec_()
        self.hide()
        return res


class ATP_Setup_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(ATP_Setup_Window, self).__init__()

        # get the path to the ui file
        ui_file = settings.WINDOW_FILEPATH

        # load the ui file
        uic.loadUi(ui_file, self)

        # self.setAttribute(QtCore.Qt.WA_StyledBackground)
        # self.setAutoFillBackground(True)

        # self.setStyleSheet(
        #     """
        #     LoginPopup {
        #         background: rgba(64, 64, 64, 64);
        #     }
        #     QWidget#container {
        #         border: 2px solid darkGray;
        #         border-radius: 4px;
        #         background: rgb(64, 64, 64);
        #     }
        #     QWidget#container > QLabel {
        #         color: white;
        #     }
        #     QLabel#title {
        #         font-size: 20pt;
        #     }
        #     QPushButton#close {
        #         color: white;
        #         font-weight: bold;
        #         background: none;
        #         border: 1px solid gray;
        #     }
        # """
        # )

        # MENU BAR ACTIONS
        ############################################################################
        #
        # self.actSave = self.findChild(QtWidgets.QAction, 'actionSave')
        # self.actSave.triggered.connect(self.Finish_Setup)
        ############################################################################

        # BUTTONS
        ############################################################################

        self.load_test_pb = self.findChild(QtWidgets.QPushButton, "load_test_pb")
        self.load_test_pb.clicked.connect(self.load_test)

        self.finish_pb = self.findChild(QtWidgets.QPushButton, "finish_pb")
        self.finish_pb.clicked.connect(self.finish)

        self.exit_pb = self.findChild(QtWidgets.QPushButton, "exit_pb")
        self.exit_pb.clicked.connect(self.exit)

        self.search_pb = self.findChild(QtWidgets.QPushButton, "search_pb")
        self.search_pb.clicked.connect(self.search)

        self.help_pb = self.findChild(QtWidgets.QPushButton, "help_pb")
        self.help_pb.clicked.connect(self.search)

        self.load_specs_pb = self.findChild(QtWidgets.QPushButton, "load_specs_pb")
        self.load_specs_pb.clicked.connect(self.search)

        ############################################################################

        # LINE EDITS
        ############################################################################

        self.serialno_le_1 = self.findChild(QtWidgets.QLineEdit, "serialno_le_1")
        self.serialno_le_2 = self.findChild(QtWidgets.QLineEdit, "serialno_le_2")
        self.serialno_le_3 = self.findChild(QtWidgets.QLineEdit, "serialno_le_3")
        self.serialno_le_4 = self.findChild(QtWidgets.QLineEdit, "serialno_le_4")
        self.serialno_le_5 = self.findChild(QtWidgets.QLineEdit, "serialno_le_5")
        self.serialno_le_6 = self.findChild(QtWidgets.QLineEdit, "serialno_le_6")
        self.serialno_le_7 = self.findChild(QtWidgets.QLineEdit, "serialno_le_7")
        self.serialno_le_8 = self.findChild(QtWidgets.QLineEdit, "serialno_le_8")

        self.serialno_list = [
            self.serialno_le_1,
            self.serialno_le_2,
            self.serialno_le_3,
            self.serialno_le_4,
            self.serialno_le_5,
            self.serialno_le_6,
            self.serialno_le_7,
            self.serialno_le_8,
        ]

        self.work_order_le = self.findChild(QtWidgets.QLineEdit, "work_order_le")
        self.part_no_le = self.findChild(QtWidgets.QLineEdit, "part_no_le")

        self.rmano_le_1 = self.findChild(QtWidgets.QLineEdit, "rmano_le_1")
        self.rmano_le_2 = self.findChild(QtWidgets.QLineEdit, "rmano_le_2")
        self.rmano_le_3 = self.findChild(QtWidgets.QLineEdit, "rmano_le_3")
        self.rmano_le_4 = self.findChild(QtWidgets.QLineEdit, "rmano_le_4")
        self.rmano_le_5 = self.findChild(QtWidgets.QLineEdit, "rmano_le_5")
        self.rmano_le_6 = self.findChild(QtWidgets.QLineEdit, "rmano_le_6")
        self.rmano_le_7 = self.findChild(QtWidgets.QLineEdit, "rmano_le_7")
        self.rmano_le_8 = self.findChild(QtWidgets.QLineEdit, "rmano_le_8")

        self.rmano_list = [
            self.rmano_le_1,
            self.rmano_le_2,
            self.rmano_le_3,
            self.rmano_le_4,
            self.rmano_le_5,
            self.rmano_le_6,
            self.rmano_le_7,
            self.rmano_le_8,
        ]

        # model_no_le

        ############################################################################

        # CHECK BOXES
        ############################################################################

        self.full_atp_ch = self.findChild(QtWidgets.QCheckBox, "full_atp_ch")
        self.tumble_test_ch = self.findChild(QtWidgets.QCheckBox, "tumble_test_ch")
        self.jdx_linearity_sweep_ch = self.findChild(
            QtWidgets.QCheckBox, "jdx_linearity_sweep_ch"
        )

        ############################################################################

        # TEXT EDITS
        ############################################################################

        self.msg_te = self.findChild(QtWidgets.QPlainTextEdit, "msg_te")

        ############################################################################

        # COMBO BOXES
        ############################################################################

        # self.email_cb = self.findChild(QtWidgets.QComboBox, "email_cb")
        # self.email_cb.addItems(get_tester_names.get_emails())

        self.user_name = ""
        self.user_password = ""

        self.show()

    def showDialog(self):
        dialog = LoginPopup(self)
        if dialog.exec_():
            # add domain if necessary.
            if "@" not in dialog.username():
                self.user_name = f"{dialog.username()}@jewellinstruments.com"
            else:
                self.user_name = f"{dialog.username()}"
            self.user_password = dialog.password()

    def load_test(self):
        """
        get the test setup json file for a given work order should one exist.
        """
        work_order = self.work_order_le.text()
        if work_order == "00000":
            pass
        return

    def finish(self):
        """
        create a json file locally for a given test.
        """
        # check the username and password.
        # ideally i would like to check the training table to see if the user is qualified on this station.

        while True:
            self.showDialog()
            api_handler_success = api_calls.APIHandler(
                login_email=self.user_name, login_pass=self.user_password
            ).login()
            if api_handler_success:
                break

        os.environ["API_USER"] = self.user_name
        os.environ["API_PASSWORD"] = self.user_password

        logging.info(f"login successful for user: {self.user_name}")

        # open popup for user and password.
        work_order = self.work_order_le.text()
        if work_order != "":
            work_order, sales_order, customer = api_calls.get_work_order(work_order)
        else:
            work_order, sales_order, customer = "00000", "local", "Jewell"

        serial_no_list = []
        for item in self.serialno_list:
            serial_no = item.text()
            if serial_no != "":
                serial_no_list.append(serial_no)

        rma_no_list = []
        for item in self.rmano_list:
            rma_no = item.text()
            if rma_no != "":
                rma_no_list.append(rma_no)

        data = {
            "part_no": self.part_no_le.text(),
            "work_order": work_order,
            "sales_order": sales_order,
            "customer": customer,
            "serial_no_list": serial_no_list,
            "rma_no_list": rma_no_list,
            "full_atp": self.full_atp_ch.isChecked(),
            "tumble_test": self.tumble_test_ch.isChecked(),
            "linearity_verification": self.jdx_linearity_sweep_ch.isChecked(),
            "name": self.user_name,
        }
        # print(data)

        filesystem.load_json_data_to_file(work_order, data)

        self.close()

        return

    # exit the window
    def exit(self):
        self.close()
        return

    def search(self):
        """
        go to the api for a given part number and get the specs. display and create a local object (json file) for the updated test?
        """
        return


# application execution method


def atp_setup_window():

    app = QtWidgets.QApplication(sys.argv)
    window = ATP_Setup_Window()  # noqa: F841
    app.exec_()
