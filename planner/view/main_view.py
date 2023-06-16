# -*- coding: utf-8 -*-
import time

################################################################################
## Form generated from reading UI file 'main_window_ui_2mCHydd.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QMainWindow, QMenuBar,
    QPushButton, QScrollArea, QSizePolicy, QStatusBar,
    QTabWidget, QWidget)

from planner.models.groups import Course, DayOfWeek, WeekType
from planner.utils.datetime_utils import as_hour
from planner.view.view_utils import create_group
from typing import List
from planner.view.select_groups_widget import SelectGroupsWidget
from planner.view.grid_widget import GridWidget


class MainWindow(QMainWindow):

    def __init__(self, width=1300, height=730):
        super(MainWindow, self).__init__()
        self.resize(width, height)
        self.setTabShape(QTabWidget.Rounded)

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")

        self.tab_widget = QTabWidget(self.centralwidget)
        self.tab_widget.setObjectName(u"tab_widget")
        self.tab_widget.setGeometry(QRect(10, 10, 1280, 680))
        self.tab_widget.setCursor(QCursor(Qt.ArrowCursor))

        self.tab = QWidget()
        self.tab.setObjectName(u"Create plan")

        self.grid_parent_widget = QWidget(self.tab)
        self.grid_parent_widget.setObjectName(u"grid_parent_widget")
        self.grid_parent_widget.setGeometry(QRect(10, 10, 930, 640))

        self.grid_widget = GridWidget(self.grid_parent_widget,
                                      120, 5, as_hour("7:00"), as_hour("21:00"))

        self.select_groups_parent_widget = QWidget(self.tab)
        self.select_groups_parent_widget.setObjectName(u"select_groups_parent_widget")
        self.select_groups_parent_widget.setGeometry(QRect(930, 10, 340, 440))

        self.select_groups_widget = SelectGroupsWidget(self.select_groups_parent_widget)

        self.pushButton = QPushButton(self.tab)
        self.pushButton.setText("Generate plan")
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(1150, 590, 111, 41))

        self.pushButton.clicked.connect(self.generate_plan)

        self.checkBox = QCheckBox(self.tab)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setText("Exclude area")
        self.checkBox.setGeometry(QRect(930, 480, 101, 20))
        # Change cursor on user action
        self.checkBox.clicked.connect(self.change_grid_cursor)
        # self.checkBox.setCursor(QCursor(Qt.CrossCursor))
        self.tab_widget.addTab(self.tab, "")

        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tab_widget.addTab(self.tab_2, "")

        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1300, 22))

        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)

        self.tab_widget.setCurrentIndex(0)
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab),
                                   "Create plan")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_2), "Tab2")

        QMetaObject.connectSlotsByName(self)

    def load_courses(self, courses: List[Course]):
        self.select_groups_widget.load_courses(courses)
        self.grid_widget.add_groups([group for course in courses for group in course.groups])

    def change_grid_cursor(self):
        if self.checkBox.isChecked():
            self.grid_widget.change_cursor(QCursor(Qt.CrossCursor))
            self.grid_widget.set_can_exclude_area(True)
        else:
            self.grid_widget.change_cursor(QCursor(Qt.ArrowCursor))
            self.grid_widget.set_can_exclude_area(False)

    # Main functionality !!!
    def generate_plan(self):
        # Get groups categorized by user, for each course
        self.select_groups_widget.get_categorized_courses()
        # Here will be some additional constraints
        self.pushButton.setCursor(QCursor(Qt.BusyCursor))
        # Algorithm ...

        self.pushButton.setCursor(QCursor(Qt.ArrowCursor))


if __name__ == "__main__":

    app = QApplication()
    window = MainWindow()

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
    window.load_courses(test_courses)
    window.show()
    app.exec()
