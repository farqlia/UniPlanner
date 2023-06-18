# -*- coding: utf-8 -*-
import sys
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
from PySide6.QtGui import (QCursor, QCloseEvent, QHideEvent)
from PySide6.QtWidgets import (QCheckBox, QMainWindow, QMenuBar,
                               QPushButton, QStatusBar,
                               QTabWidget, QWidget, QMessageBox, QGridLayout)

from planner.controller.controller import get_dream_timetables
from planner.models.groups import Course
from planner.utils.datetime_utils import as_hour
from planner.view.grid_widget import GridWidget
from planner.view.plan_widget import PlanTabWidget
from planner.view.select_groups_widget import SelectGroupsWidget


class MainWindow(QMainWindow):

    def __init__(self, parent, width=1500, height=750):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('UniPlanner')
        self.setTabShape(QTabWidget.Rounded)
        self.setFixedSize(width, height)

        self.buttons_width = 110
        self.buttons_height = 40

        self.courses = None

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
        self.grid_parent_widget.setFixedWidth(w_grid_parent_widget)
        self.grid_parent_widget.setFixedHeight(h_grid_parent_widget)

        self.grid_widget = GridWidget(self.grid_parent_widget,
                                      120, 5, as_hour("7:00"), as_hour("21:00"))

        self.select_groups_parent_widget = QWidget(self.tab)
        self.select_groups_parent_widget.setObjectName(u"select_groups_parent_widget")
        self.select_groups_parent_widget.setFixedWidth(400)
        self.select_groups_parent_widget.setFixedHeight(440)

        self.select_groups_widget = SelectGroupsWidget(self.select_groups_parent_widget, self.grid_widget,
                                                       400)

        self.generate_plan_button = QPushButton(self.tab)
        self.generate_plan_button.setText("Generate plan")
        self.generate_plan_button.setObjectName(u"generate_plan_button")
        self.generate_plan_button.setFixedWidth(110)
        self.generate_plan_button.setFixedHeight(40)

        self.generate_plan_button.clicked.connect(self.generate_plan_action)

        self.exclude_area_check_box = QCheckBox(self.tab)
        self.exclude_area_check_box.setObjectName(u"exclude_area_check_box")
        self.exclude_area_check_box.setText("Exclude area")
        # self.exclude_area_check_box.setGeometry(QRect(x_grid_parent_widget + w_grid_parent_widget, 480, 101, 20))
        # Change cursor on user action
        self.exclude_area_check_box.clicked.connect(self.allow_excluding_areas)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1300, 22))

        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)

        self.tab_widget.addTab(self.tab, "Create plan")
        self.tab_widget.setCurrentIndex(0)
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab),
                                   "Create plan")

        QMetaObject.connectSlotsByName(self)

        self.grid_widget.add_listener_on_excluding_areas(
            self.select_groups_widget.display_groups_of_course)
        self.select_groups_widget.add_listener_for_group_change(self.grid_widget.update)

        grid_layout = QGridLayout(self.centralwidget)
        grid_layout.addWidget(self.grid_parent_widget, 0, 0, 20, 1)
        grid_layout.addWidget(self.select_groups_parent_widget, 1, 14, 6, 6)
        grid_layout.addWidget(self.generate_plan_button, 18, 18, 2, 2)
        grid_layout.addWidget(self.exclude_area_check_box, 14, 14, 2, 2)

        self.tab.setLayout(grid_layout)

    def load_courses(self, courses: List[Course]):
        self.courses = courses
        self.select_groups_widget.load_courses(courses)
        self.grid_widget.load_courses(courses)

    def allow_excluding_areas(self):
        if self.exclude_area_check_box.isChecked():
            self.grid_widget.change_cursor(QCursor(Qt.CrossCursor))
            self.grid_widget.set_can_exclude_area(True)
        else:
            self.grid_widget.change_cursor(QCursor(Qt.ArrowCursor))
            self.grid_widget.set_can_exclude_area(False)

    def generate_plan_action(self):
        if self.display_yes_no_msg("It will remove all the plans you've already generated. "
                                   "Are you sure you want to do this?"):
            # Cursor is not working now
            self.generate_plan_button.setCursor(QCursor(Qt.BusyCursor))
            self.generate_plan()
            self.generate_plan_button.setCursor(QCursor(Qt.ArrowCursor))

    def generate_plan(self):
        timetables = get_dream_timetables(self.courses)
        self.remove_plan_tabs()

        if len(timetables) > 0:
            for i, timetable in enumerate(timetables, start=1):
                self.display_plan(timetable, f"Plan {i}")
            self.tab_widget.setCurrentIndex(1)

        else:
            self.display_warning_msg("No plans were generated")

    def display_plan(self, timetable, name):
        PlanTabWidget(self.tab_widget, timetable, name)

    def remove_plan_tabs(self):
        while self.tab_widget.count() > 1:
            self.tab_widget.removeTab(1)

    def display_warning_msg(self, msg=""):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Error")
        dlg.setText(msg)
        dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
        dlg.setIcon(QMessageBox.Icon.Warning)
        dlg.exec()

    def display_yes_no_msg(self, msg=""):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Information")
        dlg.setText(msg)
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setIcon(QMessageBox.Icon.Question)
        return dlg.exec() == QMessageBox.StandardButton.Yes

    def closeEvent(self, event: QCloseEvent) -> None:
        super(MainWindow, self).closeEvent(event)
        sys.exit()


