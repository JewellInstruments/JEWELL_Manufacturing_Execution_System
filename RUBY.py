# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RUBY.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLayout, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1112, 731)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.AssyAndCalButton = QPushButton(self.groupBox_2)
        self.AssyAndCalButton.setObjectName(u"AssyAndCalButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.AssyAndCalButton.sizePolicy().hasHeightForWidth())
        self.AssyAndCalButton.setSizePolicy(sizePolicy1)
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(0, 85, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        brush2 = QBrush(QColor(131, 255, 245, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Light, brush2)
        brush3 = QBrush(QColor(77, 247, 233, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush3)
        brush4 = QBrush(QColor(12, 120, 111, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush4)
        brush5 = QBrush(QColor(16, 160, 148, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        brush6 = QBrush(QColor(255, 255, 255, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush6)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush)
        brush7 = QBrush(QColor(139, 247, 238, 255))
        brush7.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush7)
        brush8 = QBrush(QColor(255, 255, 220, 255))
        brush8.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush8)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush7)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush8)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush6)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush)
        brush9 = QBrush(QColor(24, 240, 222, 255))
        brush9.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush9)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush8)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush)
        self.AssyAndCalButton.setPalette(palette)
        self.AssyAndCalButton.setStyleSheet(u"background-color:rgb(0, 85, 255)")

        self.verticalLayout.addWidget(self.AssyAndCalButton)

        self.CalibrationButton = QPushButton(self.groupBox_2)
        self.CalibrationButton.setObjectName(u"CalibrationButton")
        sizePolicy1.setHeightForWidth(self.CalibrationButton.sizePolicy().hasHeightForWidth())
        self.CalibrationButton.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.CalibrationButton)

        self.VerificationButton = QPushButton(self.groupBox_2)
        self.VerificationButton.setObjectName(u"VerificationButton")
        sizePolicy1.setHeightForWidth(self.VerificationButton.sizePolicy().hasHeightForWidth())
        self.VerificationButton.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.VerificationButton)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.gridLayout.addWidget(self.groupBox_2, 2, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.ImageLabel = QLabel(self.groupBox_3)
        self.ImageLabel.setObjectName(u"ImageLabel")
        sizePolicy.setHeightForWidth(self.ImageLabel.sizePolicy().hasHeightForWidth())
        self.ImageLabel.setSizePolicy(sizePolicy)
        self.ImageLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.ImageLabel)

        self.TextLabel = QLabel(self.groupBox_3)
        self.TextLabel.setObjectName(u"TextLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.TextLabel.sizePolicy().hasHeightForWidth())
        self.TextLabel.setSizePolicy(sizePolicy2)
        self.TextLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.TextLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.PreviousButton = QPushButton(self.groupBox_3)
        self.PreviousButton.setObjectName(u"PreviousButton")
        sizePolicy.setHeightForWidth(self.PreviousButton.sizePolicy().hasHeightForWidth())
        self.PreviousButton.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.PreviousButton)

        self.ReadyToggle = QCheckBox(self.groupBox_3)
        self.ReadyToggle.setObjectName(u"ReadyToggle")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.ReadyToggle.sizePolicy().hasHeightForWidth())
        self.ReadyToggle.setSizePolicy(sizePolicy3)

        self.horizontalLayout.addWidget(self.ReadyToggle)

        self.NextButton = QPushButton(self.groupBox_3)
        self.NextButton.setObjectName(u"NextButton")
        self.NextButton.setEnabled(False)
        sizePolicy.setHeightForWidth(self.NextButton.sizePolicy().hasHeightForWidth())
        self.NextButton.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.NextButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout_2.setStretch(0, 1)

        self.horizontalLayout_4.addLayout(self.verticalLayout_2)


        self.gridLayout.addWidget(self.groupBox_3, 0, 1, 3, 1)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignCenter)
        self.formLayout.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.formLayout.setHorizontalSpacing(10)
        self.formLayout.setVerticalSpacing(10)
        self.PartNumberLabel = QLabel(self.groupBox)
        self.PartNumberLabel.setObjectName(u"PartNumberLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.PartNumberLabel)

        self.PartNumberComboBox = QComboBox(self.groupBox)
        self.PartNumberComboBox.addItem("")
        self.PartNumberComboBox.setObjectName(u"PartNumberComboBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.PartNumberComboBox.sizePolicy().hasHeightForWidth())
        self.PartNumberComboBox.setSizePolicy(sizePolicy4)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.PartNumberComboBox)

        self.WorkStationLabel = QLabel(self.groupBox)
        self.WorkStationLabel.setObjectName(u"WorkStationLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.WorkStationLabel)

        self.WorkStationComboBox = QComboBox(self.groupBox)
        self.WorkStationComboBox.setObjectName(u"WorkStationComboBox")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.WorkStationComboBox)


        self.horizontalLayout_3.addLayout(self.formLayout)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.ProgramStatuLabel = QLabel(self.groupBox_4)
        self.ProgramStatuLabel.setObjectName(u"ProgramStatuLabel")
        self.ProgramStatuLabel.setStyleSheet(u"background-color:lightgrey")
        self.ProgramStatuLabel.setAlignment(Qt.AlignCenter)
        self.ProgramStatuLabel.setWordWrap(True)
        self.ProgramStatuLabel.setMargin(10)

        self.verticalLayout_3.addWidget(self.ProgramStatuLabel)


        self.gridLayout.addWidget(self.groupBox_4, 1, 0, 1, 1)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1112, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Controls", None))
        self.AssyAndCalButton.setText(QCoreApplication.translate("MainWindow", u"ASSY AND CAL ROUTINE", None))
        self.CalibrationButton.setText(QCoreApplication.translate("MainWindow", u"CALIBRATION ROUTINE", None))
        self.VerificationButton.setText(QCoreApplication.translate("MainWindow", u"VERIFICATION ROUTINE", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Program Window", None))
        self.ImageLabel.setText(QCoreApplication.translate("MainWindow", u"Assy Images", None))
        self.TextLabel.setText(QCoreApplication.translate("MainWindow", u"Assy Instructions", None))
        self.PreviousButton.setText(QCoreApplication.translate("MainWindow", u"Previous", None))
        self.ReadyToggle.setText(QCoreApplication.translate("MainWindow", u"Ready?", None))
        self.NextButton.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Setup", None))
        self.PartNumberLabel.setText(QCoreApplication.translate("MainWindow", u"Part Number", None))
        self.PartNumberComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Select Part", None))

        self.WorkStationLabel.setText(QCoreApplication.translate("MainWindow", u"Work Station", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Status", None))
        self.ProgramStatuLabel.setText(QCoreApplication.translate("MainWindow", u"Waiting For Part Number Selection", None))
    # retranslateUi

