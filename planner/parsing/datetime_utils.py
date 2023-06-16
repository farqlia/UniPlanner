from typing import Tuple
from datetime import datetime
import re
from planner.models.classes import DayOfWeek, WeekType


POLISH_ABBR_DAY_OF_WEEK = {'pn': DayOfWeek.Monday, 'wt': DayOfWeek.Tuesday,
                           'śr': DayOfWeek.Wednesday, 'cz': DayOfWeek.Thursday,
                           'pt': DayOfWeek.Friday}

DAYS_OF_WEEK_ABBR = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']


def get_eng_abbr(day_of_week: DayOfWeek) -> str:
    return DAYS_OF_WEEK_ABBR[day_of_week.value - 1]


def from_polish_abbr(abbr: str) -> DayOfWeek:
    return POLISH_ABBR_DAY_OF_WEEK[abbr]


def as_hour(hour: str) -> datetime:
    return datetime.strptime(hour, "%H:%M")


def week_type(week_match: str) -> WeekType:
    pass
