import uuid
from typing import List

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

    def create_event(
        self,
        title: str,
        date: str,
        event_type,
        repeat_type,
        description=None,
        color=None,
        pinned=False,
    ):
        events = self.repo.get_all_events()
        new_event = Event(
            id=str(uuid.uuid4()),
            title=title,
            date=date,
            event_type=event_type,
            repeat_type=repeat_type,
            description=description,
            color=color,
            pinned=pinned,
        )
        events.append(new_event)
        self.repo.save_all_events(events)

    def delete_event(self, event_id: str):
        events = self.repo.get_all_events()
        filtered = [event for event in events if event.id != event_id]
        self.repo.save_all_events(filtered)
