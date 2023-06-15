import typing
from datetime import datetime
from enum import Enum


class Teacher:

    def __init__(self, firstname: str, surname: str):
        self.firstname = firstname
        self.surname = surname

    def __str__(self):
        return f"{self.firstname} {self.surname}"


# Like "Administracja Systemami"
class CourseGroup:

    def __init__(self, name: str):
        self.name = name


# Classes belong to courses
class Course:

    def __init__(self, name: str, course_group: CourseGroup):
        self.name = name
        self.course_group = course_group


class WeekType(Enum):
    EVERY_WEEK = 1
    EVEN_WEEK = 2
    ODD_WEEK = 3


class Form(Enum):
    LECTURE = 1
    PRACTICALS = 2
    LABORATORY = 3
    PRACTICE = 4
    SEMINAR = 5


class Class:

    # Day of week: 1 - 7
    # week_type
    def __init__(self, day_of_week: int, start_time: datetime,
                 week_type: WeekType, form: Form,
                 durance: int, class_code: str, teacher: Teacher,
                 course: Course):
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.week_type = week_type
        self.form = form
        self.durance = durance
        self.class_code = class_code
        self.teacher = teacher
        self.course = course
