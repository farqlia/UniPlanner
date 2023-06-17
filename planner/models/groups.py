from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Any


class GroupCategory(Enum):
    PREFERRED = 1
    NEUTRAL = 2
    EXCLUDED = 3


class WeekType(Enum):
    EVERY_WEEK = 1
    EVEN_WEEK = 2
    ODD_WEEK = 3

    def __str__(self):
        return f'{self.name}'


class GroupType(Enum):
    LECTURE = 1
    PRACTICALS = 2
    LABORATORY = 3
    PRACTICE = 4
    SEMINAR = 5

    def __str__(self):
        return f'{self.name}'


class DayOfWeek(Enum):
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7

    def __str__(self):
        return f'{self.name}'


@dataclass
class Teacher:
    name: str
    title: str

    def __str__(self):
        return f"{self.title} {self.name}"

    def __repr__(self):
        return f"{self.title} {self.name}"


# Like "Administracja Systemami" nie wiem skąd to wziąć,
# chyba trzeba wprowadzić mechanizm ręcznego odrzucania kursów
class CourseGroup:
    pass


# Classes belong to courses
@dataclass
class Course:
    """Class for the course student may complete"""
    name: str
    code: str
    groups: list
    link: str = ''

@dataclass
class Group:
    """Class for classes the student may enrol on"""
    code: str
    course: Course
    lecturer: Teacher
    day: DayOfWeek
    week_type: WeekType
    start_time: datetime
    end_time: datetime
    building: str
    hall: str
    type: GroupType
    category: GroupCategory = GroupCategory.NEUTRAL

    def __repr__(self):
        return f'{self.code} on {self.day.name} in {self.week_type.name} from ' \
               f'{self.start_time.strftime("%H:%M")} to {self.end_time.strftime("%H:%M")}'

    @property
    def durance(self):
        return int((self.end_time - self.start_time).total_seconds() / 60.0)

    def __lt__(self, other):
        return self.start_time < other.start_time if self.day == other.day else self.day.value < other.day.value

    def __gt__(self, other):
        return self.start_time > other.start_time if self.day == other.day else self.day.value > other.day.value

    def occurs_even(self):
        return self.week_type == WeekType.EVEN_WEEK or self.week_type == WeekType.EVERY_WEEK

    def occurs_odd(self):
        return self.week_type == WeekType.ODD_WEEK or self.week_type == WeekType.EVERY_WEEK

    def is_excluded(self):
        return self.category == GroupCategory.EXCLUDED

    def is_preferred(self):
        return self.category == GroupCategory.PREFERRED



