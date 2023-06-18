from typing import Tuple
from datetime import datetime
import re
from planner.models.groups import DayOfWeek, WeekType


POLISH_ABBR_DAY_OF_WEEK = {'pn': DayOfWeek.Monday, 'wt': DayOfWeek.Tuesday,
                           'śr': DayOfWeek.Wednesday, 'cz': DayOfWeek.Thursday,
                           'pt': DayOfWeek.Friday}

DAYS_OF_WEEK_ENG_ABBR = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
DAYS_OF_WEEK_POL_ABBR = ['pn', 'wt', 'śr', 'cz', 'pt']

TIME_FORMAT = "%H:%M"

WEEK_TYPE_POLISH_FORM = {WeekType.EVERY_WEEK: "", WeekType.ODD_WEEK: "TN",
                         WeekType.EVEN_WEEK: "TP"}


def get_pol_day_abbr(day_of_week: DayOfWeek) -> str:
    return DAYS_OF_WEEK_POL_ABBR[day_of_week.value - 1]


def get_eng_day_abbr(day_of_week: DayOfWeek) -> str:
    return DAYS_OF_WEEK_ENG_ABBR[day_of_week.value - 1]


def format_week_type(week_type: WeekType) -> str:
    return "/" + WEEK_TYPE_POLISH_FORM[week_type] if len(
        WEEK_TYPE_POLISH_FORM[week_type]) > 0 else ""


def day_from_polish_abbr(abbr: str) -> DayOfWeek:
    return POLISH_ABBR_DAY_OF_WEEK[abbr]


# Days are 1 - 7
def get_day_from_int(day: int) -> DayOfWeek:
    return list(DayOfWeek)[day - 1]


def as_hour(hour: str) -> datetime:
    return datetime.strptime(hour, "%H:%M")


def week_type(week_match: str) -> WeekType:
    pass
