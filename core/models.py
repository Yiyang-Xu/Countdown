from dataclasses import dataclass, asdict
from typing import Optional

from config.settings import DEFAULT_TIMEZONE
from core.enums import EventType, RepeatType


@dataclass
class Event:
    id: str
    title: str
    date: str
    event_type: EventType
    time: str = "00:00:00"
    timezone: str = DEFAULT_TIMEZONE
    repeat_type: RepeatType = RepeatType.NONE
    quote: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    pinned: bool = False

    def to_dict(self):
        data = asdict(self)
        data["event_type"] = self.event_type.value
        data["repeat_type"] = self.repeat_type.value
        return data

    @staticmethod
    def from_dict(data: dict) -> "Event":
        return Event(
            id=data["id"],
            title=data["title"],
            date=data["date"],
            time=data.get("time", "00:00:00"),
            timezone=data.get("timezone", DEFAULT_TIMEZONE),
            event_type=EventType(data["event_type"]),
            repeat_type=RepeatType(data.get("repeat_type", "none")),
            quote=data.get("quote"),
            description=data.get("description"),
            color=data.get("color"),
            pinned=data.get("pinned", False),
        )
