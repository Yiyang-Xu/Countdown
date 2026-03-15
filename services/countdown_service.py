from datetime import datetime

from core.enums import EventType, RepeatType
from core.models import Event
from core.utils import parse_date, parse_datetime, now


class CountdownService:
    @staticmethod
    def _split_duration(total_seconds: int) -> dict:
        total_seconds = max(0, abs(total_seconds))
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        return {
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
        }

    @staticmethod
    def _safe_replace_year(source: datetime, year: int) -> datetime:
        try:
            return source.replace(year=year)
        except ValueError:
            # Fall back for leap-day dates on non-leap years.
            return source.replace(year=year, month=2, day=28)

    @staticmethod
    def calculate_event_status(event: Event) -> dict:
        base_datetime = parse_datetime(event.date, event.time, event.timezone)
        current_datetime = now(event.timezone)
        base_date = base_datetime.date()
        current = current_datetime.date()

        if event.event_type == EventType.COUNTUP:
            days_passed = (current - base_date).days
            seconds_diff = int((current_datetime - base_datetime).total_seconds())
            return {
                "primary_text": f"已经过去 {days_passed} 天",
                "days_value": days_passed,
                "status": "passed" if days_passed >= 0 else "future",
                "detail_parts": CountdownService._split_duration(seconds_diff),
                "target_datetime": base_datetime.isoformat(),
                "detail_mode": "countup",
                "timezone": event.timezone,
            }

        if event.event_type == EventType.COUNTDOWN:
            days_left = (base_date - current).days
            seconds_left = int((base_datetime - current_datetime).total_seconds())
            if seconds_left > 0 and days_left > 0:
                return {
                    "primary_text": f"还有 {days_left} 天",
                    "days_value": days_left,
                    "status": "upcoming",
                    "detail_parts": CountdownService._split_duration(seconds_left),
                    "target_datetime": base_datetime.isoformat(),
                    "detail_mode": "countdown",
                    "timezone": event.timezone,
                }
            elif seconds_left > 0:
                return {
                    "primary_text": "就是今天",
                    "days_value": 0,
                    "status": "today",
                    "detail_parts": CountdownService._split_duration(seconds_left),
                    "target_datetime": base_datetime.isoformat(),
                    "detail_mode": "countdown",
                    "timezone": event.timezone,
                }
            return {
                "primary_text": f"已过去 {abs(days_left)} 天",
                "days_value": abs(days_left),
                "status": "passed",
                "detail_parts": CountdownService._split_duration(seconds_left),
                "target_datetime": base_datetime.isoformat(),
                "detail_mode": "countup",
                "timezone": event.timezone,
            }

        if event.repeat_type == RepeatType.YEARLY:
            next_occurrence = CountdownService._safe_replace_year(base_datetime, current_datetime.year)
            if next_occurrence < current_datetime:
                next_occurrence = CountdownService._safe_replace_year(base_datetime, current_datetime.year + 1)

            days_left = (next_occurrence.date() - current).days
            seconds_left = int((next_occurrence - current_datetime).total_seconds())
            return {
                "primary_text": f"距离下一次还有 {days_left} 天" if days_left > 0 else "就是今天",
                "days_value": days_left,
                "status": "today" if days_left == 0 else "upcoming",
                "next_date": next_occurrence.date().isoformat(),
                "detail_parts": CountdownService._split_duration(seconds_left),
                "target_datetime": next_occurrence.isoformat(),
                "detail_mode": "countdown",
                "timezone": event.timezone,
            }

        seconds_diff = int((base_datetime - current_datetime).total_seconds())
        days_diff = (base_date - current).days
        is_upcoming = seconds_diff >= 0
        primary_text = f"还有 {days_diff} 天" if is_upcoming else f"已过去 {abs(days_diff)} 天"
        return {
            "primary_text": primary_text,
            "days_value": abs(days_diff),
            "status": "upcoming" if is_upcoming else "passed",
            "detail_parts": CountdownService._split_duration(seconds_diff),
            "target_datetime": base_datetime.isoformat(),
            "detail_mode": "countdown" if is_upcoming else "countup",
            "timezone": event.timezone,
        }
