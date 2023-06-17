from PySide6 import QtGui, QtCore
from PySide6.QtCore import (QMetaObject, QObject, QRect,
                            Qt, QPoint)
from PySide6.QtGui import (QFont, QCursor, QPalette, QBrush, QColor)
from PySide6.QtWidgets import (QApplication, QTextEdit, QWidget, QMainWindow, QGridLayout, QLabel, QFrame)
from planner.models.groups import Group, DayOfWeek, WeekType, GroupCategory, GroupType
from datetime import datetime, timedelta
from typing import Iterable, List, Dict
from planner.utils.datetime_utils import get_eng_day_abbr, get_day_from_int, as_hour, TIME_FORMAT
from planner.view.view_utils import create_group, POLISH_GROUP_TYPE

BLACK = (0, 0, 0, 255)
GREEN = (0, 170, 0, 255)
RED = (170, 39, 39, 255)
GROUP_CATEGORY_COLORS = {GroupCategory.NEUTRAL: BLACK, GroupCategory.EXCLUDED: RED,
                         GroupCategory.PREFERRED: GREEN}

COLOR_FOR_GROUP_TYPE = {GroupType.LECTURE: (24, 131, 22), GroupType.PRACTICALS: (255, 191, 80),
                        GroupType.LABORATORY: (22, 166, 218)}


# TODO: add tool-tip with group details
class GroupWidget(QFrame):

    def __init__(self, parent: QObject, group: Group, x, y, width, height):
        super(GroupWidget, self).__init__(parent)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.group = group
        self.color_margin = 2
        self.color = COLOR_FOR_GROUP_TYPE[group.type]

        self.font_size = 0

        self.group_description = QTextEdit(self)
        self.group_description.setReadOnly(True)
        self.set_description()
        self.group_description.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.group_description.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.change_font_color()

    def setGeometry(self, arg__1: QRect) -> None:
        super(GroupWidget, self).setGeometry(arg__1)
        self.setAutoFillBackground(False)
        r_2 = QRect(self.color_margin, self.color_margin, arg__1.width() - 2 * self.color_margin,
                  arg__1.height() - 2 * self.color_margin)
        self.group_description.setGeometry(r_2)
        self.setStyleSheet("background-color: rgb({}, {}, {});"
                           .format(*self.color))
        self.group_description.setStyleSheet("background-color: rgb({}, {}, {});"
                           .format(255, 255, 255))

    def set_description(self):
        self.group_description.append(POLISH_GROUP_TYPE[self.group.type] + " " + self.group.course.name)
        label = QLabel()
        label.setFont(self.group_description.font())
        label.setText(self.group.course.name)
        print(label.width())

        # if self.height > 2 * self.font_size:
          #   self.group_description.append(self.group.start_time.strftime(TIME_FORMAT)
            #                          + " - " + self.group.end_time.strftime(TIME_FORMAT))

    def change_font_color(self):
        palette = QPalette()
        brush = QBrush(QColor(*GROUP_CATEGORY_COLORS[self.group.category]))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        self.group_description.setPalette(palette)
        self.update()

    def change_font_size(self, size):
        font = QFont()
        font.setFamilies([u"Arial Unicode MS"])
        self.font_size = size
        font.setPixelSize(self.font_size)
        self.setFont(font)
        self.group_description.setFont(font)
        self.update()

    def set_group_category(self, new_cat: GroupCategory):
        self.group.category = new_cat
        self.change_font_color()

# A panel to place courses for a given day of week
# We assume that 1 minute = 1 unit of width
# The total width should be computed based on all possible groups
# (usually it is 7-21, but could be 7-22/7-23)
# Height depends on whether we include Saturday & Sunday


def overlap_along_x_axis(group_widget_1: GroupWidget, group_widget_2: GroupWidget):
    return group_widget_1.x <= group_widget_2.x <= group_widget_1.x + group_widget_1.width or \
           group_widget_2.x <= group_widget_1.x <= group_widget_2.x + group_widget_2.width


def does_group_intersect_rectangles(group: GroupWidget, day_of_week_excluded_areas: List[QRect]):
    for r in day_of_week_excluded_areas:
        if group.geometry().intersects(r):
            return True
    return False


