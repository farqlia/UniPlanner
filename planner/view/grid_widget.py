from PySide6.QtCore import (QMetaObject, QObject, QRect,
                            Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QApplication, QTextEdit, QWidget, QMainWindow, QGridLayout)
from planner.models.groups import Group, DayOfWeek, WeekType
from datetime import datetime, timedelta
from typing import Iterable, List
from planner.utils.datetime_utils import get_eng_day_abbr, get_day_from_int, as_hour, TIME_FORMAT
from planner.view.view_utils import create_class


class ClassWidget(QWidget):

    def __init__(self, parent: QObject, class_: Group, x, y, width, height):
        super(ClassWidget, self).__init__(parent)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.class_ = class_

        self.setFixedWidth(width)
        self.setGeometry(QRect(x, y, width, height))
        class_description = QTextEdit(self)
        class_description.setGeometry(QRect(0, 0, width, height))
        class_description.setReadOnly(True)
        # class_description.setCursor(QCursor(Qt.ArrowCursor))
        class_description.append(class_.code)
        class_description.append(class_.start_time.strftime(TIME_FORMAT)
                                 + " - " + class_.end_time.strftime(TIME_FORMAT))
        class_description.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        class_description.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)


# A panel to place courses for a given day of week
# We assume that 1 minute = 1 unit of width
# The total width should be computed based on all possible classes
# (usually it is 7-21, but could be 7-22/7-23)
# Height depends on whether we include Saturday & Sunday
def overlap_along_x_axis(class_widget_1: ClassWidget, class_widget_2: ClassWidget):
    return class_widget_1.x <= class_widget_2.x <= class_widget_1.x + class_widget_1.width or \
           class_widget_2.x <= class_widget_1.x <= class_widget_2.x + class_widget_2.width


