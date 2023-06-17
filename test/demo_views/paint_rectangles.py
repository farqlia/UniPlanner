import sys

from PySide6.QtCore import QPoint, Qt, QRect
from PySide6.QtGui import QIcon, QPainter, QPen
from PySide6.QtWidgets import QApplication, QWidget


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(150, 250, 500, 500)
        self.setWindowTitle("Ammyyy")
        self.setWindowIcon(QIcon("a.jpeg"))

        self.begin = QPoint()
        self.end = QPoint()
        self.rectangles = []

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setPen(QPen(Qt.black, 6, Qt.SolidLine))

        for rectangle in self.rectangles:
            qp.drawRect(rectangle)

        if not self.begin.isNull() and not self.end.isNull():
            qp.drawRect(QRect(self.begin, self.end).normalized())

    def mousePressEvent(self, event):
        self.begin = self.end = event.pos()
        self.update()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        r = QRect(self.begin, self.end).normalized()
        self.rectangles.append(r)
        self.begin = self.end = QPoint()
        self.update()
        super().mouseReleaseEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())