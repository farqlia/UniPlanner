from planner.models.classes import Class


def create_class(day, week_type, start_time, end_time, code):
    return Class(code, None, None, day, week_type, start_time, end_time, None, None, None)

