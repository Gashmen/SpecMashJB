import sys

from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem,QGraphicsRectItem
from PyQt5.QtCore import Qt, QPointF,QRect

class StayObject(QGraphicsRectItem):
    def __init__(self,x,y,w,h):
        super().__init__(x,y,w,h)
        self.setRect(x,y,w,h)
        self.setBrush(Qt.blue)

    '''
    Изменение курсора при наведение на объект
    hoverEnterEvent - при наведение во внутрь объекта
    hoverLeaveEvent - при отведение от объекта
    '''
    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.SizeAllСursor)

    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()


    def mousePressEvent(self, event):
        print(self.scenePos())

        pass

    def mouseMoveEvent(self, event):
        # orig_cursor_position = event.lastScenePos()
        # updated_cursor_position = event.scenePos()
        #
        # orig_position = self.scenePos()
        #
        # updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        # updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        # self.setPos(QPointF(updated_cursor_x, updated_cursor_y))
        pass


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
        print(self.pos())
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
        self.stayobj = StayObject(200,200,300,400)
        self.scene.addItem(self.stayobj)
        # print(self.stayobj.pos())
        self.moveObject = MovingObject(50, 50, 40)
        # self.moveObject2 = MovingObject(100, 100, 100)
        self.scene.addItem(self.moveObject)

    # def mousePressEvent(self, event):
    #     # super().mousePressEvent()
    #     if event.button() == Qt.LeftButton:
    #         # получаем координаты мыши на QGraphicsView
    #         pos = event.pos()
    #         # преобразуем координаты в координаты сцены
    #         scene_pos = self.mapToScene(pos)
    #         print("Координаты мыши на QGraphicsView:", pos.x(), pos.y())
    #         print("Координаты мыши на QGraphicsScene:", scene_pos.x(), scene_pos.y())




app = QApplication(sys.argv)
view = GraphicView()
view.show()
sys.exit(app.exec_())