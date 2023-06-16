from planner.parsing.parse_elements import parse_date_and_place, parse_teacher
from planner.utils.datetime_utils import as_hour
from planner.models.groups import DayOfWeek, WeekType, Teacher
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


@pytest.mark.parametrize("arg,expected", [
    ("Dr Zbigniew Pliszka", Teacher("Zbigniew Pliszka", "Dr")),
    ("Mgr Hanna Mazur", Teacher("Hanna Mazur", "Mgr")),
    ("Dr hab. Zygmunt Mazur", Teacher("Zygmunt Mazur", "Dr hab.")),
    ("Mgr inż. Konrad Wojtasik", Teacher("Konrad Wojtasik", "Mgr inż.")),
    ("Dr hab. inż. Janusz Jacak", Teacher("Janusz Jacak", "Dr hab. inż.")),
    ("Dr inż. Krzysztof Billewicz", Teacher("Krzysztof Billewicz", "Dr inż.")),
    ("Prof. dr hab. inż. Jerzy Świątek", Teacher("Jerzy Świątek", "Prof. dr hab. inż."))
])


def test_teacher(arg, expected):
    parsed_teacher = parse_teacher(arg)
    assert parsed_teacher.name == expected.name
    assert parsed_teacher.title == expected.title