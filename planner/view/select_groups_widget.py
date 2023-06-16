from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
                               QGroupBox, QLabel, QListWidget, QListWidgetItem,
                               QSizePolicy, QWidget, QMainWindow)
from typing import List
from planner.models.classes import Class, Course

class SelectGroupsWidget:

    def __init__(self, parent: QWidget):

        self.parent = parent
        self.parent.resize(411, 460)

        self.group_box_select_courses = QGroupBox(parent)
        self.group_box_select_courses.setObjectName(u"group_box_select_courses")
        self.group_box_select_courses.setGeometry(QRect(20, 10, 371, 441))

        self.courses_combo_box = QComboBox(self.group_box_select_courses)
        self.courses_combo_box.setObjectName(u"courses_combo_box")
        self.courses_combo_box.setGeometry(QRect(20, 50, 321, 20))

        self.list_of_neutral_choices = QListWidget(self.group_box_select_courses)
        self.list_of_neutral_choices.setObjectName(u"list_of_neutral_choices")
        self.list_of_neutral_choices.setGeometry(QRect(20, 230, 321, 81))
        self.list_of_neutral_choices.setDragDropMode(QAbstractItemView.DragDrop)
        self.list_of_neutral_choices.setDefaultDropAction(Qt.MoveAction)

        self.list_of_excluded_choices = QListWidget(self.group_box_select_courses)
        self.list_of_excluded_choices.setObjectName(u"list_of_excluded_choices")
        self.list_of_excluded_choices.setGeometry(QRect(20, 340, 321, 81))
        self.list_of_excluded_choices.setDragDropMode(QAbstractItemView.DragDrop)
        self.list_of_excluded_choices.setDefaultDropAction(Qt.MoveAction)

        self.label_2 = QLabel(self.group_box_select_courses)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 20, 49, 16))
        self.label_choose_course = QLabel(self.group_box_select_courses)

        self.label_choose_course.setObjectName(u"label_choose_course")
        self.label_choose_course.setGeometry(QRect(20, 30, 321, 20))
        self.label_preferable = QLabel(self.group_box_select_courses)

        self.label_preferable.setObjectName(u"label_preferable")
        self.label_preferable.setGeometry(QRect(20, 100, 321, 16))
        self.label_neutral = QLabel(self.group_box_select_courses)

        self.label_neutral.setObjectName(u"label_neutral")
        self.label_neutral.setGeometry(QRect(20, 210, 321, 16))
        self.label_excluded = QLabel(self.group_box_select_courses)

        self.label_excluded.setObjectName(u"label_excluded")
        self.label_excluded.setGeometry(QRect(20, 320, 321, 20))
        self.list_of_preferable_choices = QListWidget(self.group_box_select_courses)

        QListWidgetItem(self.list_of_preferable_choices)
        self.list_of_preferable_choices.setObjectName(u"list_of_preferable_choices")
        self.list_of_preferable_choices.setGeometry(QRect(20, 120, 321, 81))
        self.list_of_preferable_choices.setDragDropMode(QAbstractItemView.DragDrop)
        self.list_of_preferable_choices.setDefaultDropAction(Qt.MoveAction)

        self.retranslateUi()

        QMetaObject.connectSlotsByName(parent)
    # setupUi

    def retranslateUi(self):
        self.parent.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.group_box_select_courses.setTitle(QCoreApplication.translate("Form", u"Select groups", None))
        self.label_2.setText("")
        self.label_choose_course.setText(QCoreApplication.translate("Form", u"Choose course ", None))
        self.label_preferable.setText(QCoreApplication.translate("Form", u"Preferable", None))
        self.label_neutral.setText(QCoreApplication.translate("Form", u"Neutral", None))
        self.label_excluded.setText(QCoreApplication.translate("Form", u"Excluded", None))

    def add_courses(self, courses: List[Class]):
        pass


if __name__ == "__main__":

    app = QApplication()
    window = QMainWindow()

    test_courses = []

    SelectGroupsWidget(window)
    window.show()
    app.exec()
