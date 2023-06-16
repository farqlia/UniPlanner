from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List


class GroupCategory(Enum):
    PREFERABLE = 1
    NEUTRAL = 2
    EXCLUDED = 3


class WeekType(Enum):
    EVERY_WEEK = 1
    EVEN_WEEK = 2
    ODD_WEEK = 3


class ClassesType(Enum):
    LECTURE = 1
    PRACTICALS = 2
    LABORATORY = 3
    PRACTICE = 4
    SEMINAR = 5


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


class Teacher:
    # TODO: JAK ROZDZIELAĆ IMIĘ OD NAZWISKA? (i stopnia naukowego)
    def __init__(self, name: str, title: str):
        self.name = name
        self.title = title

    def __str__(self):
        return f"{self.title} {self.name}"


# Like "Administracja Systemami" nie wiem skąd to wziąć,
# chyba trzeba wprowadzić mechanizm ręcznego odrzucania kursów
class CourseGroup:
    pass


@dataclass
class Class: #może classes zamiast class? MOŻE GROUP? (GRUPA ZAJĘCIOWA)
    """Class for classes the student may enrol on"""
    code: str
    course: str # code
    #course: Course -< for key in database
    # lecturer: Teacher  # TODO: in future implementation it should be connected with 'Teacher class'
    date_and_place: str
    day: DayOfWeek
    week_type: WeekType
    start_time: datetime
    end_time: datetime
    building: str
    hall: str
    #place: str
    type: str # TODO: mapping to classes_type

    @property
    def durance(self):
        return int((self.end_time - self.start_time).total_seconds() / 60.0)


# Classes belong to courses
@dataclass
class Course:
    """Class for the course student may complete"""
    name: str
    code: str
    link: str  # What is it for
    classes: List[Class] # dupa
    # type: ClassesType
