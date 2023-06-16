from planner.models.groups import Course, Group
from typing import List, Optional


def find_course_by_code(courses: List[Course], course_code: str) -> Optional[Course]:
    for course in courses:
        if course.code == course_code:
            return course
    return None


def find_group_by_code(groups: List[Group], group_code: str) -> Optional[Group]:
    for group in groups:
        if group.code == group_code:
            return group
    return None

