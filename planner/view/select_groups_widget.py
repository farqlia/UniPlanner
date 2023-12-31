from typing import List, Callable

from PySide6.QtCore import (QMetaObject, QRect,
                            Qt)
from PySide6.QtGui import (QDropEvent)
from PySide6.QtWidgets import (QAbstractItemView, QComboBox, QGroupBox, QLabel, QListWidget, QListWidgetItem,
                               QWidget)

from planner.models.classes_utils import find_course_by_code, find_group_by_code
from planner.models.groups import Group, Course, GroupCategory
from planner.utils.datetime_utils import TIME_FORMAT, WEEK_TYPE_POLISH_FORM


def add_groups_to_list(course: Course, group_codes: List[str], list_widget: QListWidget):
    for group_code in group_codes:
        list_widget.addItem(format_group_to_string(find_group_by_code(course.groups, group_code)))


class DragDropList(QListWidget):

    def __init__(self, parent, category):
        super(DragDropList, self).__init__(parent)
        self.category = category
        self.currently_selected_course = None
        self.drop_event_listener = None

    def dropEvent(self, event: QDropEvent) -> None:
        super(DragDropList, self).dropEvent(event)
        if isinstance(event.source(), DragDropList) and event.source() != self:
            source_list = event.source()
            source_list.update_groups()
            self.update_groups()
        self.drop_event_listener()

    def update_groups(self):
        for i in range(self.count()):
            group = find_group_by_code(self.currently_selected_course.groups,
                        extract_group_code(self.item(i).text()))
            group.category = self.category


class DragDropListDisableOnCondition(DragDropList):

    def __init__(self, parent, category, condition):
        super(DragDropListDisableOnCondition, self).__init__(parent, category)
        self.condition = condition

    def update_items(self):
        for i in range(self.count()):
            should_be_disabled = self.condition(self, self.item(i))
            if should_be_disabled:
                disable_item(self.item(i))
            else:
                enable_item(self.item(i))


def enable_item(item):
    item.setFlags(Qt.ItemFlag.ItemIsEnabled
                              | Qt.ItemFlag.ItemIsDragEnabled
                              | Qt.ItemFlag.ItemIsDropEnabled
                              | Qt.ItemFlag.ItemIsSelectable)


def disable_item(item):
    item.setFlags(Qt.ItemFlag.NoItemFlags)


def disable_if_in_excluded_area(grid_widget, wlist: DragDropListDisableOnCondition, item: QListWidgetItem):
    gcode = extract_group_code(item.text())
    group = find_group_by_code(wlist.currently_selected_course.groups,
                               gcode)
    return grid_widget.is_group_in_excluded_area(group)


class SelectGroupsWidget:

    def __init__(self, parent: QWidget, grid_widget, width=340, height=440):
        self.parent = parent
        self.parent.resize(width, height)
        widgets_width = int(0.9 * width)
        x_offset = int(0.05 * width)

        self.courses: List[Course] = []
        self.current_course = None

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
        self.label_preferred.setText("Preferred")
        self.label_preferred.setObjectName(u"label_preferred")
        self.label_preferred.setGeometry(QRect(x_offset, 100, widgets_width, 16))

        self.list_of_preferred_choices = DragDropList(self.group_box_select_courses, GroupCategory.PREFERRED)
        self.list_of_preferred_choices.drop_event_listener = grid_widget.update
        self.list_of_preferred_choices.setObjectName(u"list_of_preferred_choices")
        self.list_of_preferred_choices.setGeometry(QRect(x_offset, 120, widgets_width, 81))
        self.list_of_preferred_choices.setDragDropMode(QAbstractItemView.DragDrop)
        self.list_of_preferred_choices.setDefaultDropAction(Qt.MoveAction)

        self.label_neutral = QLabel(self.group_box_select_courses)
        self.label_neutral.setText("Neutral")
        self.label_neutral.setObjectName(u"label_neutral")
        self.label_neutral.setGeometry(QRect(x_offset, 210, widgets_width, 16))

        self.list_of_neutral_choices = DragDropList(self.group_box_select_courses, GroupCategory.NEUTRAL)
        self.list_of_neutral_choices.drop_event_listener = grid_widget.update
        self.list_of_neutral_choices.setObjectName(u"list_of_neutral_choices")
        self.list_of_neutral_choices.setGeometry(QRect(x_offset, 230, widgets_width, 81))
        self.list_of_neutral_choices.setDragDropMode(QAbstractItemView.DragDrop)
        self.list_of_neutral_choices.setDefaultDropAction(Qt.MoveAction)

        self.label_excluded = QLabel(self.group_box_select_courses)
        self.label_excluded.setText("Excluded")
        self.label_excluded.setObjectName(u"label_excluded")
        self.label_excluded.setGeometry(QRect(x_offset, 320, widgets_width, 20))

        self.list_of_excluded_choices = DragDropListDisableOnCondition(self.group_box_select_courses,
                                                                       GroupCategory.EXCLUDED,
                                                                       lambda w, i: disable_if_in_excluded_area(grid_widget, w, i))
        # This is not working because it overrides category to excluded
        # TODO : make it work
        def condition():
            self.list_of_excluded_choices.update_items()
            self.parent.update()

        grid_widget.add_listener_on_excluding_areas(condition)
        self.list_of_excluded_choices.drop_event_listener = grid_widget.update
        # self.add_listener_for_group_change(self.list_of_excluded_choices.update_items)
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

        for course in courses:
            self.courses_combo_box.addItem(format_course_to_string(course))

        self.display_groups_of_course()

    def display_groups_of_course(self):
        self.clear_lists()
        # Each row in a list widget is a string, so we need to find the corresponding Course object by code
        course = find_course_by_code(self.courses, extract_course_code(self.courses_combo_box.currentText()))
        self.set_course_displayed_by_lists(course)
        for group in course.groups:
            self.map_list_widget_to_category[group.category].addItem(format_group_to_string(group))

    def clear_lists(self):
        self.list_of_preferred_choices.clear()
        self.list_of_neutral_choices.clear()
        self.list_of_excluded_choices.clear()

    def set_course_displayed_by_lists(self, course):
        for widget_list in self.map_list_widget_to_category.values():
            widget_list.currently_selected_course = course

    def update_on_course_change(self):
        self.assign_groups_to_categories()
        self.display_groups_of_course()

    def assign_groups_to_categories(self):
        for widget_list in self.map_list_widget_to_category.values():
            widget_list.update_groups()

    def add_listener_for_group_change(self, listener: Callable):
        self.list_of_neutral_choices.itemChanged.connect(listener)
        self.list_of_preferred_choices.itemChanged.connect(listener)
        self.list_of_excluded_choices.itemChanged.connect(listener)


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
