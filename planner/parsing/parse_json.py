import json

from planner.models.groups import Teacher, Group, Course
from planner.utils.datetime_utils import TIME_FORMAT
from planner.parsing.parse_elements import group_factory


def load_from_file(file: str):
    with open(file, encoding='utf-8') as f:
        return json.load(f)


def load_from_json(file: str):
    return [Course(groups=[group_factory(**group) for group in loaded_course['groups']],
                   **{attr: loaded_course[attr] for attr in loaded_course if attr != 'groups'})
            for loaded_course in load_from_file(file)['courses']]


def obj_to_dict(obj):
    if isinstance(obj, list):
        return {
            "course": [obj_to_dict(c) for c in obj]
        }
    elif isinstance(obj, Teacher):
        return {
            "title": obj.title,
            "name": obj.name
        }
    elif isinstance(obj, Group):
        return {
            "code": obj.code,
            "course": obj.course,
            "lecturer": obj_to_dict(obj.lecturer),
            "day": obj.day.value,
            "week_type": obj.week_type.value,
            "start_time": obj.start_time.strftime(TIME_FORMAT),
            "end_time": obj.end_time.strftime(TIME_FORMAT),
            "building": obj.building,
            "hall": obj.hall,
            "type": obj.type.value
        }
    elif isinstance(obj, Course):
        return {
            "name": obj.name,
            "code": obj.code,
            "groups": [obj_to_dict(c) for c in obj.groups]
        }
