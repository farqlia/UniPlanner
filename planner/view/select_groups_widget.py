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
from planner.view.view_utils import create_group
from planner.utils.datetime_utils import as_hour, TIME_FORMAT, WEEK_TYPE_POLISH_FORM


@dataclass
class CategorizedGroups:
    # Store only code of a group
    categorized_groups: Dict[GroupCategory, List[str]]


def add_groups_to_list(course: Course, group_codes: List[str], list_widget: QListWidget):
    for group_code in group_codes:
        list_widget.addItem(format_group_to_string(find_group_by_code(course.groups, group_code)))


class SelectGroupsWidget:

    def __init__(self, parent: QWidget, width=340, height=440):

        self.parent = parent
        self.parent.resize(width, height)
        widgets_width = int(0.9 * width)
        x_offset = int(0.05 * width)

        self.courses: List[Course] = []
        self.current_course = None
        # Store by course code because class 'Course' is unhashable
        self.courses_to_categorized_groups: Dict[str, CategorizedGroups] = {}

        self.group_box_select_courses = QGroupBox(parent)
        self.group_box_select_courses.setTitle("Select groups")
        self.group_box_select_courses.setObjectName(u"group_box_select_courses")
        self.group_box_select_courses.setGeometry(QRect(0, 10, width, 441))

        self.label_select_courses = QLabel(self.group_box_select_courses)
        self.label_select_courses.setObjectName(u"label_2")
        self.label_select_courses.setGeometry(QRect(x_offset, 20, 49, 16))

        self.courses_combo_box = QComboBox(self.group_box_select_courses)
        self.courses_combo_box.setObjectName(u"courses_combo_box")
        self.courses_combo_box.setGeometry(QRect(x_offset, 50, widgets_width, 20))

        self.label_choose_course = QLabel(self.group_box_select_courses)
        self.label_choose_course.setText("Choose course")
        self.label_choose_course.setObjectName(u"label_choose_course")
        self.label_choose_course.setGeometry(QRect(x_offset, 30, widgets_width, 20))

        self.courses_combo_box.setEditable(False)
        self.courses_combo_box.setCurrentText("Choose course")
        self.courses_combo_box.currentIndexChanged.connect(self.update_on_course_change)

        self.label_preferred = QLabel(self.group_box_select_courses)
        self.label_preferred.setText("Prefered")
        self.label_preferred.setObjectName(u"label_preferred")
        self.label_preferred.setGeometry(QRect(x_offset, 100, widgets_width, 16))

        self.list_of_preferred_choices = QListWidget(self.group_box_select_courses)
        self.list_of_preferred_choices.setObjectName(u"list_of_preferred_choices")
        self.list_of_preferred_choices.setGeometry(QRect(x_offset, 120, widgets_width, 81))
        self.list_of_preferred_choices.setDragDropMode(QAbstractItemView.DragDrop)
        self.list_of_preferred_choices.setDefaultDropAction(Qt.MoveAction)

        self.label_neutral = QLabel(self.group_box_select_courses)
        self.label_neutral.setText("Neutral")
        self.label_neutral.setObjectName(u"label_neutral")
        self.label_neutral.setGeometry(QRect(x_offset, 210, widgets_width, 16))

        self.list_of_neutral_choices = QListWidget(self.group_box_select_courses)
        self.list_of_neutral_choices.setObjectName(u"list_of_neutral_choices")
        self.list_of_neutral_choices.setGeometry(QRect(x_offset, 230, widgets_width, 81))
        self.list_of_neutral_choices.setDragDropMode(QAbstractItemView.DragDrop)
        self.list_of_neutral_choices.setDefaultDropAction(Qt.MoveAction)

        self.label_excluded = QLabel(self.group_box_select_courses)
        self.label_excluded.setText("Excluded")
        self.label_excluded.setObjectName(u"label_excluded")
        self.label_excluded.setGeometry(QRect(x_offset, 320, widgets_width, 20))

        self.list_of_excluded_choices = QListWidget(self.group_box_select_courses)
        self.list_of_excluded_choices.setObjectName(u"list_of_excluded_choices")
        self.list_of_excluded_choices.setGeometry(QRect(x_offset, 340, widgets_width, 81))
        self.list_of_excluded_choices.setDragDropMode(QAbstractItemView.DragDrop)
        self.list_of_excluded_choices.setDefaultDropAction(Qt.MoveAction)

        self.map_list_widget_to_category = {GroupCategory.PREFERRED: self.list_of_preferred_choices,
                                            GroupCategory.NEUTRAL: self.list_of_neutral_choices,
                                            GroupCategory.EXCLUDED: self.list_of_excluded_choices}

        QMetaObject.connectSlotsByName(parent)

    def load_courses(self, courses: List[Course]):
        self.courses = courses
        self.current_course = courses[0]

        for course in self.courses:
            self.courses_to_categorized_groups[course.code] = CategorizedGroups({k: [] for k in list(GroupCategory)})

        for course in courses:
            self.courses_combo_box.addItem(format_course_to_string(course))
            for group in course.groups:
                self.courses_to_categorized_groups[course.code].categorized_groups[GroupCategory.NEUTRAL]\
                    .append(group.code)

        self.display_groups_of_course()

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
        self.list_of_preferred_choices.clear()
        self.list_of_neutral_choices.clear()
        self.list_of_excluded_choices.clear()

    def update_on_course_change(self):
        self.update_categorized_groups(self.current_course)
        self.current_course = find_course_by_code(self.courses,
                                                  extract_course_code(self.courses_combo_box.currentText()))
        self.display_groups_of_course()

    def update_categorized_groups(self, course):
        for category in list(GroupCategory):
            self.update_groups_for_category(course, category)

    def update_groups_for_category(self, course, category):
        self.courses_to_categorized_groups[course.code].categorized_groups[category].clear()
        for i in range(self.map_list_widget_to_category[category].count()):
            self.courses_to_categorized_groups[course.code].categorized_groups[category]\
                .append(extract_group_code(self.map_list_widget_to_category[category].item(i).text()))


