# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'grid_widgetoXfMlN.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QSizePolicy, QTextEdit, QWidget, QMainWindow)
import planner.models.classes as classes
from datetime import datetime, timedelta
from typing import Iterable

DAYS_OF_WEEK = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

class ClassWidget(QWidget):

    def __init__(self, parent: QObject, class_: classes.Class, x, y, width, height):
        super(ClassWidget, self).__init__(parent)

        self.class_ = class_

        self.setGeometry(QRect(x, y, width, height))
        class_description = QTextEdit(self)
        class_description.setGeometry(QRect(0, 0, width, height))
        class_description.setReadOnly(True)
        # class_description.setCursor(QCursor(Qt.ArrowCursor))
        class_description.append(class_.class_code)
        class_description.append(class_.form.name)
        class_description.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        class_description.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)


# A panel to place courses for a given day of week
# We assume that 1 minute = 1 unit of width
# The total width should be computed based on all possible classes
# (usually it is 7-21, but could be 7-22/7-23)
# Height depends on whether we include Saturday & Sunday
class DayOfWeekWidget(QWidget):

    # x, y are positions regarding the 'widget_classes' widget
    def __init__(self, day_of_week: str, parent: QObject, time_0: datetime, x, y, width, height, label_width) -> None:
        super().__init__(parent)
        self.setGeometry(QRect(x, y, width + label_width, height))
        self.time_0 = time_0
        self.widgets = []      # all classes currently placed

        self.label_width = label_width

        day_label = QTextEdit(self)
        day_label.setTextInteractionFlags(Qt.NoTextInteraction)
        day_label.setGeometry(0, 0, label_width, height)
        day_label.setReadOnly(True)
        day_label.setText(day_of_week)

    def place_class_widget(self, class_: classes.Class):
        class_widget = ClassWidget(self, class_, self._compute_x(class_), self._compute_y(class_),
                                self._compute_width(class_), self._compute_height(class_))
        self.widgets.append(class_widget)

    def _compute_x(self, class_: classes.Class) -> int:
        return self.label_width + int((class_.start_time - self.time_0).total_seconds() / 60.0)

    # Just for now
    def _compute_y(self, class_: classes.Class) -> int:
        return 0

    def _compute_height(self, class_: classes.Class) -> int:
        return self.height()

    def _compute_width(self, class_: classes.Class) -> int:
        return class_.durance


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

        self.days_of_weeks_widgets = [None for _ in range(n_days_of_week)]

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
        self.days_of_weeks_widgets[index_day_of_week] = DayOfWeekWidget(DAYS_OF_WEEK[index_day_of_week],
                                                                        self.main_grid_widget,
                                                                        self.start_time, 0,
                                                                        index_day_of_week * self.cell_height,
                                                                        self.width, self.cell_height,
                                                                        self.days_of_week_labels_widget_width)

    def add_days_of_week_widgets(self):
        for i in range(1, self.n_days_of_week + 1):
            self.add_day_of_week_widget(i)

    def add_class_widget(self, class_: classes.Class, day_of_week: int):
        if 1 <= day_of_week <= self.n_days_of_week:
            index_day_of_week = day_of_week - 1
            self.days_of_weeks_widgets[index_day_of_week].place_course_widget(class_)

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
            return [(start_time + timedelta(minutes=i * (rows_of_time_label * time_interval_in_minutes))).strftime("%H:%M")
                    for i in range(n_labels)]

        upper_labels = generate_labels(self.start_time, n_labels + 1)
        lower_labels = generate_labels(datetime.strptime((self.start_time
                                        + timedelta(minutes=time_interval_in_minutes)).strftime("%H:%M"), "%H:%M"),
                                       n_labels + int(n_intervals % 2))

        # self.text_time.
        self.text_time.append(" ".join(upper_labels))
        self.text_time.append(" " + " ".join(lower_labels))

    def add_classes(self, classes_ : Iterable[classes.Class]):
        for class_ in classes_:
            index_day_of_week = class_.day_of_week - 1
            if 0 <= index_day_of_week < self.n_days_of_week:
                self.days_of_weeks_widgets[index_day_of_week].place_class_widget(class_)


    # retranslateUi

if __name__ == "__main__":

    app = QApplication()
    window = QMainWindow()
    GridWidget(window, 120, 5, datetime.strptime("7:00", "%H:%M"), datetime.strptime("21:00", "%H:%M"))
    window.show()
    app.exec()