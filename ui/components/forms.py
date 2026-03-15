from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import streamlit as st

from config.settings import DEFAULT_TIMEZONE
from core.enums import EventType
from core.utils import parse_date


EVENT_TYPE_LABELS = {
    EventType.COUNTUP: "正计时",
    EventType.COUNTDOWN: "倒计时",
    EventType.ANNIVERSARY: "Anniversary",
    EventType.BIRTHDAY: "Birthday",
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

def render_countdown_form(
    event_service,
    event=None,
    submit_label: str = "Create Countdown",
):
    is_edit = event is not None
    form_key = f"countdown_form_{event.id}" if is_edit else "create_countdown_form"
    default_title = event.title if is_edit else ""
    default_type = event.event_type if is_edit else EventType.COUNTDOWN
    default_date = parse_date(event.date) if is_edit else None
    default_time = event.time if is_edit else "00:00:00"
    default_hour, default_minute, _ = default_time.split(":")
    default_timezone = event.timezone if is_edit else DEFAULT_TIMEZONE

    with st.form(form_key, clear_on_submit=False):
        st.markdown('<div class="field-label">Pick a title</div>', unsafe_allow_html=True)
        title = st.text_input(
            "Pick a title",
            label_visibility="collapsed",
            placeholder="例如：东京的第一天 / 结婚纪念日 / 和她见面的那个晚上",
            value=default_title,
        )

        st.markdown('<div class="field-label">Choose a type</div>', unsafe_allow_html=True)
        event_type = st.selectbox(
            "Type",
            options=list(EventType),
            format_func=lambda x: EVENT_TYPE_LABELS[x],
            label_visibility="collapsed",
            index=list(EventType).index(default_type),
        )

        st.markdown('<div class="field-label">Pick a date</div>', unsafe_allow_html=True)
        date_value = st.date_input(
            "Pick a date",
            label_visibility="collapsed",
            value=default_date,
        )

        st.markdown('<div class="field-label">Pick a time</div>', unsafe_allow_html=True)
        hour_col, minute_col = st.columns(2, gap="medium")
        with hour_col:
            hour_value = st.selectbox(
                "Hour",
                options=[f"{hour:02d}" for hour in range(24)],
                label_visibility="collapsed",
                index=int(default_hour),
            )
        with minute_col:
            minute_value = st.selectbox(
                "Minute",
                options=[f"{minute:02d}" for minute in range(60)],
                label_visibility="collapsed",
                index=int(default_minute),
            )

        st.markdown('<div class="field-label">Timezone</div>', unsafe_allow_html=True)
        timezone_values = [timezone_name for timezone_name, _ in TIMEZONE_CITY_OPTIONS]
        default_timezone_index = timezone_values.index(default_timezone) if default_timezone in timezone_values else 0
        timezone_text = st.selectbox(
            "Timezone",
            options=timezone_values,
            index=default_timezone_index,
            format_func=lambda timezone_name: TIMEZONE_LABELS[timezone_name],
            label_visibility="collapsed",
        )

        st.markdown("""
        <div class="field-label">Color</div>
        <div class="color-placeholder">Color palette coming later.</div>
        """, unsafe_allow_html=True)

        st.markdown(f'<div class="submit-wrap">', unsafe_allow_html=True)
        submitted = st.form_submit_button(submit_label)
        st.markdown('</div>', unsafe_allow_html=True)

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
                date=date_value.isoformat(),
                time=normalized_time,
                timezone=timezone_text,
                event_type=event_type,
            )

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
            st.rerun()


def render_create_countdown_form(event_service):
    render_countdown_form(event_service)
