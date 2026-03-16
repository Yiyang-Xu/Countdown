from dataclasses import dataclass, asdict
from typing import Optional

from config.settings import DEFAULT_TIMEZONE
from core.enums import CalendarType, EventType, RepeatType


@dataclass
class Event:
    id: str
    title: str
    date: str
    event_type: EventType
    date_type: CalendarType = CalendarType.SOLAR
    time: str = "00:00:00"
    timezone: str = DEFAULT_TIMEZONE
    repeat_type: RepeatType = RepeatType.NONE
    lunar_month: Optional[int] = None
    lunar_day: Optional[int] = None
    lunar_is_leap_month: bool = False
    quote: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    pinned: bool = False

    def to_dict(self):
        data = asdict(self)
        data["date_type"] = self.date_type.value
        data["event_type"] = self.event_type.value
        data["repeat_type"] = self.repeat_type.value
        return data

    @staticmethod
    def from_dict(data: dict) -> "Event":
        return Event(
            id=data["id"],
            title=data["title"],
            date=data["date"],
            event_type=EventType(data["event_type"]),
            date_type=CalendarType(data.get("date_type", "solar")),
            time=data.get("time", "00:00:00"),
            timezone=data.get("timezone", DEFAULT_TIMEZONE),
            repeat_type=RepeatType(data.get("repeat_type", "none")),
            lunar_month=data.get("lunar_month"),
            lunar_day=data.get("lunar_day"),
            lunar_is_leap_month=data.get("lunar_is_leap_month", False),
            quote=data.get("quote"),
            description=data.get("description"),
            color=data.get("color"),
            pinned=data.get("pinned", False),
        )