class DayOfWeekWidget(QWidget):

    # x, y are positions regarding the 'widget_group' widget
    def __init__(self, day_of_week: DayOfWeek, parent: QObject, time_0: datetime, x, y, width, height, label_width) -> None:
        super().__init__(parent)
        self.day_of_week = day_of_week
        self.offset_from_edge = 2
        self.setGeometry(QRect(x, y, width + label_width, height))
        self.time_0 = time_0
        self.group_widgets: List[GroupWidget] = []      # all groups currently placed - sorted by x cooridnate

        self.label_width = label_width

        day_label = QTextEdit(self)
        day_label.setTextInteractionFlags(Qt.NoTextInteraction)
        day_label.setGeometry(0, 0, label_width, height)
        day_label.setReadOnly(True)
        day_label.setText(get_eng_day_abbr(day_of_week))

        self.begin = QPoint()
        self.end = QPoint()

        self.can_paint_rectangles = False

        self.rectangles: List[QRect] = []

        self.release_mouse_listener = []

    def inform_listeners(self):
        for listener in self.release_mouse_listener:
            listener()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40))
        qp.setBrush(br)
        if self.can_paint_rectangles:
            if not self.begin.isNull() and not self.end.isNull():
                qp.drawRect(QRect(self.begin, self.end).normalized())

        self.paint_rectangles(qp)


    def paint_rectangles(self, qp):
        for r in self.rectangles:
            qp.drawRect(r)
            
    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        self.update()
        super(DayOfWeekWidget, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()
        super(DayOfWeekWidget, self).mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        if self.can_paint_rectangles:
            self.remove_rectangle(event.pos())
        super(DayOfWeekWidget, self).mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        if self.can_paint_rectangles:
            if self.begin != self.end:
                r = QRect(self.get_geometry()).normalized()
                i = 0
                while i < len(self.rectangles) and (r.x() >= self.rectangles[i].x() or r.intersects(self.rectangles[i])):
                    if r.intersects(self.rectangles[i]):
                        r = r.united(self.rectangles[i])
                        self.rectangles.pop(i)
                    else:
                        i += 1
                self.rectangles.insert(i, r)

        self.begin = self.end = QPoint()
        self.update()
        self.mark_group_widgets_as_intersecting()
        super(DayOfWeekWidget, self).mouseReleaseEvent(event)

    def get_geometry(self):
        width = abs(self.end.x() - self.begin.x())
        height = self.height()
        return QRect(min(self.begin.x(), self.end.x()), 0, width, height)

    def remove_rectangle(self, p: QPoint):
        i = 0
        while i < len(self.rectangles):
            if self.rectangles[i].contains(p):
                self.reset_widgets_color_if_intersect(self.rectangles.pop(i))
                self.inform_listeners()
                i = len(self.rectangles)
            i += 1

    def get_rectangles(self):
        return list(self.rectangles)

    def compute_x(self, group: Group):
        return self.label_width + int((group.start_time - self.time_0).total_seconds() / 60.0)

    def place_group_widget(self, group: Group):
        x = self.compute_x(group)
        y = self.offset_from_edge
        width = group.durance
        height = self.height()
        group_widget = GroupWidget(self, group, x, y, width, height)
        group_widget.setObjectName(group.code)
        self.add_to_list(group_widget)

    def add_to_list(self, group_widget: GroupWidget):
        i = 0
        overlapping_widgets: List[GroupWidget] = []

        while i < len(self.group_widgets) and group_widget.x <= self.group_widgets[i].x:
            if overlap_along_x_axis(group_widget, self.group_widgets[i]):
                overlapping_widgets.append(self.group_widgets[i])
            i += 1

        overlapping_widgets.append(group_widget)
        self.group_widgets.insert(i, group_widget)
        i += 1

        while i < len(self.group_widgets) and overlap_along_x_axis(group_widget, self.group_widgets[i]):
            overlapping_widgets.append(self.group_widgets[i])
            i += 1

        new_height = int((self.height() - 2 * self.offset_from_edge) / len(overlapping_widgets))
        # sorted_widgets = sorted(overlapping_widgets, key=lambda w: (w.x, w.y))

        for i, widget in enumerate(overlapping_widgets):
            widget.setGeometry(QRect(widget.x, self.offset_from_edge + i * new_height, widget.width, new_height))
            widget.change_font_size(int(min(new_height / 2, 12)))

    # This will be used by select groups widget to add excluded groups there
    def mark_group_widgets_as_intersecting(self):
        for w in self.group_widgets:
            if does_group_intersect_rectangles(w, self.rectangles):
                w.set_group_category(GroupCategory.EXCLUDED)
        self.inform_listeners()

    def reset_widgets_color_if_intersect(self, rectangle: QRect):
        for w in self.group_widgets:
            if rectangle.intersects(w.geometry()):
                w.set_group_category(GroupCategory.NEUTRAL)
        self.inform_listeners()

    def is_in_excluded_area(self, group: Group):
        return does_group_intersect_rectangles(self.findChild(GroupWidget, group.code),
                                               self.rectangles)


class GridWidget:

    def __init__(self, parent: QWidget, cell_height: int, n_days_of_week: int,
                 start_time: datetime, end_time: datetime) -> None:

        # What time range we consider
        self.start_time = start_time
        self.end_time = end_time
        self.cell_height = cell_height
        self.height = n_days_of_week * cell_height
        self.n_minutes = int((end_time - start_time).total_seconds() / 60.0)
        self.width = self.n_minutes
        x_offset = 0
        y_offset = 0

        self.time_widget_height = 30
        self.days_of_week_labels_widget_width = 60
        self.n_days_of_week = n_days_of_week

        parent.resize(self.width + self.days_of_week_labels_widget_width, self.height + self.time_widget_height)

        self.days_of_weeks_widgets: List[DayOfWeekWidget] = [None for _ in range(n_days_of_week)]

        self.widget = QWidget(parent)
        self.widget.setGeometry(QRect(x_offset, y_offset, self.width + self.days_of_week_labels_widget_width,
                                self.time_widget_height + self.height))

        print(self.widget.geometry())

        self.widget_time = QWidget(self.widget)
        self.widget_time.setObjectName(u"widget_time")
        self.widget_time.setGeometry(QRect(self.days_of_week_labels_widget_width, 0,
                                           self.width,
                                           self.time_widget_height))

        self.main_grid_widget = QWidget(self.widget)
        self.main_grid_widget.setObjectName(u"main_grid_widget")
        self.main_grid_widget.setGeometry(QRect(0,
                                                self.time_widget_height, self.widget.width(), self.height))

        self.add_days_of_week_widgets()
        self.add_minutes_labels()

        print(self.main_grid_widget.geometry())

        # self.retranslateUi(parent)
        QMetaObject.connectSlotsByName(parent)

    # 1 through 7
    def add_day_of_week_widget(self, day_of_week: int):
        index_day_of_week = day_of_week - 1
        self.days_of_weeks_widgets[index_day_of_week] = DayOfWeekWidget(get_day_from_int(day_of_week),
                                                                        self.main_grid_widget,
                                                                        self.start_time, 0,
                                                                        index_day_of_week * self.cell_height,
                                                                        self.width, self.cell_height,
                                                                        self.days_of_week_labels_widget_width)

    def add_days_of_week_widgets(self):
        for i in range(1, self.n_days_of_week + 1):
            self.add_day_of_week_widget(i)

    def add_group_widget(self, group: Group, day_of_week: int):
        if 1 <= day_of_week <= self.n_days_of_week:
            index_day_of_week = day_of_week - 1
            self.days_of_weeks_widgets[index_day_of_week].place_group_widget(group)

    def add_minutes_labels(self):
        font = QFont()
        font.setFamilies([u"Arial Unicode MS"])
        font.setPointSize(8)
        self.widget_time.setFont(font)

        time_interval_in_minutes = 30
        # This will always be 2
        rows_of_time_label = 2

        n_intervals = self.n_minutes / time_interval_in_minutes
        n_intervals += int(n_intervals % 2)

        n_labels = int(n_intervals / rows_of_time_label)

        def generate_labels(start_time, n_labels):
            return [start_time + timedelta(minutes=i * (rows_of_time_label * time_interval_in_minutes))
                    for i in range(n_labels)]

        upper_labels = generate_labels(self.start_time, n_labels + 1)
        lower_labels = generate_labels(datetime.strptime((self.start_time
                                        + timedelta(minutes=time_interval_in_minutes)).strftime(TIME_FORMAT), TIME_FORMAT),
                                       n_labels + int(n_intervals % 2))

        self.place_labels(upper_labels, 0)
        self.place_labels(lower_labels, int(self.time_widget_height / rows_of_time_label))

    def place_labels(self, time_labels: List[datetime], y):
        for t_label in time_labels:
            x = (t_label - self.start_time).total_seconds() / 60.0
            label = QLabel(self.widget_time)
            label.setText(t_label.strftime(TIME_FORMAT))
            label.setGeometry(QRect(x, y, 30, int(self.time_widget_height / 2)))

    def add_groups(self, groups: Iterable[Group]):
        for group in groups:
            index_day_of_week = group.day.value - 1
            if 0 <= index_day_of_week < self.n_days_of_week:
                self.days_of_weeks_widgets[index_day_of_week].place_group_widget(group)

    def change_cursor(self, new_cursor):
        self.main_grid_widget.setCursor(QCursor(new_cursor))

    def set_can_exclude_area(self, can_set):
        for widget in self.days_of_weeks_widgets:
            widget.can_paint_rectangles = can_set

    def add_listener_on_excluding_areas(self, listener):
        for widget in self.days_of_weeks_widgets:
            widget.release_mouse_listener.append(listener)

    def update(self):
        for w in self.days_of_weeks_widgets:
            for gw in w.group_widgets:
                gw.change_font_color()
                gw.update()

    def is_group_in_excluded_area(self, group: Group) -> bool:
        print(group)
        print(self.days_of_weeks_widgets[group.day.value - 1])
        return self.days_of_weeks_widgets[group.day.value - 1].is_in_excluded_area(group)


if __name__ == "__main__":

    app = QApplication()
    window = QMainWindow()
    grid = GridWidget(window, 120, 5, datetime.strptime("7:00", "%H:%M"), datetime.strptime("21:00", "%H:%M"))

    test_groups = [create_group(DayOfWeek.Monday, WeekType.EVERY_WEEK, as_hour("7:30"), as_hour("9:00"), "K01-30a"),
                   create_group(DayOfWeek.Monday, WeekType.EVERY_WEEK, as_hour("8:00"), as_hour("10:00"), "K01-30b"),
                   create_group(DayOfWeek.Monday, WeekType.EVERY_WEEK, as_hour("7:30"), as_hour("10:00"), "K01-30c"),
                   create_group(DayOfWeek.Monday, WeekType.EVERY_WEEK, as_hour("11:15"), as_hour("13:00"), "K01-30d"),
                   create_group(DayOfWeek.Monday, WeekType.EVERY_WEEK, as_hour("11:15"), as_hour("13:00"), "K01-30e"),
                   create_group(DayOfWeek.Monday, WeekType.EVERY_WEEK, as_hour("11:15"), as_hour("13:00"), "K01-30o"),
                   create_group(DayOfWeek.Monday, WeekType.EVERY_WEEK, as_hour("11:15"), as_hour("13:00"), "K01-30o"),
                   create_group(DayOfWeek.Monday, WeekType.EVERY_WEEK, as_hour("11:15"), as_hour("13:00"), "K01-30i"),
                   create_group(DayOfWeek.Monday, WeekType.EVERY_WEEK, as_hour("11:15"), as_hour("13:00"), "K01-30f"),
                   create_group(DayOfWeek.Monday, WeekType.EVERY_WEEK, as_hour("11:15"), as_hour("13:00"), "K01-30g"),
                   create_group(DayOfWeek.Monday, WeekType.EVERY_WEEK, as_hour("11:15"), as_hour("13:00"), "K01-30h"),
                   create_group(DayOfWeek.Friday, WeekType.EVERY_WEEK, as_hour("11:15"), as_hour("13:00"), "K01-31c"),
                   create_group(DayOfWeek.Friday, WeekType.EVERY_WEEK, as_hour("11:15"), as_hour("13:00"), "K01-31d")]

    grid.add_groups(test_groups)
    window.show()
    app.exec()