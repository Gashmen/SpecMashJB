#python -m PyQt5.uic.pyuic error.ui -o error.py
import os

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

import src.pyui_files.error as error_ui

class Mainver(QtWidgets.QWidget, error_ui.Ui_WidgetError):

    def __init__(self):
        '''БАЗА ПРИ ЗАПУСКЕ'''
        super().__init__()

        self.setupUi(self)

    def add_error(self,list_errors):
        self.Error_listwidget.addItems(list_errors)
