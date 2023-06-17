from PySide6 import QtGui
from PySide6.QtGui import QTextOption
from PySide6.QtWidgets import QApplication, QGridLayout, QSizePolicy, QLabel, QWidget


class myQLabel(QLabel):
    def __init__(self, *args, **kargs):
        super(myQLabel, self).__init__(*args, **kargs)

        self.setSizePolicy(QSizePolicy(QSizePolicy.Ignored,
                                             QSizePolicy.Ignored))

        self.setMinSize(5)
        self.setWordWrap(True)

    def setMinSize(self, minfs):

        f = self.font()
        f.setPixelSize(minfs)
        br = QtGui.QFontMetrics(f).boundingRect(self.text())

        self.setMinimumSize(br.width(), br.height())

    def resizeEvent(self, event):
        super(myQLabel, self).resizeEvent(event)

        if not self.text():
            return

        #--- fetch current parameters ----

        f = self.font()
        cr = self.contentsRect()

        #--- find the font size that fits the contentsRect ---

        fs = 1
        while True:

            f.setPixelSize(fs)
            br = QtGui.QFontMetrics(f).boundingRect(self.text())

            if br.height() <= cr.height() and br.width() <= cr.width():
                fs += 1
            else:
                f.setPixelSize(max(fs - 1, 1)) # backtrack
                break

        #--- update font size ---

        self.setFont(f)


class myApplication(QWidget):
    def __init__(self, parent=None):
        super(myApplication, self).__init__(parent)

        #---- Prepare a Layout ----

        grid = QGridLayout()

        for i in range(1):
            grid.addWidget(myQLabel('some text'), i, 0)
            grid.setRowStretch(i, i+1)
            grid.setRowMinimumHeight(i, 5)

        self.setLayout(grid)
        self.resize(500, 300)


if __name__ == '__main__':

    app = QApplication()

    instance = myApplication()
    instance.show()

    app.exec()