from dataclasses import dataclass, asdict
from typing import Optional

from core.enums import EventType, RepeatType


@dataclass
class Event:
    id: str
    title: str
    date: str
    event_type: EventType
    repeat_type: RepeatType = RepeatType.NONE
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
            event_type=EventType(data["event_type"]),
            repeat_type=RepeatType(data.get("repeat_type", "none")),
            description=data.get("description"),
            color=data.get("color"),
            pinned=data.get("pinned", False),
        )
