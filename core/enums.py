from enum import Enum


class CalendarType(str, Enum):
    SOLAR = "solar"
    LUNAR = "lunar"


class EventType(str, Enum):
    ANNIVERSARY = "anniversary"
    BIRTHDAY = "birthday"
    COUNTUP = "countup"
    COUNTDOWN = "countdown"


class RepeatType(str, Enum):
    NONE = "none"
    YEARLY = "yearly"
