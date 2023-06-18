import sys

from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QDialog, QLabel, QApplication


class W1(QWidget):
    def __init__(self, parent=None):
        super(W1, self).__init__(parent)
        self.btn = QPushButton('Click1')

        vb = QVBoxLayout()
        vb.addWidget(self.btn)
        self.setLayout(vb)

        self.btn.clicked.connect(self.fireupWindows2)

    def fireupWindows2(self):
        w2 = W2()
        if w2.exec_():
            self.w3 = W3()
            self.w3.show()

class W2(QDialog):
    def __init__(self, parent=None):
        super(W2, self).__init__(parent)

        self.btn = QPushButton('Click2')

        vb = QVBoxLayout()
        vb.addWidget(self.btn)
        self.setLayout(vb)

        self.btn.clicked.connect(self.fireupWindows3)

    def fireupWindows3(self):
        self.accept()

class W3(QWidget):
    def __init__(self, parent=None):
        super(W3, self).__init__(parent)
        self.resize(300, 300)
        self.btn = QLabel('The Last Window')

        vb = QVBoxLayout()
        vb.addWidget(self.btn)
        self.setLayout(vb)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = W1()
    w.show()
    sys.exit(app.exec_())