from datetime import datetime

import streamlit as st

from core.calendar_utils import (
    convert_lunar_to_solar,
    format_lunar_day,
    format_lunar_month,
    get_lunar_day_count,
    solar_to_lunar_parts,
)
from core.enums import CalendarType, EventType
from core.location_data import (
    get_country_options,
    get_subdivision_options,
    infer_location_from_timezone,
    resolve_location,
)
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
    default_location = (
        {
            "country_code": event.country_code or "",
            "country_name": event.country_name or "",
            "subdivision_name": event.subdivision_name or "",
            "city_name": event.city_name or "",
            "timezone": event.timezone,
        }
        if is_edit and event.country_code and event.subdivision_name
        else infer_location_from_timezone(event.timezone if is_edit else "America/New_York")
    )
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
    country_key = f"{form_key}_country"
    subdivision_key = f"{form_key}_subdivision"

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
    _init_widget_state(country_key, default_location["country_code"])
    _init_widget_state(subdivision_key, default_location["subdivision_name"])
    try:
        country_options = get_country_options()
    except RuntimeError as exc:
        st.error(str(exc))
        return
    country_codes = [country["code"] for country in country_options]
    country_labels = {country["code"]: country["name"] for country in country_options}
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
            <div class="form-section-title">补充发生时间</div>
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

        st.markdown("""
        <div class="form-section-heading">
            <div class="form-section-kicker">Location</div>
            <div class="form-section-title">让地点决定时区，但不把时区展示出来</div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state[country_key] not in country_codes:
            st.session_state[country_key] = (
                default_location["country_code"]
                if default_location["country_code"] in country_codes
                else "US" if "US" in country_codes else country_codes[0]
            )

        country_col, subdivision_col = st.columns(2, gap="medium")
        with country_col:
            st.markdown('<div class="field-label">Country</div>', unsafe_allow_html=True)
            country_code = st.selectbox(
                "Country",
                options=country_codes,
                key=country_key,
                format_func=lambda value: country_labels.get(value, value),
                label_visibility="collapsed",
            )

        subdivision_options = get_subdivision_options(country_code)
        subdivision_names = [item["name"] for item in subdivision_options]
        if st.session_state[subdivision_key] not in subdivision_names:
            st.session_state[subdivision_key] = subdivision_names[0] if subdivision_names else ""

        subdivision_label = "Province" if country_code == "CN" else "State" if country_code == "US" else "Region"
        with subdivision_col:
            st.markdown(f'<div class="field-label">{subdivision_label}</div>', unsafe_allow_html=True)
            subdivision_name = st.selectbox(
                subdivision_label,
                options=subdivision_names,
                key=subdivision_key,
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

        resolved_location = resolve_location(country_code, subdivision_name)
        if not resolved_location:
            st.error("Please choose a valid country and state/province.")
            return

        payload = dict(
            title=title.strip(),
            date=date_value.isoformat() if date_value else None,
            time=normalized_time,
            country_code=resolved_location["country_code"],
            country_name=resolved_location["country_name"],
            subdivision_name=resolved_location["subdivision_name"],
            city_name=resolved_location["city_name"],
            timezone=resolved_location["timezone"],
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