class DayOfWeekWidget(QWidget):

    # x, y are positions regarding the 'widget_classes' widget
    def __init__(self, day_of_week: str, parent: QObject, time_0: datetime, x, y, width, height, label_width) -> None:
        super().__init__(parent)
        self.setGeometry(QRect(x, y, width + label_width, height))
        self.time_0 = time_0
        self.widgets = []      # all classes currently placed - sorted by x cooridnate

        self.label_width = label_width

        day_label = QTextEdit(self)
        day_label.setTextInteractionFlags(Qt.NoTextInteraction)
        day_label.setGeometry(0, 0, label_width, height)
        day_label.setReadOnly(True)
        day_label.setText(day_of_week)

        self.layout = QGridLayout(self)

        self.setLayout(self.layout)

    def place_class_widget(self, class_: Group):
        x = self.label_width + int((class_.start_time - self.time_0).total_seconds() / 60.0)
        y = 0
        width = class_.durance
        height = self.height()
        class_widget = ClassWidget(self, class_, x, y, width, height)
        self.add_to_list(class_widget)

    def add_to_list(self, class_widget: ClassWidget):
        i = 0
        overlapping_widgets: List[ClassWidget] = []

        while i < len(self.widgets) and class_widget.x <= self.widgets[i].x:
            if overlap_along_x_axis(class_widget, self.widgets[i]):
                overlapping_widgets.append(self.widgets[i])
            i += 1

        overlapping_widgets.append(class_widget)
        self.widgets.insert(i, class_widget)
        i += 1

        while i < len(self.widgets) and overlap_along_x_axis(class_widget, self.widgets[i]):
            overlapping_widgets.append(self.widgets[i])
            i += 1

        new_height = int(self.height() / len(overlapping_widgets))
        # sorted_widgets = sorted(overlapping_widgets, key=lambda w: (w.x, w.y))

        for i, widget in enumerate(overlapping_widgets):
            widget.setGeometry(QRect(widget.x, i * new_height, widget.width, new_height))


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
        x_offset = 10
        y_offset = 10

        parent.resize(int(self.width * 1.1), int(self.height * 1.1))

        self.time_widget_height = 30
        self.days_of_week_labels_widget_width = 60
        self.n_days_of_week = n_days_of_week

        self.days_of_weeks_widgets: List[DayOfWeekWidget] = [None for _ in range(n_days_of_week)]

        self.widget = QWidget(parent)
        self.widget.setGeometry(QRect(x_offset, y_offset, self.width + self.days_of_week_labels_widget_width,
                                self.time_widget_height + self.height))

        self.widget_time = QWidget(self.widget)
        self.widget_time.setObjectName(u"widget_time")
        self.widget_time.setGeometry(QRect(self.days_of_week_labels_widget_width, 0,
                                           self.width,
                                           self.time_widget_height))

        self.text_time = QTextEdit(self.widget)
        self.text_time.setObjectName(u"text_time")
        self.text_time.setReadOnly(True)
        self.text_time.setTextInteractionFlags(Qt.NoTextInteraction)
        self.text_time.setGeometry(QRect(self.days_of_week_labels_widget_width,
                                         0, self.width, self.time_widget_height))

        self.text_time.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.text_time.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.main_grid_widget = QWidget(self.widget)
        self.main_grid_widget.setObjectName(u"main_grid_widget")
        self.main_grid_widget.setGeometry(QRect(0,
                                                self.time_widget_height, self.width, self.height))

        self.add_days_of_week_widgets()
        self.add_minutes_labels()

        # self.retranslateUi(parent)
        QMetaObject.connectSlotsByName(parent)

    # 1 through 7
    def add_day_of_week_widget(self, day_of_week: int):
        index_day_of_week = day_of_week - 1
        self.days_of_weeks_widgets[index_day_of_week] = DayOfWeekWidget(get_eng_day_abbr(get_day_from_int(day_of_week)),
                                                                        self.main_grid_widget,
                                                                        self.start_time, 0,
                                                                        index_day_of_week * self.cell_height,
                                                                        self.width, self.cell_height,
                                                                        self.days_of_week_labels_widget_width)

    def add_days_of_week_widgets(self):
        for i in range(1, self.n_days_of_week + 1):
            self.add_day_of_week_widget(i)

    def add_class_widget(self, class_: Group, day_of_week: int):
        if 1 <= day_of_week <= self.n_days_of_week:
            index_day_of_week = day_of_week - 1
            self.days_of_weeks_widgets[index_day_of_week].place_class_widget(class_)

    def add_minutes_labels(self):
        font = QFont()
        font.setFamilies([u"Arial Unicode MS"])
        font.setPointSize(7)
        font.setWordSpacing(30)
        self.text_time.setFont(font)

        time_interval_in_minutes = 30
        # This will always be 2
        rows_of_time_label = 2

        n_intervals = self.n_minutes / time_interval_in_minutes
        n_intervals += int(n_intervals % 2)

        n_labels = int(n_intervals / rows_of_time_label)

        def generate_labels(start_time, n_labels):
            return [(start_time + timedelta(minutes=i * (rows_of_time_label * time_interval_in_minutes))).strftime(TIME_FORMAT)
                    for i in range(n_labels)]

        upper_labels = generate_labels(self.start_time, n_labels + 1)
        lower_labels = generate_labels(datetime.strptime((self.start_time
                                        + timedelta(minutes=time_interval_in_minutes)).strftime(TIME_FORMAT), TIME_FORMAT),
                                       n_labels + int(n_intervals % 2))

        # TODO: change this to labels
        self.text_time.append(" ".join(upper_labels))
        self.text_time.append(" " + " ".join(lower_labels))

    def add_classes(self, classes_: Iterable[Class]):
        for class_ in classes_:
            index_day_of_week = class_.day.value - 1
            if 0 <= index_day_of_week < self.n_days_of_week:
                self.days_of_weeks_widgets[index_day_of_week].place_class_widget(class_)


    # retranslateUi

if __name__ == "__main__":

    app = QApplication()
    window = QMainWindow()
    grid = GridWidget(window, 120, 5, datetime.strptime("7:00", "%H:%M"), datetime.strptime("21:00", "%H:%M"))

    test_classes = [create_class(DayOfWeek.Monday, WeekType.EVERY_WEEK, as_hour("7:30"), as_hour("9:00"), "K01-30a"),
                    create_class(DayOfWeek.Monday, WeekType.EVERY_WEEK, as_hour("8:00"), as_hour("10:00"), "K01-30b"),
                    create_class(DayOfWeek.Monday, WeekType.EVERY_WEEK, as_hour("7:30"), as_hour("10:00"), "K01-30c"),
                    create_class(DayOfWeek.Monday, WeekType.EVERY_WEEK, as_hour("11:15"), as_hour("13:00"), "K01-30d"),
                    create_class(DayOfWeek.Friday, WeekType.EVERY_WEEK, as_hour("11:15"), as_hour("13:00"), "K01-31c"),
                    create_class(DayOfWeek.Friday, WeekType.EVERY_WEEK, as_hour("11:15"), as_hour("13:00"), "K01-31d")]

    grid.add_classes(test_classes)
    window.show()
    app.exec()