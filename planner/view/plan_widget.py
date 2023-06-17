from planner.view.grid_widget import BasicGridWidget, BasicDayOfWeekWidget, GroupWidget
from PySide6.QtWidgets import QWidget


class PlanWidget(QWidget):

    def __init__(self, parent, groups):
        super(PlanWidget, self).__init__(parent)
        w_grid_widget, h_grid_widget = 950, 640
        self.setFixedWidth(w_grid_widget)
        self.setFixedHeight(h_grid_widget)

        self.grid_widget = BasicGridWidget(self)
        self.grid_widget.load_groups(groups)
        self.update()



