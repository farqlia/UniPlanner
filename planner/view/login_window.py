# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_windowGNOIOv.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QRect)
from PySide6.QtWidgets import (QLabel, QLineEdit, QMainWindow,
                               QPushButton, QWidget)

from planner.connection.connection import LoginException
from planner.controller.controller import get_courses, download_to_file
from planner.view.main_window import MainWindow
from planner.view.view_utils import display_error_msg


class LoginWindow(QMainWindow):

    def __init__(self):
        super(LoginWindow, self).__init__()
        self.resize(462, 308)

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setText("Login")
        self.label.setGeometry(QRect(30, 70, 71, 31))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 130, 71, 31))
        self.label_2.setText("Password")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setText("Log in")
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(310, 200, 81, 31))

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(130, 70, 250, 25))
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(130, 130, 250, 25))
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.setCentralWidget(self.centralwidget)

        self.pushButton.clicked.connect(self.login_event)

    def login_event(self):
        if self.is_login_successful():
            main_window = MainWindow(self)
            main_window.load_courses(get_courses())
            main_window.show()
            self.hide()

    def is_login_successful(self):
        try:
            ## download_to_file(self.lineEdit.text(), self.lineEdit_2.text())
            return True
        except LoginException:
            display_error_msg(self, "Login credentials are invalid")
        except:
            display_error_msg(self, "Unknown error occurred")

