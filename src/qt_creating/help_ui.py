
from PyQt5 import QtCore, QtGui, QtWidgets

class ClssDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ClssDialog, self).__init__(parent)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textLabel = QtWidgets.QLabel()
        self.textLabel.setObjectName("HelpLabel")
        self.verticalLayout.addWidget(self.textLabel)
        self.setWindowTitle("Help Window")
        self.textLabel.setText("Version 0.0.2")

    def btnClosed(self):
        self.close()