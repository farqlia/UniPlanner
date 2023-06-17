from PySide6.QtWidgets import QApplication

from planner.controller.controller import get_courses
from planner.view.main_view import MainWindow


if __name__ == "__main__":

    courses = get_courses()
    app = QApplication()
    window = MainWindow()
    window.load_courses(courses)
    window.show()
    app.exec()
