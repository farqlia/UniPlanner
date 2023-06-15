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
from datetime import datetime

DAYS_OF_WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

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
        # day_label.setCursor(QCursor(Qt.ArrowCursor))
        day_label.setGeometry(0, y, label_width, height)
        day_label.setReadOnly(True)
        day_label.setText(day_of_week[:3].capitalize())


    def place_course_widget(self, class_: classes.Class):
        class_widget = QWidget(self)
        rectangle_size = QRect(self._compute_x(class_), self._compute_y(class_),
                                self._compute_width(class_), self._compute_height(class_))
        class_widget.setGeometry(rectangle_size)
        class_description = QTextEdit(class_widget)
        class_description.setGeometry(QRect(0, 0, rectangle_size.width(), rectangle_size.height()))
        class_description.setReadOnly(True)
        # class_description.setCursor(QCursor(Qt.ArrowCursor))
        class_description.setText(class_.class_code)

    def _compute_x(self, class_: classes.Class) -> int:
        return self.label_width + int((class_.start_time - self.time_0).total_seconds() / 60.0)

    # Just for now
    def _compute_y(self, class_: classes.Class) -> int:
        return 0

    def _compute_height(self, class_: classes.Class) -> int:
        return self.height()

    def _compute_width(self, class_: classes.Class) -> int:
        return class_.durance


class Ui_Form(object):
    def setupUi(self, Form, width, height, n_days_of_week):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(926, 656)

        time_widget_height = 30
        days_of_week_labels_widget_width = 60

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 10, width + days_of_week_labels_widget_width, time_widget_height + height))

        self.widget_time = QWidget(self.widget)
        self.widget_time.setObjectName(u"widget_time")
        self.widget_time.setGeometry(QRect(days_of_week_labels_widget_width, 0, width, time_widget_height))

        self.text_time = QTextEdit(self.widget_time)
        self.text_time.setObjectName(u"text_time")
        self.text_time.setReadOnly(True)
        self.text_time.setTextInteractionFlags(Qt.NoTextInteraction)
        self.text_time.setGeometry(QRect(0, 0, width, time_widget_height))

        self.widget_day_of_week_labels = QWidget(self.widget)
        self.widget_day_of_week_labels.setObjectName(u"widget_day_of_week_labels")
        self.widget_day_of_week_labels.setGeometry(QRect(0, time_widget_height, days_of_week_labels_widget_width, height))

        self.main_grid_widget = QWidget(self.widget)
        self.main_grid_widget.setObjectName(u"widget_3")
        self.main_grid_widget.setGeometry(QRect(0, time_widget_height, width, height))

        monday_widget = DayOfWeekWidget('Monday', self.main_grid_widget,
                                       datetime.strptime("7:00", "%H:%M"), 0, 0, width, height // n_days_of_week,
                                        days_of_week_labels_widget_width)
        monday_widget.place_course_widget(classes.Class(1, datetime.strptime("8:00", "%H:%M"), classes.WeekType.EVERY_WEEK,
                                                      classes.Form.LECTURE, 90, "K01-22a", None, None))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))

    # retranslateUi

if __name__ == "__main__":
    app = QApplication()
    window = QMainWindow()
    Ui_Form().setupUi(window, 840, 600, 5)
    window.show()
    app.exec()