import streamlit as st

from ui.components.cards import render_event_card


def render_dashboard_page(event_service):
    st.markdown('<div class="app-title">Life Countdown</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-subtitle">记录重要时刻，也记录生活的仪式感。</div>',
        unsafe_allow_html=True
    )

    events = event_service.list_events_with_status()

    if not events:
        st.info("No events yet. Go to 'My Events' to create your first one.")
        return

    st.subheader("Highlights")

    for item in events:
        event = item["event"]
        status_info = item["status_info"]
        meta = f"{event.date} · {event.event_type.value} · {event.repeat_type.value}"
        render_event_card(
            title=event.title,
            primary_text=status_info["primary_text"],
            meta_text=meta,
        )
