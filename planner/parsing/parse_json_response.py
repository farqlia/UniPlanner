from typing import Tuple
from datetime import datetime
import re
from planner.models.classes import Class, Course, DayOfWeek, WeekType
from planner.parsing.datetime_utils import from_polish_abbr, as_hour

# W tym module moze bedziemy dawac jakies funkcje do parsowania

PLACE_AND_DATE_REGEX = re.compile("(?P<day_of_week>\w{2})(?P<type_of_week>[TPN+12/]*) "
                                "(?P<hour_start>\d{2}:\d{2})-(?P<hour_end>\d{2}:\d{2}), "
                                  "bud. (?P<building>[-\w]+), sala (?P<hall>\w+)")


def parse_date_and_place(date_and_place: str) -> Tuple[DayOfWeek, WeekType, datetime, datetime, str, str]:
    match = PLACE_AND_DATE_REGEX.match(date_and_place)
    day_of_week = from_polish_abbr(match.group("day_of_week"))
    type_of_week = WeekType.EVERY_WEEK if len(match.group("type_of_week")) == 0 \
        else WeekType.EVEN_WEEK if match.group("type_of_week").startswith("/TP") else WeekType.ODD_WEEK
    start_time = as_hour(match.group("hour_start"))
    end_time = as_hour(match.group("hour_end"))
    return day_of_week, type_of_week, start_time, end_time, match.group("building"), match.group("hall")