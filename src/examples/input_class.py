import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, geom_button):
        super(MainWindow, self).__init__()
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Demo Room")
        self.geom_button = geom_button
        self.buttons = {}
        self.add_buttons()

    def add_buttons(self):
        for i, geom in enumerate(self.geom_button):
            self.btn = QtWidgets.QPushButton(self.central_widget)
            self.btn.clicked.connect(lambda ch, i=i: self.onLight(i))
            self.btn.setGeometry(*geom)
            path_image = "img/lightOff.png"
            qss = 'border-image: url({})'.format(path_image)
            self.btn.setStyleSheet(qss)
            self.buttons[i] = (self.btn, 0)

    def onLight(self, i):
        if self.buttons[i][1]:
            self.buttons[i][0].setStyleSheet('border-image: url({})'.format("img/lightOff.png"))
            self.buttons[i] = (self.buttons[i][0], 0)
        else:
            self.buttons[i][0].setStyleSheet('border-image: url({})'.format("img/lightOn.png"))
            self.buttons[i] = (self.buttons[i][0], 1)


geom_button = [
    (330, 70, 20, 30), (270, 110, 20, 20), (300, 110, 30, 30), (360, 110, 40, 40), (330, 150, 50, 50),
    (180, 190, 20, 30), (240, 190, 20, 20), (300, 190, 30, 30), (360, 190, 40, 40), (210, 230, 50, 50),
    (270, 230, 20, 30), (330, 230, 20, 20), (180, 270, 30, 30), (240, 270, 40, 40), (270, 270, 50, 50),
    (300, 270, 20, 30), (360, 270, 20, 20), (210, 310, 30, 30), (330, 310, 40, 40), (180, 350, 50, 50),
    (240, 350, 20, 30), (300, 350, 20, 20), (360, 350, 30, 30), (210, 390, 40, 40), (270, 390, 50, 50),
    (330, 390, 20, 30), (180, 430, 20, 20), (240, 430, 30, 30), (300, 430, 40, 40), (360, 430, 50, 50),
    (400, 230, 256, 256)
]

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(geom_button)
    w.resize(800, 640)
    w.show()
    sys.exit(app.exec_())