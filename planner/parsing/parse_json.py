import json

from planner.models.groups import Teacher, Group, Course
from planner.utils.datetime_utils import TIME_FORMAT


def load_from_file(file: str):
    with open(file, encoding='utf-8') as f:
        return json.load(f)

"""
"course": [
    {
      "name": "Bazy danych",
      "code": "INZ002007C",
      "groups": [
        {
          "code": "K01-17a",
          "course": "INZ002007C",
          "lecturer": {
            "title": "Dr hab.",
            "name": "Zygmunt Mazur"
          },
          "day": "Monday",
          "week_type": "ODD_WEEK",
          "start_time": "09:15",
          "end_time": "11:00",
          "building": "D-1",
          "hall": "311c",
          "type": "PRACTICALS"
        },
        {
          "code": "K01-17b",
          "course": "INZ002007C",
          "lecturer": {
            "title": "Dr hab.",
            "name": "Zygmunt Mazur"
          },
          "day": "Monday",
          "week_type": "EVEN_WEEK",
          "start_time": "09:15",
          "end_time": "11:00",
          "building": "D-1",
          "hall": "311c",
          "type": "PRACTICALS"
        },
        """


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
