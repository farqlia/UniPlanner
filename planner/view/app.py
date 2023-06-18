from PySide6.QtWidgets import QApplication

from planner.controller.controller import download_to_file, get_courses
from planner.view.main_view import MainWindow
from planner.view.login_window import do_login


# TODO: to be implemented
def is_login_correct(login, password):
    return True


def run_app(login, password):
    # download_to_file(login, password)
    main_window = MainWindow()
    main_window.load_courses(get_courses())
    main_window.show()


if __name__ == "__main__":

    do_login(is_login_correct, run_app)

