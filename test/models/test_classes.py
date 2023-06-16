from datetime import datetime
from planner.models.classes import DayOfWeek


def test_enum_values():
    print(list(DayOfWeek))
    print(list(DayOfWeek)[0])