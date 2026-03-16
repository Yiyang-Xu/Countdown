from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import streamlit as st

from config.settings import DEFAULT_TIMEZONE
from core.calendar_utils import (
    convert_lunar_to_solar,
    format_lunar_day,
    format_lunar_month,
    get_lunar_day_count,
    solar_to_lunar_parts,
)
from core.enums import CalendarType, EventType
from core.utils import parse_date
from lunar_python import LunarYear


EVENT_TYPE_LABELS = {
    EventType.COUNTUP: "正计时",
    EventType.COUNTDOWN: "倒计时",
    EventType.ANNIVERSARY: "Anniversary",
    EventType.BIRTHDAY: "Birthday",
}

CALENDAR_TYPE_LABELS = {
    CalendarType.SOLAR: "公历",
    CalendarType.LUNAR: "农历",
}

TIMEZONE_CITY_OPTIONS = [
    ("Pacific/Honolulu", "Honolulu"),
    ("America/Anchorage", "Anchorage"),
    ("America/Los_Angeles", "Los Angeles"),
    ("America/Denver", "Denver"),
    ("America/Chicago", "Chicago"),
    ("America/New_York", "New York"),
    ("America/Toronto", "Toronto"),
    ("America/Sao_Paulo", "Sao Paulo"),
    ("America/Buenos_Aires", "Buenos Aires"),
    ("Atlantic/Reykjavik", "Reykjavik"),
    ("Europe/London", "London"),
    ("Europe/Paris", "Paris"),
    ("Europe/Berlin", "Berlin"),
    ("Europe/Madrid", "Madrid"),
    ("Europe/Rome", "Rome"),
    ("Europe/Athens", "Athens"),
    ("Europe/Helsinki", "Helsinki"),
    ("Europe/Moscow", "Moscow"),
    ("Africa/Cairo", "Cairo"),
    ("Africa/Johannesburg", "Johannesburg"),
    ("Asia/Dubai", "Dubai"),
    ("Asia/Karachi", "Karachi"),
    ("Asia/Kolkata", "New Delhi"),
    ("Asia/Dhaka", "Dhaka"),
    ("Asia/Bangkok", "Bangkok"),
    ("Asia/Shanghai", "Beijing"),
    ("Asia/Hong_Kong", "Hong Kong"),
    ("Asia/Singapore", "Singapore"),
    ("Asia/Tokyo", "Tokyo"),
    ("Asia/Seoul", "Seoul"),
    ("Australia/Perth", "Perth"),
    ("Australia/Sydney", "Sydney"),
    ("Pacific/Auckland", "Auckland"),
    ("UTC", "UTC"),
]


