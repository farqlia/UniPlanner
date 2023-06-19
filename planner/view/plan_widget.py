from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QPushButton, QTextEdit, QGridLayout, QLabel

from planner.view.grid_widget import BasicGridWidget, detailed_description


class PlanWidget(QWidget):

    def __init__(self, parent, groups):
        super(PlanWidget, self).__init__(parent)
        w_grid_widget, h_grid_widget = 950, 640

        self.setFixedWidth(w_grid_widget)
        self.setFixedHeight(h_grid_widget)

        self.grid_widget = BasicGridWidget(self,
                                           description=detailed_description,
                                           set_color=False)
        self.grid_widget.load_groups(groups)
        self.update()


class PlanTabWidget(QWidget):

    def __init__(self, parent, timetable, name):
        super(PlanTabWidget, self).__init__(parent)

        self.timetable = timetable
        self.plan_widget = PlanWidget(self, timetable)

        self.generate_codes_button = QPushButton()

        self.codes_text_label = QLabel(self)
        self.codes_text_label.setText("Group codes")

        self.codes_text_widget = QTextEdit(self)
        self.codes_text_widget.setFixedHeight(440)
        self.codes_text_widget.setFixedWidth(400)
        self.codes_text_widget.setReadOnly(True)
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.plan_widget, 0, 0, 20, 1)
        grid_layout.addWidget(self.codes_text_label, 2, 1, 1, 1, Qt.AlignmentFlag.AlignTop)
        grid_layout.addWidget(self.codes_text_widget, 3, 1, 1, 1, Qt.AlignmentFlag.AlignTop)

        # self.generate_codes_button.clicked.connect(self.generate_codes)

        self.setLayout(grid_layout)

        for group in self.timetable:
            self.codes_text_widget.append(f"{group.course.name} ({group.course.code}) - {group.code}")

        parent.addTab(self, name)

