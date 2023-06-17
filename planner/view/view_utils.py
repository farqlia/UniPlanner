from planner.models.groups import Group, GroupCategory, GroupType

POLISH_GROUP_TYPE = {GroupType.LECTURE: 'W',
                     GroupType.LABORATORY: 'L',
                     GroupType.PRACTICALS: 'C',
                     GroupType.SEMINAR: 'S',
                     GroupType.PRACTICE: 'P'}

def create_group(day, week_type, start_time, end_time, code):
    return Group(code, None, None, day, week_type, start_time, end_time,
                 None, None, None, GroupCategory.NEUTRAL)


