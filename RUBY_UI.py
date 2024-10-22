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
    QLayout, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStackedWidget, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1118, 818)
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
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.CalToggle = QCheckBox(self.groupBox_2)
        self.CalToggle.setObjectName(u"CalToggle")

        self.horizontalLayout_5.addWidget(self.CalToggle)

        self.VeriToggle = QCheckBox(self.groupBox_2)
        self.VeriToggle.setObjectName(u"VeriToggle")
        self.VeriToggle.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.VeriToggle)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.SBRButton = QPushButton(self.groupBox_2)
        self.SBRButton.setObjectName(u"SBRButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.SBRButton.sizePolicy().hasHeightForWidth())
        self.SBRButton.setSizePolicy(sizePolicy1)
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(250, 128, 114, 255))
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
        self.SBRButton.setPalette(palette)
        font = QFont()
        font.setPointSize(14)
        self.SBRButton.setFont(font)
        self.SBRButton.setStyleSheet(u"background-color:salmon")

        self.verticalLayout.addWidget(self.SBRButton)

        self.CalibrationButton = QPushButton(self.groupBox_2)
        self.CalibrationButton.setObjectName(u"CalibrationButton")
        self.CalibrationButton.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.CalibrationButton.sizePolicy().hasHeightForWidth())
        self.CalibrationButton.setSizePolicy(sizePolicy1)
        self.CalibrationButton.setFont(font)
        self.CalibrationButton.setStyleSheet(u"background-color:cyan")

        self.verticalLayout.addWidget(self.CalibrationButton)

        self.SBTButton = QPushButton(self.groupBox_2)
        self.SBTButton.setObjectName(u"SBTButton")
        self.SBTButton.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.SBTButton.sizePolicy().hasHeightForWidth())
        self.SBTButton.setSizePolicy(sizePolicy1)
        self.SBTButton.setFont(font)
        self.SBTButton.setStyleSheet(u"background-color:violet")

        self.verticalLayout.addWidget(self.SBTButton)

        self.VerificationButton = QPushButton(self.groupBox_2)
        self.VerificationButton.setObjectName(u"VerificationButton")
        self.VerificationButton.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.VerificationButton.sizePolicy().hasHeightForWidth())
        self.VerificationButton.setSizePolicy(sizePolicy1)
        self.VerificationButton.setFont(font)
        self.VerificationButton.setStyleSheet(u"background-color:yellow")

        self.verticalLayout.addWidget(self.VerificationButton)

        self.PauseButton = QPushButton(self.groupBox_2)
        self.PauseButton.setObjectName(u"PauseButton")
        self.PauseButton.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.PauseButton.sizePolicy().hasHeightForWidth())
        self.PauseButton.setSizePolicy(sizePolicy1)
        self.PauseButton.setFont(font)
        self.PauseButton.setStyleSheet(u"background-color: lightblue")

        self.verticalLayout.addWidget(self.PauseButton)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.gridLayout.addWidget(self.groupBox_2, 2, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setEnabled(True)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMaximumSize(QSize(16777215, 16777215))
        self.groupBox_3.setSizeIncrement(QSize(0, 0))
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_4.setSpacing(11)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.stackedWidget = QStackedWidget(self.groupBox_3)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy1.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy1)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.page.setEnabled(True)
        self.verticalLayout_5 = QVBoxLayout(self.page)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.ImageLabel = QLabel(self.page)
        self.ImageLabel.setObjectName(u"ImageLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.ImageLabel.sizePolicy().hasHeightForWidth())
        self.ImageLabel.setSizePolicy(sizePolicy2)
        self.ImageLabel.setScaledContents(True)
        self.ImageLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.ImageLabel)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_2 = QGridLayout(self.page_2)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(15, -1, 15, -1)
        self.SBRRecordLabel = QLabel(self.page_2)
        self.SBRRecordLabel.setObjectName(u"SBRRecordLabel")
        font1 = QFont()
        font1.setPointSize(12)
        self.SBRRecordLabel.setFont(font1)
        self.SBRRecordLabel.setStyleSheet(u"background-color:gold")
        self.SBRRecordLabel.setAlignment(Qt.AlignCenter)
        self.SBRRecordLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.SBRRecordLabel, 0, 0, 1, 1)

        self.SBRTimeLabel = QLabel(self.page_2)
        self.SBRTimeLabel.setObjectName(u"SBRTimeLabel")
        self.SBRTimeLabel.setFont(font1)
        self.SBRTimeLabel.setStyleSheet(u"background-color:lightgray")
        self.SBRTimeLabel.setAlignment(Qt.AlignCenter)
        self.SBRTimeLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.SBRTimeLabel, 0, 3, 1, 1)

        self.CalLabel = QLabel(self.page_2)
        self.CalLabel.setObjectName(u"CalLabel")
        self.CalLabel.setFont(font1)
        self.CalLabel.setStyleSheet(u"background-color:lightgray")
        self.CalLabel.setAlignment(Qt.AlignCenter)
        self.CalLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.CalLabel, 1, 2, 1, 1)

        self.CalTimeLabel = QLabel(self.page_2)
        self.CalTimeLabel.setObjectName(u"CalTimeLabel")
        self.CalTimeLabel.setFont(font1)
        self.CalTimeLabel.setStyleSheet(u"background-color:lightgray")
        self.CalTimeLabel.setAlignment(Qt.AlignCenter)
        self.CalTimeLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.CalTimeLabel, 1, 3, 1, 1)

        self.SBTLabel = QLabel(self.page_2)
        self.SBTLabel.setObjectName(u"SBTLabel")
        self.SBTLabel.setFont(font1)
        self.SBTLabel.setStyleSheet(u"background-color:lightgray")
        self.SBTLabel.setAlignment(Qt.AlignCenter)
        self.SBTLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.SBTLabel, 2, 2, 1, 1)

        self.SBTTimeLabel = QLabel(self.page_2)
        self.SBTTimeLabel.setObjectName(u"SBTTimeLabel")
        self.SBTTimeLabel.setFont(font1)
        self.SBTTimeLabel.setStyleSheet(u"background-color:lightgray")
        self.SBTTimeLabel.setAlignment(Qt.AlignCenter)
        self.SBTTimeLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.SBTTimeLabel, 2, 3, 1, 1)

        self.VerificationLabel = QLabel(self.page_2)
        self.VerificationLabel.setObjectName(u"VerificationLabel")
        self.VerificationLabel.setFont(font1)
        self.VerificationLabel.setStyleSheet(u"background-color:lightgray")
        self.VerificationLabel.setAlignment(Qt.AlignCenter)
        self.VerificationLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.VerificationLabel, 3, 2, 1, 1)

        self.VerificationTimeLabel = QLabel(self.page_2)
        self.VerificationTimeLabel.setObjectName(u"VerificationTimeLabel")
        self.VerificationTimeLabel.setFont(font1)
        self.VerificationTimeLabel.setStyleSheet(u"background-color:lightgray")
        self.VerificationTimeLabel.setAlignment(Qt.AlignCenter)
        self.VerificationTimeLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.VerificationTimeLabel, 3, 3, 1, 1)

        self.SBRLabel = QLabel(self.page_2)
        self.SBRLabel.setObjectName(u"SBRLabel")
        self.SBRLabel.setFont(font1)
        self.SBRLabel.setStyleSheet(u"background-color:lightgray")
        self.SBRLabel.setAlignment(Qt.AlignCenter)
        self.SBRLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.SBRLabel, 0, 2, 1, 1)

        self.OverallLabel = QLabel(self.page_2)
        self.OverallLabel.setObjectName(u"OverallLabel")
        self.OverallLabel.setFont(font1)
        self.OverallLabel.setStyleSheet(u"background-color:lightgray")
        self.OverallLabel.setAlignment(Qt.AlignCenter)
        self.OverallLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.OverallLabel, 4, 2, 1, 1)

        self.OverallTimeLabel = QLabel(self.page_2)
        self.OverallTimeLabel.setObjectName(u"OverallTimeLabel")
        self.OverallTimeLabel.setFont(font1)
        self.OverallTimeLabel.setStyleSheet(u"background-color:lightgray")
        self.OverallTimeLabel.setAlignment(Qt.AlignCenter)
        self.OverallTimeLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.OverallTimeLabel, 4, 3, 1, 1)

        self.SBRRecordTimeLabel = QLabel(self.page_2)
        self.SBRRecordTimeLabel.setObjectName(u"SBRRecordTimeLabel")
        self.SBRRecordTimeLabel.setFont(font1)
        self.SBRRecordTimeLabel.setStyleSheet(u"background-color:gold")
        self.SBRRecordTimeLabel.setAlignment(Qt.AlignCenter)
        self.SBRRecordTimeLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.SBRRecordTimeLabel, 0, 1, 1, 1)

        self.CalRecordLabel = QLabel(self.page_2)
        self.CalRecordLabel.setObjectName(u"CalRecordLabel")
        self.CalRecordLabel.setFont(font1)
        self.CalRecordLabel.setStyleSheet(u"background-color:gold")
        self.CalRecordLabel.setAlignment(Qt.AlignCenter)
        self.CalRecordLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.CalRecordLabel, 1, 0, 1, 1)

        self.CalRecordTimeLabel = QLabel(self.page_2)
        self.CalRecordTimeLabel.setObjectName(u"CalRecordTimeLabel")
        self.CalRecordTimeLabel.setFont(font1)
        self.CalRecordTimeLabel.setStyleSheet(u"background-color:gold")
        self.CalRecordTimeLabel.setAlignment(Qt.AlignCenter)
        self.CalRecordTimeLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.CalRecordTimeLabel, 1, 1, 1, 1)

        self.SBTRecordLabel = QLabel(self.page_2)
        self.SBTRecordLabel.setObjectName(u"SBTRecordLabel")
        self.SBTRecordLabel.setFont(font1)
        self.SBTRecordLabel.setStyleSheet(u"background-color:gold")
        self.SBTRecordLabel.setAlignment(Qt.AlignCenter)
        self.SBTRecordLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.SBTRecordLabel, 2, 0, 1, 1)

        self.SBTRecordTimeLabel = QLabel(self.page_2)
        self.SBTRecordTimeLabel.setObjectName(u"SBTRecordTimeLabel")
        self.SBTRecordTimeLabel.setFont(font1)
        self.SBTRecordTimeLabel.setStyleSheet(u"background-color:gold")
        self.SBTRecordTimeLabel.setAlignment(Qt.AlignCenter)
        self.SBTRecordTimeLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.SBTRecordTimeLabel, 2, 1, 1, 1)

        self.VerificationRecordLabel = QLabel(self.page_2)
        self.VerificationRecordLabel.setObjectName(u"VerificationRecordLabel")
        self.VerificationRecordLabel.setFont(font1)
        self.VerificationRecordLabel.setStyleSheet(u"background-color:gold")
        self.VerificationRecordLabel.setAlignment(Qt.AlignCenter)
        self.VerificationRecordLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.VerificationRecordLabel, 3, 0, 1, 1)

        self.VerificationRecordTimeLabel = QLabel(self.page_2)
        self.VerificationRecordTimeLabel.setObjectName(u"VerificationRecordTimeLabel")
        self.VerificationRecordTimeLabel.setFont(font1)
        self.VerificationRecordTimeLabel.setStyleSheet(u"background-color:gold")
        self.VerificationRecordTimeLabel.setAlignment(Qt.AlignCenter)
        self.VerificationRecordTimeLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.VerificationRecordTimeLabel, 3, 1, 1, 1)

        self.OverallRecordLabel = QLabel(self.page_2)
        self.OverallRecordLabel.setObjectName(u"OverallRecordLabel")
        self.OverallRecordLabel.setFont(font1)
        self.OverallRecordLabel.setStyleSheet(u"background-color:gold")
        self.OverallRecordLabel.setAlignment(Qt.AlignCenter)
        self.OverallRecordLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.OverallRecordLabel, 4, 0, 1, 1)

        self.OverallRecordTimeLabel = QLabel(self.page_2)
        self.OverallRecordTimeLabel.setObjectName(u"OverallRecordTimeLabel")
        self.OverallRecordTimeLabel.setFont(font1)
        self.OverallRecordTimeLabel.setStyleSheet(u"background-color:gold")
        self.OverallRecordTimeLabel.setAlignment(Qt.AlignCenter)
        self.OverallRecordTimeLabel.setWordWrap(True)

        self.gridLayout_2.addWidget(self.OverallRecordTimeLabel, 4, 1, 1, 1)

        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout_2.addWidget(self.stackedWidget)

        self.TextLabel = QLabel(self.groupBox_3)
        self.TextLabel.setObjectName(u"TextLabel")
        sizePolicy1.setHeightForWidth(self.TextLabel.sizePolicy().hasHeightForWidth())
        self.TextLabel.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setPointSize(16)
        self.TextLabel.setFont(font2)
        self.TextLabel.setStyleSheet(u"background-color: lightgrey")
        self.TextLabel.setAlignment(Qt.AlignCenter)
        self.TextLabel.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.TextLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.PreviousButton = QPushButton(self.groupBox_3)
        self.PreviousButton.setObjectName(u"PreviousButton")
        self.PreviousButton.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.PreviousButton.sizePolicy().hasHeightForWidth())
        self.PreviousButton.setSizePolicy(sizePolicy1)
        self.PreviousButton.setFont(font2)
        self.PreviousButton.setStyleSheet(u"background-color:lightblue")

        self.horizontalLayout.addWidget(self.PreviousButton)

        self.ReadyToggle = QCheckBox(self.groupBox_3)
        self.ReadyToggle.setObjectName(u"ReadyToggle")
        self.ReadyToggle.setEnabled(True)
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.ReadyToggle.sizePolicy().hasHeightForWidth())
        self.ReadyToggle.setSizePolicy(sizePolicy3)

        self.horizontalLayout.addWidget(self.ReadyToggle)

        self.NextButton = QPushButton(self.groupBox_3)
        self.NextButton.setObjectName(u"NextButton")
        self.NextButton.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.NextButton.sizePolicy().hasHeightForWidth())
        self.NextButton.setSizePolicy(sizePolicy1)
        self.NextButton.setFont(font2)
        self.NextButton.setStyleSheet(u"background-color:lightblue")
        self.NextButton.setProperty("Ready", False)

        self.horizontalLayout.addWidget(self.NextButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout_2.setStretch(0, 10)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 1)

        self.horizontalLayout_4.addLayout(self.verticalLayout_2)


        self.gridLayout.addWidget(self.groupBox_3, 0, 1, 3, 1)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignCenter)
        self.formLayout.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.formLayout.setHorizontalSpacing(10)
        self.formLayout.setVerticalSpacing(10)
        self.PartNumberLabel = QLabel(self.groupBox)
        self.PartNumberLabel.setObjectName(u"PartNumberLabel")
        self.PartNumberLabel.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.PartNumberLabel)

        self.JobNumberLabel = QLabel(self.groupBox)
        self.JobNumberLabel.setObjectName(u"JobNumberLabel")
        self.JobNumberLabel.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.JobNumberLabel)

        self.JobNumberComboBox = QComboBox(self.groupBox)
        self.JobNumberComboBox.addItem("")
        self.JobNumberComboBox.setObjectName(u"JobNumberComboBox")
        self.JobNumberComboBox.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.JobNumberComboBox)

        self.PartNumberLineEdit = QLineEdit(self.groupBox)
        self.PartNumberLineEdit.setObjectName(u"PartNumberLineEdit")
        self.PartNumberLineEdit.setEnabled(False)
        sizePolicy.setHeightForWidth(self.PartNumberLineEdit.sizePolicy().hasHeightForWidth())
        self.PartNumberLineEdit.setSizePolicy(sizePolicy)
        self.PartNumberLineEdit.setFont(font)
        self.PartNumberLineEdit.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.PartNumberLineEdit)


        self.horizontalLayout_3.addLayout(self.formLayout)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        font3 = QFont()
        font3.setPointSize(8)
        self.groupBox_4.setFont(font3)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.ProgramStatusLabel = QLabel(self.groupBox_4)
        self.ProgramStatusLabel.setObjectName(u"ProgramStatusLabel")
        self.ProgramStatusLabel.setFont(font2)
        self.ProgramStatusLabel.setStyleSheet(u"background-color:lightgrey")
        self.ProgramStatusLabel.setAlignment(Qt.AlignCenter)
        self.ProgramStatusLabel.setWordWrap(True)
        self.ProgramStatusLabel.setMargin(10)

        self.verticalLayout_3.addWidget(self.ProgramStatusLabel)

        self.InfoLabel1 = QLabel(self.groupBox_4)
        self.InfoLabel1.setObjectName(u"InfoLabel1")
        font4 = QFont()
        font4.setFamilies([u"Arial"])
        font4.setPointSize(12)
        self.InfoLabel1.setFont(font4)
        self.InfoLabel1.setStyleSheet(u"background-color:lightgrey")
        self.InfoLabel1.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.InfoLabel1)

        self.InfoLabel2 = QLabel(self.groupBox_4)
        self.InfoLabel2.setObjectName(u"InfoLabel2")
        self.InfoLabel2.setFont(font4)
        self.InfoLabel2.setStyleSheet(u"background-color:lightgrey")
        self.InfoLabel2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.InfoLabel2)

        self.InfoLabel3 = QLabel(self.groupBox_4)
        self.InfoLabel3.setObjectName(u"InfoLabel3")
        self.InfoLabel3.setFont(font4)
        self.InfoLabel3.setStyleSheet(u"background-color:lightgrey")
        self.InfoLabel3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.InfoLabel3)

        self.InfoLabel4 = QLabel(self.groupBox_4)
        self.InfoLabel4.setObjectName(u"InfoLabel4")
        self.InfoLabel4.setFont(font4)
        self.InfoLabel4.setStyleSheet(u"background-color:lightgrey")
        self.InfoLabel4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.InfoLabel4)

        self.InfoLabel5 = QLabel(self.groupBox_4)
        self.InfoLabel5.setObjectName(u"InfoLabel5")
        self.InfoLabel5.setFont(font4)
        self.InfoLabel5.setStyleSheet(u"background-color:lightgrey")
        self.InfoLabel5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.InfoLabel5)

        self.InfoLabel6 = QLabel(self.groupBox_4)
        self.InfoLabel6.setObjectName(u"InfoLabel6")
        self.InfoLabel6.setFont(font4)
        self.InfoLabel6.setStyleSheet(u"background-color:lightgrey")
        self.InfoLabel6.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.InfoLabel6)

        self.InfoLabel7 = QLabel(self.groupBox_4)
        self.InfoLabel7.setObjectName(u"InfoLabel7")
        self.InfoLabel7.setFont(font4)
        self.InfoLabel7.setStyleSheet(u"background-color:lightgrey")
        self.InfoLabel7.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.InfoLabel7)

        self.InfoLabel8 = QLabel(self.groupBox_4)
        self.InfoLabel8.setObjectName(u"InfoLabel8")
        self.InfoLabel8.setFont(font4)
        self.InfoLabel8.setStyleSheet(u"background-color:lightgrey")
        self.InfoLabel8.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.InfoLabel8)


        self.gridLayout.addWidget(self.groupBox_4, 1, 0, 1, 1)

        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 7)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1118, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Controls", None))
        self.CalToggle.setText(QCoreApplication.translate("MainWindow", u"Skip SBR?", None))
        self.VeriToggle.setText(QCoreApplication.translate("MainWindow", u"Skip SBT?", None))
        self.SBRButton.setText(QCoreApplication.translate("MainWindow", u"SBR INSTALLATION", None))
        self.CalibrationButton.setText(QCoreApplication.translate("MainWindow", u"CALIBRATION", None))
        self.SBTButton.setText(QCoreApplication.translate("MainWindow", u"SBT INSTALLATION", None))
        self.VerificationButton.setText(QCoreApplication.translate("MainWindow", u"VERIFICATION", None))
        self.PauseButton.setText(QCoreApplication.translate("MainWindow", u"PAUSE", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Program Window", None))
        self.ImageLabel.setText(QCoreApplication.translate("MainWindow", u"Assy Images", None))
        self.SBRRecordLabel.setText(QCoreApplication.translate("MainWindow", u"SBR Time Monthly Record", None))
        self.SBRTimeLabel.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.CalLabel.setText(QCoreApplication.translate("MainWindow", u"Calibration Setup Time:", None))
        self.CalTimeLabel.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.SBTLabel.setText(QCoreApplication.translate("MainWindow", u"SBT Time:", None))
        self.SBTTimeLabel.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.VerificationLabel.setText(QCoreApplication.translate("MainWindow", u"Verification Setup Time:", None))
        self.VerificationTimeLabel.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.SBRLabel.setText(QCoreApplication.translate("MainWindow", u"SBR Time:", None))
        self.OverallLabel.setText(QCoreApplication.translate("MainWindow", u"Overall time:", None))
        self.OverallTimeLabel.setText(QCoreApplication.translate("MainWindow", u"00:00:00", None))
        self.SBRRecordTimeLabel.setText(QCoreApplication.translate("MainWindow", u"99:99:99", None))
        self.CalRecordLabel.setText(QCoreApplication.translate("MainWindow", u"Cal Setup Time Monthly Record", None))
        self.CalRecordTimeLabel.setText(QCoreApplication.translate("MainWindow", u"99:99:99", None))
        self.SBTRecordLabel.setText(QCoreApplication.translate("MainWindow", u"SBT Time Monthly Record", None))
        self.SBTRecordTimeLabel.setText(QCoreApplication.translate("MainWindow", u"99:99:99", None))
        self.VerificationRecordLabel.setText(QCoreApplication.translate("MainWindow", u"Verifictation Time Monthly Record", None))
        self.VerificationRecordTimeLabel.setText(QCoreApplication.translate("MainWindow", u"99:99:99", None))
        self.OverallRecordLabel.setText(QCoreApplication.translate("MainWindow", u"Overall Time Monthly Record", None))
        self.OverallRecordTimeLabel.setText(QCoreApplication.translate("MainWindow", u"99:99:99", None))
        self.TextLabel.setText(QCoreApplication.translate("MainWindow", u"Assy Instructions", None))
        self.PreviousButton.setText(QCoreApplication.translate("MainWindow", u"Previous", None))
        self.ReadyToggle.setText(QCoreApplication.translate("MainWindow", u"Ready?", None))
        self.NextButton.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Setup", None))
        self.PartNumberLabel.setText(QCoreApplication.translate("MainWindow", u"Part #:", None))
        self.JobNumberLabel.setText(QCoreApplication.translate("MainWindow", u"Job #:", None))
        self.JobNumberComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"N/A", None))

        self.PartNumberLineEdit.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Status", None))
        self.ProgramStatusLabel.setText(QCoreApplication.translate("MainWindow", u"Waiting for operator to select job order", None))
        self.InfoLabel1.setText(QCoreApplication.translate("MainWindow", u"Info_1", None))
        self.InfoLabel2.setText(QCoreApplication.translate("MainWindow", u"Info_2", None))
        self.InfoLabel3.setText(QCoreApplication.translate("MainWindow", u"Info_3", None))
        self.InfoLabel4.setText(QCoreApplication.translate("MainWindow", u"Info_4", None))
        self.InfoLabel5.setText(QCoreApplication.translate("MainWindow", u"Info_5", None))
        self.InfoLabel6.setText(QCoreApplication.translate("MainWindow", u"Info_6", None))
        self.InfoLabel7.setText(QCoreApplication.translate("MainWindow", u"Info_7", None))
        self.InfoLabel8.setText(QCoreApplication.translate("MainWindow", u"Info_8", None))
    # retranslateUi

