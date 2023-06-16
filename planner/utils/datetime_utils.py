from typing import Tuple
from datetime import datetime
import re
from planner.models.groups import DayOfWeek, WeekType


POLISH_ABBR_DAY_OF_WEEK = {'pn': DayOfWeek.Monday, 'wt': DayOfWeek.Tuesday,
                           'śr': DayOfWeek.Wednesday, 'cz': DayOfWeek.Thursday,
                           'pt': DayOfWeek.Friday}

DAYS_OF_WEEK_ABBR = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

TIME_FORMAT = "%H:%M"

WEEK_TYPE_POLISH_FORM = {WeekType.EVERY_WEEK: "", WeekType.ODD_WEEK: "TN",
                         WeekType.EVEN_WEEK: "TP"}


def get_eng_day_abbr(day_of_week: DayOfWeek) -> str:
    return DAYS_OF_WEEK_ABBR[day_of_week.value - 1]


def day_from_polish_abbr(abbr: str) -> DayOfWeek:
    return POLISH_ABBR_DAY_OF_WEEK[abbr]


# Days are 1 - 7
def get_day_from_int(day: int) -> DayOfWeek:
    return list(DayOfWeek)[day - 1]


def as_hour(hour: str) -> datetime:
    return datetime.strptime(hour, "%H:%M")


def week_type(week_match: str) -> WeekType:
    pass
