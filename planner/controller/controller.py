from typing import List

from planner.models.groups import Course, Group
from planner.parsing.parse_json import load_from_json
from planner.algorithms.searching import get_best_solutions


def get_dream_timetables(courses: List[Course]) -> List[List[Group]]:
    return get_best_solutions(courses)


def get_courses(filename: str = '../../data/courses.json') -> List[Course]:
    return load_from_json(filename)
