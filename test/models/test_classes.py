from datetime import datetime


def test_how_time_subtracts():

    t1 = datetime.strptime("7:30", "%H:%M")
    t2 = datetime.strptime("7:00", "%H:%M")

    print((t1 - t2).total_seconds() / 60.0)