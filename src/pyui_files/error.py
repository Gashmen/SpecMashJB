# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'error.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog


class Ui_WidgetError(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Error Window')
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Error_listwidget = QtWidgets.QListWidget()
        self.Error_listwidget.setObjectName("Error_listwidget")
        self.horizontalLayout.addWidget(self.Error_listwidget)
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, WidgetError):
        _translate = QtCore.QCoreApplication.translate
        WidgetError.setWindowTitle(_translate("WidgetError", "Form"))

    def add_error(self, str_error):
        self.Error_listwidget.addItem(str_error)