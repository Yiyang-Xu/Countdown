import uuid
from typing import List

from core.enums import EventType, RepeatType
from core.models import Event
from services.countdown_service import CountdownService


class EventService:
    def __init__(self, repo):
        self.repo = repo

    def list_events(self) -> List[Event]:
        return self.repo.get_all_events()

    def list_events_with_status(self) -> list[dict]:
        events = self.repo.get_all_events()
        enriched = []
        for event in events:
            status_info = CountdownService.calculate_event_status(event)
            enriched.append({
                "event": event,
                "status_info": status_info
            })
        return enriched

    def get_event_by_id(self, event_id: str) -> Event | None:
        for event in self.repo.get_all_events():
            if event.id == event_id:
                return event
        return None

    def get_event_with_status(self, event_id: str) -> dict | None:
        event = self.get_event_by_id(event_id)
        if not event:
            return None
        return {
            "event": event,
            "status_info": CountdownService.calculate_event_status(event),
        }

    def create_event(
        self,
        title: str,
        date: str,
        time: str,
        timezone: str,
        event_type,
        quote=None,
        description=None,
        color=None,
        pinned=False,
    ):
        events = self.repo.get_all_events()
        repeat_type = (
            RepeatType.YEARLY
            if event_type in {EventType.BIRTHDAY, EventType.ANNIVERSARY}
            else RepeatType.NONE
        )
        new_event = Event(
            id=str(uuid.uuid4()),
            title=title,
            date=date,
            time=time,
            timezone=timezone,
            event_type=event_type,
            repeat_type=repeat_type,
            quote=quote,
            description=description,
            color=color,
            pinned=pinned,
        )
        events.append(new_event)
        self.repo.save_all_events(events)
        return new_event

    def update_event(
        self,
        event_id: str,
        title: str,
        date: str,
        time: str,
        timezone: str,
        event_type,
        quote=None,
        description=None,
        color=None,
        pinned=False,
    ) -> Event | None:
        events = self.repo.get_all_events()
        repeat_type = (
            RepeatType.YEARLY
            if event_type in {EventType.BIRTHDAY, EventType.ANNIVERSARY}
            else RepeatType.NONE
        )

        updated_event = None
        updated_events = []
        for event in events:
            if event.id == event_id:
                updated_event = Event(
                    id=event.id,
                    title=title,
                    date=date,
                    time=time,
                    timezone=timezone,
                    event_type=event_type,
                    repeat_type=repeat_type,
                    quote=quote,
                    description=description,
                    color=color,
                    pinned=pinned,
                )
                updated_events.append(updated_event)
            else:
                updated_events.append(event)

        if updated_event is None:
            return None

        self.repo.save_all_events(updated_events)
        return updated_event

    def delete_event(self, event_id: str):
        events = self.repo.get_all_events()
        filtered = [event for event in events if event.id != event_id]
        self.repo.save_all_events(filtered)
