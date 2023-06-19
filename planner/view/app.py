from PySide6.QtWidgets import QApplication

from planner.view.login_window import LoginWindow

if __name__ == "__main__":
    app = QApplication()

    instance = LoginWindow()
    instance.show()

    app.exec()

