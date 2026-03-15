import streamlit as st

from core.enums import EventType, RepeatType


def render_add_event_form(event_service):
    with st.form("add_event_form", clear_on_submit=True):
        st.subheader("Add New Event")

        title = st.text_input("Title")
        date_value = st.date_input("Date")
        event_type = st.selectbox(
            "Event Type",
            options=list(EventType),
            format_func=lambda x: x.value,
        )
        repeat_type = st.selectbox(
            "Repeat Type",
            options=list(RepeatType),
            format_func=lambda x: x.value,
        )
        description = st.text_area("Description")
        pinned = st.checkbox("Pin this event")

        submitted = st.form_submit_button("Create Event")

        if submitted and title:
            event_service.create_event(
                title=title,
                date=date_value.isoformat(),
                event_type=event_type,
                repeat_type=repeat_type,
                description=description,
                pinned=pinned,
            )
            st.success("Event created successfully.")
            st.rerun()
