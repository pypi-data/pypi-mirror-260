from datetime import datetime, timedelta
from enum import Enum
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Font:
    def __init__(
        self,
        color: str = "",
        font_size: int = 0,
        font_weight: str = "",
        family: str = "",
    ):
        self.family = family
        self.color = color
        self.font_size = font_size
        self.font_weight = font_weight

    def __str__(self):
        family = f"family: {self.family};" if self.family else ""
        color = f"color: {self.color};" if self.color else ""
        font_size = f"font-size: {self.font_size}px;" if self.font_size else ""
        font_weight = f"font-weight: {self.font_weight};" if self.font_weight else ""

        return f"""
            {family}
            {color}
            {font_size}
            {font_weight}
        """


class DayLetter(QLabel):
    def __init__(self, text: str):
        super().__init__(text)

        s = 40
        self.setFixedSize(s, s)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)


DAYS_LETTERS = ["S", "M", "T", "W", "TH", "F", "S"]


class ButtonType(Enum):
    no_day = "no_day"
    day_number = "day_number"
    day_number_event = "day_number_event"


class DayButton(QPushButton):
    def __init__(
        self,
        row: int,
        col: int,
        type: ButtonType = ButtonType.day_number,
    ):
        super().__init__()

        s = 40
        self.setFixedSize(s, s)
        self.update_type(type)

        self.row = row
        self.col = col
        self.day: datetime = None
        self.event_: str = ""

        self.datetime: datetime = None

        t = row * 7 + col + 1
        self.setText(str(t))

    def update_type(self, type: ButtonType):
        self.setObjectName(type.value)
        self.update()

    def set_day(self, day: datetime, event: str = ""):
        self.day = day
        self.setText(str(day.day))
        self.set_event(event)

    def set_event(self, event: str):
        self.event_ = event
        self.update_type(
            ButtonType.day_number_event if event else ButtonType.day_number
        )
        self.setToolTip(event)

    def set_empty(self):
        self.day = None
        self.setText("")
        self.setToolTip("")
        self.update_type(ButtonType.no_day)
