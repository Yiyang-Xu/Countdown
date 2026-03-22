from datetime import date, datetime

from lunar_python import Lunar, LunarYear, Solar

from config.settings import DEFAULT_TIMEZONE
from core.enums import CalendarType
from core.utils import parse_datetime

LUNAR_MONTH_NAMES = {
    1: "正月",
    2: "二月",
    3: "三月",
    4: "四月",
    5: "五月",
    6: "六月",
    7: "七月",
    8: "八月",
    9: "九月",
    10: "十月",
    11: "十一月",
    12: "十二月",
}

LUNAR_DAY_NAMES = {
    1: "初一",
    2: "初二",
    3: "初三",
    4: "初四",
    5: "初五",
    6: "初六",
    7: "初七",
    8: "初八",
    9: "初九",
    10: "初十",
    11: "十一",
    12: "十二",
    13: "十三",
    14: "十四",
    15: "十五",
    16: "十六",
    17: "十七",
    18: "十八",
    19: "十九",
    20: "二十",
    21: "廿一",
    22: "廿二",
    23: "廿三",
    24: "廿四",
    25: "廿五",
    26: "廿六",
    27: "廿七",
    28: "廿八",
    29: "廿九",
    30: "三十",
}


def normalize_calendar_type(value) -> CalendarType:
    if isinstance(value, CalendarType):
        return value
    return CalendarType(value or CalendarType.SOLAR.value)


def solar_to_lunar_parts(solar_date: date) -> dict:
    lunar = Solar.fromYmd(solar_date.year, solar_date.month, solar_date.day).getLunar()
    lunar_month = lunar.getMonth()
    return {
        "year": lunar.getYear(),
        "month": abs(lunar_month),
        "day": lunar.getDay(),
        "is_leap_month": lunar_month < 0,
    }


def get_lunar_leap_month(lunar_year: int) -> int | None:
    leap_month = LunarYear.fromYear(lunar_year).getLeapMonth()
    return leap_month or None


def get_lunar_day_count(lunar_year: int, lunar_month: int, is_leap_month: bool = False) -> int:
    month_value = -lunar_month if is_leap_month else lunar_month
    return LunarYear.fromYear(lunar_year).getMonth(month_value).getDayCount()


def validate_lunar_date(
    lunar_year: int,
    lunar_month: int,
    lunar_day: int,
    is_leap_month: bool = False,
) -> None:
    if not 1 <= lunar_month <= 12:
        raise ValueError("农历月份必须在 1 到 12 之间。")

    leap_month = get_lunar_leap_month(lunar_year)
    if is_leap_month and leap_month != lunar_month:
        raise ValueError(f"{lunar_year} 年没有闰{lunar_month}月。")

    max_day = get_lunar_day_count(lunar_year, lunar_month, is_leap_month)
    if not 1 <= lunar_day <= max_day:
        raise ValueError(f"{lunar_year} 年农历 {'闰' if is_leap_month else ''}{lunar_month}月只有 {max_day} 天。")


def convert_lunar_to_solar(
    lunar_year: int,
    lunar_month: int,
    lunar_day: int,
    is_leap_month: bool = False,
) -> date:
    validate_lunar_date(lunar_year, lunar_month, lunar_day, is_leap_month)
    month_value = -lunar_month if is_leap_month else lunar_month
    solar = Lunar.fromYmd(lunar_year, month_value, lunar_day).getSolar()
    return date(solar.getYear(), solar.getMonth(), solar.getDay())


def resolve_next_lunar_occurrence(
    lunar_month: int,
    lunar_day: int,
    is_leap_month: bool,
    current_datetime: datetime,
    event_time: str = "00:00:00",
    timezone_str: str = DEFAULT_TIMEZONE,
) -> datetime:
    current_date = current_datetime.date()
    current_lunar = Solar.fromYmd(current_date.year, current_date.month, current_date.day).getLunar()
    start_year = current_lunar.getYear()

    for lunar_year in range(start_year, start_year + 20):
        try:
            solar_date = convert_lunar_to_solar(lunar_year, lunar_month, lunar_day, is_leap_month)
        except ValueError:
            continue

        candidate = parse_datetime(solar_date.isoformat(), event_time, timezone_str)
        if candidate >= current_datetime:
            return candidate

    raise ValueError("无法在未来 20 个农历年内找到下一次对应日期。")


def format_event_date_summary(
    date_type,
    solar_date: str,
    lunar_month: int | None = None,
    lunar_day: int | None = None,
    lunar_is_leap_month: bool = False,
) -> str:
    calendar_type = normalize_calendar_type(date_type)
    if calendar_type == CalendarType.LUNAR and lunar_month and lunar_day:
        return f"农历 {format_lunar_month(lunar_month, lunar_is_leap_month)}{format_lunar_day(lunar_day)} · 公历 {solar_date}"
    return f"公历 {solar_date}"


def format_lunar_month(lunar_month: int, is_leap_month: bool = False) -> str:
    prefix = "闰" if is_leap_month else ""
    return f"{prefix}{LUNAR_MONTH_NAMES[lunar_month]}"


def format_lunar_day(lunar_day: int) -> str:
    return LUNAR_DAY_NAMES[lunar_day]
