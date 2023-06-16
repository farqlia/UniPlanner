from dataclasses import dataclass

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform, QDropEvent, QDragEnterEvent, QDragLeaveEvent, QDragMoveEvent)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
                               QGroupBox, QLabel, QListWidget, QListWidgetItem,
                               QSizePolicy, QWidget, QMainWindow)
from typing import List, Dict
from planner.models.groups import Group, Course, DayOfWeek, WeekType, GroupCategory
from planner.models.classes_utils import find_course_by_code, find_group_by_code
from planner.view.view_utils import create_class
from planner.utils.datetime_utils import as_hour, TIME_FORMAT, WEEK_TYPE_POLISH_FORM


@dataclass
class CategorizedGroups:
    # Store only code of a group
    categorized_groups: Dict[GroupCategory, List[str]]


def add_groups_to_list(course: Course, group_codes: List[str], list_widget: QListWidget):
    for group_code in group_codes:
        list_widget.addItem(format_group_to_string(find_group_by_code(course.classes, group_code)))

'''
class DragAndDropList(QListWidget):

    def __init__(self, *args):
        super(DragAndDropList, self).__init__(*args)

    def dropEvent(self, event: QDropEvent) -> None:
        super(DragAndDropList, self).dropEvent(event)
        # drop_item = self.itemAt(event.posF())
        drop_item = self.itemAt(event.pos().x(), event.pos().y())
        # drop_item_text = drop_item.text()
        # print(drop_item_text)
        # print(drop_item)
        # print(type(drop_item))

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        super(DragAndDropList, self).dragMoveEvent(event)
        # drop_item = self.itemAt(event.posF())
        drop_item = self.itemAt(event.pos())
        # drop_item_text = drop_item.text()
        # print(drop_item_text)
        print(drop_item)
        print(type(drop_item))
'''

class SelectGroupsWidget:

    def __init__(self, parent: QWidget, courses: List[Course]):

        self.parent = parent
        self.parent.resize(411, 460)

        self.courses: List[Course] = courses
        # Store by course code because class 'Course' is unhashable
        self.courses_to_categorized_groups: Dict[str, CategorizedGroups] = {}

        for course in self.courses:
            self.courses_to_categorized_groups[course.code] = CategorizedGroups({k: [] for k in list(GroupCategory)})

        self.group_box_select_courses = QGroupBox(parent)
        self.group_box_select_courses.setObjectName(u"group_box_select_courses")
        self.group_box_select_courses.setGeometry(QRect(20, 10, 371, 441))

        self.courses_combo_box = QComboBox(self.group_box_select_courses)
        self.courses_combo_box.setObjectName(u"courses_combo_box")
        self.courses_combo_box.setGeometry(QRect(20, 50, 321, 20))

        for course in courses:
            self.courses_combo_box.addItem(format_course_to_string(course))
            for group in course.classes:
                self.courses_to_categorized_groups[course.code].categorized_groups[GroupCategory.NEUTRAL]\
                    .append(group.code)

        self.courses_combo_box.setEditable(False)
        self.courses_combo_box.setCurrentText("")
        self.courses_combo_box.currentIndexChanged.connect(self.display_groups_of_course)

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
        self.list_of_preferable_choices.setObjectName(u"list_of_preferable_choices")
        self.list_of_preferable_choices.setGeometry(QRect(20, 120, 321, 81))
        self.list_of_preferable_choices.setDragDropMode(QAbstractItemView.DragDrop)
        self.list_of_preferable_choices.setDefaultDropAction(Qt.MoveAction)
        self.retranslateUi()

        # Temporary solution, then we'll fit this widget to the number of groups
        self.map_list_widget_to_category = {GroupCategory.PREFERABLE: self.list_of_preferable_choices,
                                            GroupCategory.NEUTRAL: self.list_of_neutral_choices,
                                            GroupCategory.EXCLUDED: self.list_of_excluded_choices}

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

    def display_groups_of_course(self):
        self.clear_lists()
        # Each row in a list widget is a string, so we need to find the corresponding Course object by code
        course = find_course_by_code(self.courses, extract_course_code(self.courses_combo_box.currentText()))
        for category in list(GroupCategory):
            add_groups_to_list(
                course,
                # For a given course and given category
                self.courses_to_categorized_groups[course.code].categorized_groups[category],
                self.map_list_widget_to_category[category])

    def clear_lists(self):
        self.list_of_preferable_choices.clear()
        self.list_of_neutral_choices.clear()
        self.list_of_excluded_choices.clear()

    def update_categorized_groups(self, course):
        for category in GroupCategory:
            self.update_groups_for_category(course, category)

    def update_groups_for_category(self, course, category):
        self.courses_to_categorized_groups[course.code].categorized_groups[category].clear()
        for i in range(self.map_list_widget_to_category[category].count()):
            self.courses_to_categorized_groups[course.code].categorized_groups[category]\
                .append(self.map_list_widget_to_category[category].item(i))


