import streamlit as st

from ui.components.forms import render_add_event_form


def render_events_page(event_service):
    st.title("My Events")

    col1, col2 = st.columns([1, 1])

    with col1:
        render_add_event_form(event_service)

    with col2:
        st.subheader("Existing Events")
        events = event_service.list_events()

        if not events:
            st.caption("No events found.")
            return

        for event in events:
            with st.container(border=True):
                st.write(f"**{event.title}**")
                st.caption(f"{event.date} · {event.event_type.value} · {event.repeat_type.value}")
                if event.description:
                    st.write(event.description)

                if st.button("Delete", key=f"delete_{event.id}"):
                    event_service.delete_event(event.id)
                    st.success("Deleted.")
                    st.rerun()
