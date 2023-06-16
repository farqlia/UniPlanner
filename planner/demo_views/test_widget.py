from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow


class MyWidget(QWidget):
    def __init__(self, parent, width, height):
        super().__init__(parent)
        self.setGeometry(30,30,600,400)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40))
        qp.setBrush(br)
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        self.update()


if __name__ == "__main__":

    app = QApplication()
    window = QMainWindow()
    widget = MyWidget(window)
    window.show()
    app.exec()