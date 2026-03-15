import streamlit as st


def render_event_card(
    event_id: str,
    title: str,
    stat_value: str,
    stat_unit: str,
    stat_label: str,
    meta_text: str,
    badge_text: str,
    tone_class: str,
):
    st.markdown(f"""
    <a class="event-card-link" href="?page=detail&event_id={event_id}" target="_self">
    <div class="event-card {tone_class}">
        <div class="event-card-topline">{badge_text}</div>
        <div class="event-main-block">
            <div class="event-main">{stat_value}</div>
            <div class="event-unit">{stat_unit}</div>
        </div>
        <div class="event-label">{stat_label}</div>
        <div class="event-title">{title}</div>
        <div class="event-meta">{meta_text}</div>
    </div>
    </a>
    """, unsafe_allow_html=True)
