from planner.models.groups import Group, GroupCategory


def create_group(day, week_type, start_time, end_time, code):
    return Group(code, None, None, day, week_type, start_time, end_time,
                 None, None, None, GroupCategory.NEUTRAL)

