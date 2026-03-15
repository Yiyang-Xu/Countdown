from datetime import date

from core.enums import EventType, RepeatType
from core.models import Event
from core.utils import parse_date, today


class CountdownService:
    @staticmethod
    def calculate_event_status(event: Event) -> dict:
        base_date = parse_date(event.date)
        current = today()

        if event.event_type == EventType.COUNTUP:
            days_passed = (current - base_date).days
            return {
                "primary_text": f"已经过去 {days_passed} 天",
                "days_value": days_passed,
                "status": "passed" if days_passed >= 0 else "future",
            }

        if event.event_type == EventType.COUNTDOWN:
            days_left = (base_date - current).days
            if days_left > 0:
                return {
                    "primary_text": f"还有 {days_left} 天",
                    "days_value": days_left,
                    "status": "upcoming",
                }
            elif days_left == 0:
                return {
                    "primary_text": "就是今天",
                    "days_value": 0,
                    "status": "today",
                }
            return {
                "primary_text": f"已过去 {abs(days_left)} 天",
                "days_value": abs(days_left),
                "status": "passed",
            }

        if event.repeat_type == RepeatType.YEARLY:
            next_occurrence = base_date.replace(year=current.year)
            if next_occurrence < current:
                next_occurrence = next_occurrence.replace(year=current.year + 1)

            days_left = (next_occurrence - current).days
            return {
                "primary_text": f"距离下一次还有 {days_left} 天" if days_left > 0 else "就是今天",
                "days_value": days_left,
                "status": "today" if days_left == 0 else "upcoming",
                "next_date": next_occurrence.isoformat(),
            }

        days_diff = (base_date - current).days
        return {
            "primary_text": f"还有 {days_diff} 天" if days_diff >= 0 else f"已过去 {abs(days_diff)} 天",
            "days_value": abs(days_diff),
            "status": "upcoming" if days_diff >= 0 else "passed",
        }