def format_course_to_string(course: Course):
    return course.code + ", " + course.name


def extract_course_code(course_repr: str):
    return course_repr.split(", ")[0]


def extract_group_code(group_repr: str):
    return group_repr.split(", ")[0]


def format_group_to_string(group: Group):
    return group.code + ", " + group.day.name.lower() + \
           ("/" + WEEK_TYPE_POLISH_FORM[group.week_type] if len(
               WEEK_TYPE_POLISH_FORM[group.week_type]) > 0 else "") + " " + \
           group.start_time.strftime(TIME_FORMAT) + "-" + group.end_time.strftime(TIME_FORMAT) \
           + ", " + str(group.lecturer)


if __name__ == "__main__":

    app = QApplication()
    window = QMainWindow()

    test_courses = [Course("Bazy danych", "INZ002007C", "", groups=[create_group(DayOfWeek.Monday, WeekType.ODD_WEEK,
                                                                                 as_hour("9:15"), as_hour("11:00"), "K01-17a"),
                                                                    create_group(DayOfWeek.Monday, WeekType.EVEN_WEEK,
                                                                                 as_hour("9:15"), as_hour("11:00"), "K01-17b"),
                                                                    create_group(DayOfWeek.Tuesday, WeekType.ODD_WEEK,
                                                                                 as_hour("9:15"), as_hour("11:00"), "K01-17c"),
                                                                    create_group(DayOfWeek.Tuesday, WeekType.EVEN_WEEK,
                                                                                 as_hour("9:15"), as_hour("11:00"),"K01-17d"),
                                                                    ]),
                    Course("Metody systemowe i decyzyjne", "INZ002008L", "", groups=[create_group(DayOfWeek.Wednesday, WeekType.ODD_WEEK,
                                                                                                  as_hour("13:15"), as_hour("15:00"), "K01-21a"),
                                                                                     create_group(DayOfWeek.Wednesday, WeekType.ODD_WEEK,
                                                                                                  as_hour("15:15"), as_hour("16:55"), "K01-21b"),
                                                                                     create_group(DayOfWeek.Wednesday,
                                                                                                  WeekType.EVEN_WEEK,
                                                                                                  as_hour("15:15"),
                                                                                                  as_hour("16:55"),
                                                                                                   "K01-21d")]),
                    Course("Języki skryptowe", "INZ002009L", "", groups=[create_group(DayOfWeek.Monday, WeekType.EVERY_WEEK,
                                                                                      as_hour("13:15"), as_hour("15:00"), "K01-23b"),
                                                                         create_group(DayOfWeek.Monday, WeekType.EVERY_WEEK,
                                                                                      as_hour("15:15"), as_hour("16:55"), "K01-23c"),
                                                                         create_group(DayOfWeek.Tuesday, WeekType.EVERY_WEEK, as_hour("17:05"),
                                                                                      as_hour("18:45"), "K01-23e"),
                                                                         create_group(DayOfWeek.Friday, WeekType.EVERY_WEEK,
                                                                                      as_hour("11:15"), as_hour("13:00"), "K01-28g")])
    ]

    select_groups_widget = SelectGroupsWidget(window)
    select_groups_widget.load_courses(test_courses)
    window.show()
    app.exec()
