from PySide6.QtWidgets import QMessageBox

from planner.models.groups import Group, GroupCategory, GroupType

POLISH_GROUP_TYPE = {GroupType.LECTURE: 'W',
                     GroupType.LABORATORY: 'L',
                     GroupType.PRACTICALS: 'C',
                     GroupType.SEMINAR: 'S',
                     GroupType.PROJECT: 'P'}


def create_group(day, week_type, start_time, end_time, code):
    return Group(code, None, None, day, week_type, start_time, end_time,
                 None, None, None, GroupCategory.NEUTRAL)


def display_warning_msg(parent, msg="") -> None:
    dlg = QMessageBox(parent)
    dlg.setWindowTitle("Warning")
    dlg.setText(msg)
    dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
    dlg.setIcon(QMessageBox.Icon.Warning)
    dlg.exec()


def display_error_msg(parent, msg="") -> None:
    dlg = QMessageBox(parent)
    dlg.setWindowTitle("Warning")
    dlg.setText(msg)
    dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
    dlg.setIcon(QMessageBox.Icon.Critical)
    dlg.exec()


def display_yes_no_msg(parent, msg="") -> bool:
    dlg = QMessageBox(parent)
    dlg.setWindowTitle("Information")
    dlg.setText(msg)
    dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    dlg.setIcon(QMessageBox.Icon.Question)
    return dlg.exec() == QMessageBox.StandardButton.Yes
