from datetime import datetime

from PySide6.QtGui import QFont, QFontInfo, QFontMetrics


def test_how_time_subtracts():

    t1 = datetime.strptime("7:30", "%H:%M")
    t2 = datetime.strptime("7:00", "%H:%M")

    print((t1 - t2).total_seconds() / 60.0)


def test_font():
    font = QFont()
    font.setFamilies([u"Arial Unicode MS"])
    font.setPointSize(7)
    font.setPixelSize(2)
    print(font.pixelSize())