def _format_offset(timezone_name: str) -> str:
    now_in_zone = datetime.now(ZoneInfo(timezone_name))
    offset = now_in_zone.utcoffset()
    if offset is None:
        return "UTC+00:00"

    total_minutes = int(offset.total_seconds() // 60)
    sign = "+" if total_minutes >= 0 else "-"
    total_minutes = abs(total_minutes)
    hours, minutes = divmod(total_minutes, 60)
    return f"UTC{sign}{hours:02d}:{minutes:02d}"


TIMEZONE_LABELS = {
    timezone_name: f"{city_name} · {_format_offset(timezone_name)} · {timezone_name}"
    for timezone_name, city_name in TIMEZONE_CITY_OPTIONS
}


def _init_widget_state(key: str, value):
    if key not in st.session_state:
        st.session_state[key] = value


def _month_option_value(lunar_month: int, is_leap_month: bool) -> str:
    return f"{lunar_month}:{1 if is_leap_month else 0}"


def _parse_month_option(value: str) -> tuple[int, bool]:
    month_text, is_leap_text = value.split(":")
    return int(month_text), is_leap_text == "1"


def _build_lunar_month_options(lunar_year: int | None) -> list[str]:
    if lunar_year is None:
        return []

    options = []
    for month in LunarYear.fromYear(lunar_year).getMonthsInYear():
        options.append(_month_option_value(abs(month.getMonth()), month.isLeap()))
    return options


def _format_lunar_month_option(value: str) -> str:
    lunar_month, is_leap_month = _parse_month_option(value)
    return format_lunar_month(lunar_month, is_leap_month)


def render_countdown_form(
    event_service,
    event=None,
    submit_label: str = "Create Countdown",
):
    is_edit = event is not None
    form_key = f"countdown_form_{event.id}" if is_edit else "create_countdown_form"
    default_title = event.title if is_edit else ""
    default_type = event.event_type if is_edit else EventType.COUNTDOWN
    default_date_type = event.date_type if is_edit else CalendarType.SOLAR
    default_date = parse_date(event.date) if is_edit else datetime.now().date()
    default_time = event.time if is_edit else "00:00:00"
    default_hour, default_minute, _ = default_time.split(":")
    default_timezone = event.timezone if is_edit else DEFAULT_TIMEZONE
    default_lunar = (
        {
            "year": default_date.year,
            "month": event.lunar_month,
            "day": event.lunar_day,
            "is_leap_month": event.lunar_is_leap_month,
        }
        if is_edit and event.date_type == CalendarType.LUNAR and event.lunar_month and event.lunar_day
        else solar_to_lunar_parts(default_date or datetime.now().date())
    )
    title_key = f"{form_key}_title"
    type_key = f"{form_key}_type"
    date_type_key = f"{form_key}_date_type"
    solar_date_key = f"{form_key}_solar_date"
    lunar_year_key = f"{form_key}_lunar_year"
    lunar_month_key = f"{form_key}_lunar_month"
    lunar_day_key = f"{form_key}_lunar_day"
    hour_key = f"{form_key}_hour"
    minute_key = f"{form_key}_minute"
    timezone_key = f"{form_key}_timezone"

    _init_widget_state(title_key, default_title)
    _init_widget_state(type_key, default_type)
    _init_widget_state(date_type_key, default_date_type)
    _init_widget_state(solar_date_key, default_date)
    _init_widget_state(
        lunar_year_key,
        int(default_lunar["year"]) if is_edit and default_date_type == CalendarType.LUNAR else None,
    )
    _init_widget_state(
        lunar_month_key,
        _month_option_value(int(default_lunar["month"]), bool(default_lunar["is_leap_month"]))
        if is_edit and default_date_type == CalendarType.LUNAR and default_lunar["month"]
        else None,
    )
    _init_widget_state(
        lunar_day_key,
        int(default_lunar["day"]) if is_edit and default_date_type == CalendarType.LUNAR else None,
    )
    _init_widget_state(hour_key, default_hour)
    _init_widget_state(minute_key, default_minute)
    _init_widget_state(timezone_key, default_timezone)
    with st.container():
        st.markdown('<div class="create-form-marker"></div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="form-section-heading">
            <div class="form-section-kicker">Basic Info</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="field-label">Pick a title</div>', unsafe_allow_html=True)
        title = st.text_input(
            "Pick a title",
            key=title_key,
            label_visibility="collapsed",
            placeholder="例如：东京的第一天 / 结婚纪念日 / 和她见面的那个晚上",
        )

        st.markdown("""
        <div class="form-section-heading">
            <div class="form-section-kicker">Date</div>
        </div>
        """, unsafe_allow_html=True)
        type_col, calendar_col = st.columns(2, gap="medium")
        with type_col:
            st.markdown('<div class="field-label">Choose a type</div>', unsafe_allow_html=True)
            event_type = st.selectbox(
                "Type",
                options=list(EventType),
                key=type_key,
                format_func=lambda x: EVENT_TYPE_LABELS[x],
                label_visibility="collapsed",
            )
        with calendar_col:
            st.markdown('<div class="field-label">Calendar</div>', unsafe_allow_html=True)
            date_type = st.selectbox(
                "Calendar",
                options=list(CalendarType),
                key=date_type_key,
                format_func=lambda x: CALENDAR_TYPE_LABELS[x],
                label_visibility="collapsed",
            )

        date_value = None
        lunar_year = None
        lunar_month = None
        lunar_day = None
        lunar_is_leap_month = False

        if date_type == CalendarType.SOLAR:
            st.markdown('<div class="field-label">Pick a date</div>', unsafe_allow_html=True)
            date_value = st.date_input(
                "Pick a date",
                key=solar_date_key,
                label_visibility="collapsed",
            )
        else:
            st.markdown('<div class="field-label">Pick a lunar date</div>', unsafe_allow_html=True)

            year_options = list(range(1900, 2201))
            lunar_year = st.selectbox(
                "Lunar year",
                options=year_options,
                key=lunar_year_key,
                index=None if st.session_state[lunar_year_key] is None else year_options.index(st.session_state[lunar_year_key]),
                placeholder="先选择年份",
                format_func=lambda value: f"{value}年",
                label_visibility="collapsed",
            )

            month_options = _build_lunar_month_options(lunar_year)
            if st.session_state[lunar_month_key] not in month_options:
                st.session_state[lunar_month_key] = None

            lunar_month_col, lunar_day_col = st.columns(2, gap="medium")
            with lunar_month_col:
                selected_month_option = st.selectbox(
                    "Lunar month",
                    options=month_options,
                    key=lunar_month_key,
                    index=None if st.session_state[lunar_month_key] is None else month_options.index(st.session_state[lunar_month_key]),
                    placeholder="先选择月份",
                    format_func=_format_lunar_month_option,
                    label_visibility="collapsed",
                    disabled=lunar_year is None,
                )

            if selected_month_option is not None:
                lunar_month, lunar_is_leap_month = _parse_month_option(selected_month_option)
                day_options = list(range(1, get_lunar_day_count(int(lunar_year), lunar_month, lunar_is_leap_month) + 1))
            else:
                day_options = []

            if st.session_state[lunar_day_key] not in day_options:
                st.session_state[lunar_day_key] = None

            with lunar_day_col:
                lunar_day = st.selectbox(
                    "Lunar day",
                    options=day_options,
                    key=lunar_day_key,
                    index=None if st.session_state[lunar_day_key] is None else day_options.index(st.session_state[lunar_day_key]),
                    placeholder="先选择日期",
                    format_func=lambda value: format_lunar_day(value),
                    label_visibility="collapsed",
                    disabled=selected_month_option is None,
                )

            if lunar_year is not None and selected_month_option is not None and lunar_day is not None:
                resolved_solar = convert_lunar_to_solar(
                    lunar_year=int(lunar_year),
                    lunar_month=lunar_month,
                    lunar_day=lunar_day,
                    is_leap_month=lunar_is_leap_month,
                )
                st.caption(f"对应公历日期：{resolved_solar.isoformat()}")

        st.markdown("""
        <div class="form-section-heading">
            <div class="form-section-kicker">Time</div>
            <div class="form-section-title">补充时间与时区</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="field-label">Pick a time</div>', unsafe_allow_html=True)
        hour_col, minute_col = st.columns(2, gap="medium")
        with hour_col:
            hour_value = st.selectbox(
                "Hour",
                options=[f"{hour:02d}" for hour in range(24)],
                key=hour_key,
                label_visibility="collapsed",
            )
        with minute_col:
            minute_value = st.selectbox(
                "Minute",
                options=[f"{minute:02d}" for minute in range(60)],
                key=minute_key,
                label_visibility="collapsed",
            )

        st.markdown('<div class="field-label">Timezone</div>', unsafe_allow_html=True)
        timezone_values = [timezone_name for timezone_name, _ in TIMEZONE_CITY_OPTIONS]
        if st.session_state[timezone_key] not in timezone_values:
            st.session_state[timezone_key] = DEFAULT_TIMEZONE
        timezone_text = st.selectbox(
            "Timezone",
            options=timezone_values,
            key=timezone_key,
            format_func=lambda timezone_name: TIMEZONE_LABELS[timezone_name],
            label_visibility="collapsed",
        )

        st.markdown("""
        <div class="form-section-heading">
            <div class="form-section-kicker">Appearance</div>
            <div class="form-section-title">预留一点视觉风格</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="field-label">Color</div>
        <div class="color-placeholder">Color palette coming later.</div>
        """, unsafe_allow_html=True)

        submitted = st.button(submit_label, key=f"{form_key}_submit", use_container_width=False)

    if submitted:
        if not title.strip():
            st.error("Please enter a title.")
            return

        time_text = f"{hour_value}:{minute_value}:00"
        try:
            normalized_time = datetime.strptime(time_text, "%H:%M:%S").strftime("%H:%M:%S")
        except ValueError:
            st.error("Time must use a valid HH:MM:SS value.")
            return

        try:
            ZoneInfo(timezone_text)
        except ZoneInfoNotFoundError:
            st.error("Timezone must be a valid IANA timezone.")
            return

        payload = dict(
            title=title.strip(),
            date=date_value.isoformat() if date_value else None,
            time=normalized_time,
            timezone=timezone_text,
            event_type=event_type,
            date_type=date_type,
            lunar_year=int(lunar_year) if lunar_year else None,
            lunar_month=lunar_month,
            lunar_day=lunar_day,
            lunar_is_leap_month=lunar_is_leap_month,
        )

        try:
            if is_edit:
                updated_event = event_service.update_event(event.id, **payload)
                if not updated_event:
                    st.error("This countdown could not be updated.")
                    return
                st.query_params.clear()
                st.query_params["page"] = "detail"
                st.query_params["event_id"] = event.id
            else:
                created_event = event_service.create_event(**payload)
                st.query_params.clear()
                st.query_params["page"] = "detail"
                st.query_params["event_id"] = created_event.id
        except ValueError as exc:
            st.error(str(exc))
            return
        st.rerun()


def render_create_countdown_form(event_service):
    render_countdown_form(event_service)
