# import random
# import sys
#
# from PyQt5 import QtCore, QtGui, QtWidgets
#
#
# class Window(QtWidgets.QMainWindow):
#     def __init__(self):
#         super(Window, self).__init__()
#
#         self.rect = QtCore.QRect()
#         self.drag_position = QtCore.QPoint()
#
#         button = QtWidgets.QPushButton("Add", self)
#         button.clicked.connect(self.on_clicked)
#
#         self.resize(640, 480)
#
#     @QtCore.pyqtSlot()
#     def on_clicked(self):
#         if self.rect.isNull():
#             self.rect = QtCore.QRect(
#                 QtCore.QPoint(*random.sample(range(200), 2)), QtCore.QSize(100, 100)
#             )
#             self.update()
#
#     def paintEvent(self, event):
#         super().paintEvent(event)
#         if not self.rect.isNull():
#             painter = QtGui.QPainter(self)
#             painter.setRenderHint(QtGui.QPainter.Antialiasing)
#             painter.setPen(QtGui.QPen(QtCore.Qt.black, 5, QtCore.Qt.SolidLine))
#             painter.drawEllipse(self.rect)
#
#     def mousePressEvent(self, event):
#         if (
#             2 * QtGui.QVector2D(event.pos() - self.rect.center()).length()
#             < self.rect.width()
#         ):
#             self.drag_position = event.pos() - self.rect.topLeft()
#         super().mousePressEvent(event)
#
#     def mouseMoveEvent(self, event):
#         if not self.drag_position.isNull():
#             self.rect.moveTopLeft(event.pos() - self.drag_position)
#             self.update()
#         super().mouseMoveEvent(event)
#
#     def mouseReleaseEvent(self, event):
#         self.drag_position = QtCore.QPoint()
#         super().mouseReleaseEvent(event)
#
#
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     Rect = Window()
#     Rect.show()
#     sys.exit(app.exec_())

import sys

from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem,QGraphicsRectItem
from PyQt5.QtCore import Qt, QPointF,QRect

class StayObject(QGraphicsRectItem):
    def __init__(self,x,y,w,h):
        super().__init__(x,y,w,h)
        self.setRect(x,y,w,h)
        self.setBrush(Qt.blue)

    # mouse hover event
    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.SizeAllCursor)

    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()

    # mouse click event
    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))



class MovingObject(QGraphicsEllipseItem):
    def __init__(self, x, y, r):
        super().__init__(0, 0, r, r)
        self.setPos(x, y)
        self.setBrush(Qt.blue)
        self.setAcceptHoverEvents(True)

    # mouse hover event
    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.SizeAllCursor)

    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()

    # mouse click event
    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))

class GraphicView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 1200, 1000)
        # self.rectangle = QRect(200,200,500,500)

        self.moveObject = MovingObject(50, 50, 40)
        # self.moveObject2 = MovingObject(100, 100, 100)
        self.scene.addItem(self.moveObject)
        self.stayobj = StayObject(200,200,300,400)
        self.scene.addItem(self.stayobj)
        # self.scene.addItem(self.moveObject2)


app = QApplication(sys.argv)
view = GraphicView()
view.show()
sys.exit(app.exec_())