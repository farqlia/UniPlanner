from planner.models.classes import Course, Class
from typing import List, Optional


def find_course_by_code(courses: List[Course], course_code: str) -> Optional[Course]:
    for course in courses:
        if course.code == course_code:
            return course
    return None


def find_group_by_code(groups: List[Class], group_code: str) -> Optional[Class]:
    for group in groups:
        if group.code == group_code:
            return group
    return None

