from typing import List

from planner.models.groups import Course, Group
from searching import get_best_solutions


def get_dream_timetables(courses: List[Course]) -> List[List[Group]]:
    return get_best_solutions(courses)
