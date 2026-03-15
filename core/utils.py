from datetime import date, datetime
from zoneinfo import ZoneInfo

from config.settings import DEFAULT_TIMEZONE


def parse_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def parse_datetime(
    date_str: str,
    time_str: str = "00:00:00",
    timezone_str: str = DEFAULT_TIMEZONE,
) -> datetime:
    naive = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
    return naive.replace(tzinfo=ZoneInfo(timezone_str))


def today() -> date:
    return date.today()


def now(timezone_str: str = DEFAULT_TIMEZONE) -> datetime:
    return datetime.now(ZoneInfo(timezone_str))