def format_course_to_string(course: Course):
    return course.code + ", " + course.name


def extract_course_code(course_repr: str):
    return course_repr.split(", ")[0]


def extract_group_code(group_repr: str):
    return group_repr.split(", ")[0]


def format_group_to_string(class_: Group):
    return class_.code + ", " + class_.day.name.lower() + \
           ("/" + WEEK_TYPE_POLISH_FORM[class_.week_type] if len(
               WEEK_TYPE_POLISH_FORM[class_.week_type]) > 0 else "") + " " + \
           class_.start_time.strftime(TIME_FORMAT) + "-" + class_.end_time.strftime(TIME_FORMAT)


if __name__ == "__main__":

    app = QApplication()
    window = QMainWindow()

    test_courses = [Course("Bazy danych", "INZ002007C", "", classes=[create_class(DayOfWeek.Monday, WeekType.ODD_WEEK,
                                                                                  as_hour("9:15"), as_hour("11:00"), "K01-17a"),
                                                                     create_class(DayOfWeek.Monday, WeekType.EVEN_WEEK,
                                                                                  as_hour("9:15"), as_hour("11:00"), "K01-17b"),
                                                                     create_class(DayOfWeek.Tuesday, WeekType.ODD_WEEK,
                                                                                  as_hour("9:15"), as_hour("11:00"), "K01-17c"),
                                                                     create_class(DayOfWeek.Tuesday, WeekType.EVEN_WEEK,
                                                                                  as_hour("9:15"), as_hour("11:00"),"K01-17c"),
                                                                     ]),
                    Course("Metody systemowe i decyzyjne", "INZ002008L", "", classes=[create_class(DayOfWeek.Wednesday, WeekType.ODD_WEEK,
                                                                                                   as_hour("13:15"), as_hour("15:00"), "K01-21a"),
                                                                                      create_class(DayOfWeek.Wednesday, WeekType.ODD_WEEK,
                                                                                                   as_hour("15:15"), as_hour("16:55"), "K01-21b"),
                                                                                      create_class(DayOfWeek.Wednesday,
                                                                                                   WeekType.EVEN_WEEK,
                                                                                                   as_hour("15:15"),
                                                                                                   as_hour("16:55"),
                                                                                                   "K01-21d")]),
                    Course("Języki skryptowe", "INZ002009L", "", classes=[create_class(DayOfWeek.Monday, WeekType.EVERY_WEEK,
                                                                                       as_hour("13:15"), as_hour("15:00"), "K01-23b"),
                                                                          create_class(DayOfWeek.Monday, WeekType.EVERY_WEEK,
                                                                                       as_hour("15:15"), as_hour("16:55"), "K01-23c"),
                                                                          create_class(DayOfWeek.Tuesday, WeekType.EVERY_WEEK, as_hour("17:05"),
                                                                                       as_hour("18:45"), "K01-23e"),
                                                                          create_class(DayOfWeek.Friday, WeekType.EVERY_WEEK,
                                                                                       as_hour("11:15"), as_hour("13:00"), "K01-28g")])
    ]

    select_groups_widget = SelectGroupsWidget(window, test_courses)
    window.show()
    app.exec()
