from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QMouseEvent, QCursor, QPalette, QColor, QPainter
from PyQt5.QtCore import Qt, QMimeData


class Circle(QGraphicsEllipseItem):
    def __init__(self, x, y, r):
        super().__init__(x, y, r, r)
        self.setCursor(QCursor(Qt.OpenHandCursor))
        self.setAcceptDrops(True)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.setCursor(QCursor(Qt.ClosedHandCursor))

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        QMouseEvent.accept(event)
        self.setPos(event.scenePos())
        if self.collidesWithItem(square):
            print(F'Circle coords: {event.scenePos()}')


class Square(QGraphicsEllipseItem):
    def __init__(self, size):
        super().__init__(0, 0, size, size)
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable, False)
        self.setBrush(QColor(Qt.green))


class View(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasFormat(QMimeData):
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        if event.mimeData().hasFormat(QMimeData):
            x = event.scenePos().x() - r / 2
            y = event.scenePos().y() - r / 2
            self.scene().addItem(Circle(x, y, r))
            event.acceptProposedAction()


if __name__ == '__main__':
    app = QApplication([])
    scene = QGraphicsScene()
    view = View(scene)
    view.setFixedSize(800, 800)
    square = Square(100)
    square.setPos(300, 300)
    scene.addItem(square)
    r = 20
    circle1 = Circle(100, 100, r)
    circle2 = Circle(200, 200, r)
    circle3 = Circle(400, 350, r)
    scene.addItem(circle1)
    scene.addItem(circle2)
    scene.addItem(circle3)
    view.show()
    app.exec()