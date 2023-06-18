import sys

from PySide6.QtWidgets import QApplication

from planner.view.login_window import LoginWindow
from planner.controller.controller import download_to_file


def is_login_successful(login, password):
    # download_to_file(login, password)
    return True


if __name__ == "__main__":
    app = QApplication()

    instance = LoginWindow(is_login_successful)
    instance.show()

    app.exec()

