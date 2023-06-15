from PySide6.QtCore import QSize
from PySide6.QtGui import QPainter, QFontMetrics, QFont
from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout, QApplication, QPlainTextEdit


class VerticalLabel(QLabel):

    def __init__(self, *args):
        QLabel.__init__(self, *args)

    def paintEvent(self, event):
        painter = QPainter(self)
        fm = QFontMetrics(painter.font())
        painter.translate(0, self.height())
        painter.rotate(-90)
        # calculate the size of the font
        xoffset = int(fm.boundingRect(self.text()).width() / 2)
        yoffset = int(fm.boundingRect(self.text()).height() / 2)
        x = int(self.width() / 2)
        y = int(self.height() / 2)
        # because we rotated the label, x affects the vertical placement, and y affects the horizontal
        painter.drawText(x, y,  self.text())
        painter.end()

    def minimumSizeHint(self):
        size = QLabel.minimumSizeHint(self)
        return QSize(size.height(), size.width())

    def sizeHint(self):
        size = QLabel.sizeHint(self)
        return QSize(size.height(), size.width())


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        lbl1 = VerticalLabel('ABSOLUTE')
        # lbl1.setFont(QFont('Arial', 20))
        lbl1.setStyleSheet("QLabel { background-color : black; color : orange; }");
        lbl2 = VerticalLabel('lbl 2')
        lbl3 = VerticalLabel('lbl 3')
        hBoxLayout = QHBoxLayout()

        for i in range(10):
            hBoxLayout.addWidget(VerticalLabel(f'lbl {i}'))

        self.setLayout(hBoxLayout)
        self.setGeometry(300, 300, 100, 100)
        self.show()

def main():
    app = QApplication()
    ex = Example()
    app.exec()

if __name__ == '__main__':
    main()