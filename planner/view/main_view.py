# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window_ui_2mCHydd.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from typing import List

from PySide6.QtCore import (QMetaObject, QRect,
                            Qt)
from PySide6.QtGui import (QCursor)
from PySide6.QtWidgets import (QApplication, QCheckBox, QMainWindow, QMenuBar,
                               QPushButton, QStatusBar,
                               QTabWidget, QWidget)

from planner.models.groups import Course, DayOfWeek, WeekType
from planner.utils.datetime_utils import as_hour
from planner.view.grid_widget import GridWidget
from planner.view.select_groups_widget import SelectGroupsWidget
from planner.view.view_utils import create_group


class MainWindow(QMainWindow):

    def __init__(self, width=1500, height=750):
        super(MainWindow, self).__init__()
        self.setTabShape(QTabWidget.Rounded)
        self.setFixedSize(width, height)

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")

        self.tab_widget = QTabWidget(self.centralwidget)
        self.tab_widget.setObjectName(u"tab_widget")
        self.tab_widget.setGeometry(QRect(10, 10, width - 20, height - 20))
        self.tab_widget.setCursor(QCursor(Qt.ArrowCursor))

        self.tab = QWidget()
        self.tab.setObjectName(u"Create plan")

        x_grid_parent_widget, y_grid_parent_widget, w_grid_parent_widget, h_grid_parent_widget = 10, 10, 950, 640
        self.grid_parent_widget = QWidget(self.tab)
        self.grid_parent_widget.setObjectName(u"grid_parent_widget")
        self.grid_parent_widget.setGeometry(QRect(x_grid_parent_widget, y_grid_parent_widget,
                                                  w_grid_parent_widget, h_grid_parent_widget))

        self.grid_widget = GridWidget(self.grid_parent_widget,
                                      120, 5, as_hour("7:00"), as_hour("21:00"))

        self.select_groups_parent_widget = QWidget(self.tab)
        self.select_groups_parent_widget.setObjectName(u"select_groups_parent_widget")
        self.select_groups_parent_widget.setGeometry(QRect(x_grid_parent_widget + w_grid_parent_widget,
                                                           y_grid_parent_widget, 400, 440))

        self.select_groups_widget = SelectGroupsWidget(self.select_groups_parent_widget,
                                                       400)

        self.pushButton = QPushButton(self.tab)
        self.pushButton.setText("Generate plan")
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(width - 150, 590, 111, 41))

        self.pushButton.clicked.connect(self.generate_plan)

        self.exclude_area_check_box = QCheckBox(self.tab)
        self.exclude_area_check_box.setObjectName(u"exclude_area_check_box")
        self.exclude_area_check_box.setText("Exclude area")
        self.exclude_area_check_box.setGeometry(QRect(x_grid_parent_widget + w_grid_parent_widget, 480, 101, 20))
        # Change cursor on user action
        self.exclude_area_check_box.clicked.connect(self.allow_excluding_areas)

        self.remove_area_check_box = QCheckBox(self.tab)
        self.remove_area_check_box.setObjectName(u"remove_area_check_box")
        self.remove_area_check_box.setGeometry(QRect(x_grid_parent_widget + w_grid_parent_widget, 510, 240, 20))
        self.remove_area_check_box.setText("Remove excluded area (Double click)")
        self.remove_area_check_box.clicked.connect(self.allow_removing_excluded_areas)

        # self.exclude_area_check_box.setCursor(QCursor(Qt.CrossCursor))
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

        self.grid_widget.add_listeners(self.select_groups_widget.update_categorized_groups_for_current_course)
        self.select_groups_widget.add_listener_for_group_change(self.grid_widget.update)

    def load_courses(self, courses: List[Course]):
        self.select_groups_widget.load_courses(courses)
        self.grid_widget.add_groups([group for course in courses for group in course.groups])

    def allow_excluding_areas(self):
        if self.exclude_area_check_box.isChecked():
            self.remove_area_check_box.setChecked(False)
            self.grid_widget.change_cursor(QCursor(Qt.CrossCursor))
            self.grid_widget.set_can_exclude_area(True)
        else:
            self.grid_widget.change_cursor(QCursor(Qt.ArrowCursor))
            self.grid_widget.set_can_exclude_area(False)

    def allow_removing_excluded_areas(self):
        if self.remove_area_check_box.isChecked():
            self.exclude_area_check_box.setChecked(False)
            self.grid_widget.change_cursor(QCursor(Qt.OpenHandCursor))
            self.grid_widget.set_can_remove_area(True)
        else:
            self.grid_widget.change_cursor(QCursor(Qt.ArrowCursor))
            self.grid_widget.set_can_remove_area(False)

    # Main functionality !!!
    def generate_plan(self):
        # Get groups categorized by user, for each course
        # self.select_groups_widget.courses
        # Areas excluded by user as rectangles
        # Here will be some additional constraints
        self.pushButton.setCursor(QCursor(Qt.BusyCursor))
        # Algorithm ...

        self.pushButton.setCursor(QCursor(Qt.ArrowCursor))
