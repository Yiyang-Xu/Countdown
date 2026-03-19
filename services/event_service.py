import uuid
from typing import List

from core.calendar_utils import convert_lunar_to_solar, normalize_calendar_type
from core.enums import CalendarType, EventType, RepeatType
from core.models import Event
from core.utils import parse_date
from services.countdown_service import CountdownService


class EventService:
    def __init__(self, repo):
        self.repo = repo

    @staticmethod
    def _normalize_event_date(
        date: str | None,
        date_type,
        lunar_year: int | None = None,
        lunar_month: int | None = None,
        lunar_day: int | None = None,
        lunar_is_leap_month: bool = False,
    ) -> tuple[str, CalendarType, int | None, int | None, bool]:
        normalized_date_type = normalize_calendar_type(date_type)
        if normalized_date_type == CalendarType.SOLAR:
            if not date:
                raise ValueError("请选择一个公历日期。")
            return parse_date(date).isoformat(), normalized_date_type, None, None, False

        if lunar_year is None or lunar_month is None or lunar_day is None:
            raise ValueError("请输入完整的农历年月日。")

        resolved_date = convert_lunar_to_solar(
            lunar_year=lunar_year,
            lunar_month=lunar_month,
            lunar_day=lunar_day,
            is_leap_month=lunar_is_leap_month,
        )
        return (
            resolved_date.isoformat(),
            normalized_date_type,
            lunar_month,
            lunar_day,
            lunar_is_leap_month,
        )

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
        date: str | None,
        time: str,
        country_code: str,
        country_name: str,
        subdivision_name: str,
        city_name: str,
        timezone: str,
        event_type,
        date_type=CalendarType.SOLAR,
        lunar_year: int | None = None,
        lunar_month: int | None = None,
        lunar_day: int | None = None,
        lunar_is_leap_month: bool = False,
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
        resolved_date, resolved_date_type, stored_lunar_month, stored_lunar_day, stored_lunar_is_leap_month = self._normalize_event_date(
            date=date,
            date_type=date_type,
            lunar_year=lunar_year,
            lunar_month=lunar_month,
            lunar_day=lunar_day,
            lunar_is_leap_month=lunar_is_leap_month,
        )
        new_event = Event(
            id=str(uuid.uuid4()),
            title=title,
            date=resolved_date,
            date_type=resolved_date_type,
            time=time,
            timezone=timezone,
            country_code=country_code,
            country_name=country_name,
            subdivision_name=subdivision_name,
            city_name=city_name,
            event_type=event_type,
            repeat_type=repeat_type,
            lunar_month=stored_lunar_month,
            lunar_day=stored_lunar_day,
            lunar_is_leap_month=stored_lunar_is_leap_month,
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
        date: str | None,
        time: str,
        country_code: str,
        country_name: str,
        subdivision_name: str,
        city_name: str,
        timezone: str,
        event_type,
        date_type=CalendarType.SOLAR,
        lunar_year: int | None = None,
        lunar_month: int | None = None,
        lunar_day: int | None = None,
        lunar_is_leap_month: bool = False,
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
        resolved_date, resolved_date_type, stored_lunar_month, stored_lunar_day, stored_lunar_is_leap_month = self._normalize_event_date(
            date=date,
            date_type=date_type,
            lunar_year=lunar_year,
            lunar_month=lunar_month,
            lunar_day=lunar_day,
            lunar_is_leap_month=lunar_is_leap_month,
        )

        updated_event = None
        updated_events = []
        for event in events:
            if event.id == event_id:
                updated_event = Event(
                    id=event.id,
                    title=title,
                    date=resolved_date,
                    date_type=resolved_date_type,
                    time=time,
                    timezone=timezone,
                    country_code=country_code,
                    country_name=country_name,
                    subdivision_name=subdivision_name,
                    city_name=city_name,
                    event_type=event_type,
                    repeat_type=repeat_type,
                    lunar_month=stored_lunar_month,
                    lunar_day=stored_lunar_day,
                    lunar_is_leap_month=stored_lunar_is_leap_month,
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
