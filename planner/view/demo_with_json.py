from PySide6.QtWidgets import QApplication

from planner.parsing.parse_json import load_from_json
from planner.view.main_view import MainWindow

if __name__ == "__main__":
    path = r"..\..\data\courses.json"

    courses = load_from_json(path)
    app = QApplication()
    window = MainWindow()
    window.load_courses(courses)
    window.show()
    app.exec()
