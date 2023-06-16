from planner.connection.connection import parse_date_and_place, as_hour
from planner.models.classes import DayOfWeek, WeekType
from datetime import datetime
import pytest


@pytest.mark.parametrize("arg,expected", [
    ("pn/TN+1/2 09:15-11:00, bud. D-1, sala 311c", (DayOfWeek.Monday, WeekType.ODD_WEEK, as_hour("09:15"), as_hour("11:00"), "D-1", "311c")),
    ("pt 13:15-15:00, bud. C-6, sala 128", (DayOfWeek.Friday, WeekType.EVERY_WEEK, as_hour("13:15"), as_hour("15:00"), "C-6", "128")),
    ("śr/TP+1/2 09:15-11:00, bud. D-2, sala 127c", (DayOfWeek.Wednesday, WeekType.EVEN_WEEK, as_hour("9:15"), as_hour("11:00"), "D-2", "127c"))
])
def test_parse_date_and_place(arg, expected):
    parsed_elements = parse_date_and_place(arg)
    assert parsed_elements == expected

