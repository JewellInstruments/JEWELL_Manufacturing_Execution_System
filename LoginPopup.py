# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LoginPopup.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(299, 106)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.loginButton = QPushButton(Dialog)
        self.loginButton.setObjectName(u"loginButton")

        self.gridLayout.addWidget(self.loginButton, 1, 0, 1, 1)

        self.cancelButton = QPushButton(Dialog)
        self.cancelButton.setObjectName(u"cancelButton")

        self.gridLayout.addWidget(self.cancelButton, 1, 1, 1, 1)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.usernameLabel = QLabel(Dialog)
        self.usernameLabel.setObjectName(u"usernameLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.usernameLabel)

        self.usernameLineEdit = QLineEdit(Dialog)
        self.usernameLineEdit.setObjectName(u"usernameLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.usernameLineEdit)

        self.passwordLabel = QLabel(Dialog)
        self.passwordLabel.setObjectName(u"passwordLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.passwordLabel)

        self.passwordLineEdit = QLineEdit(Dialog)
        self.passwordLineEdit.setObjectName(u"passwordLineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.passwordLineEdit)


        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.loginButton.setText(QCoreApplication.translate("Dialog", u"Login", None))
        self.cancelButton.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.usernameLabel.setText(QCoreApplication.translate("Dialog", u"Username", None))
        self.usernameLineEdit.setText("")
        self.passwordLabel.setText(QCoreApplication.translate("Dialog", u"Password", None))
    # retranslateUi

