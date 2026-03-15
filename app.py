import streamlit as st

from config.settings import APP_TITLE, PAGE_ICON
from repository.event_repository import EventRepository
from services.event_service import EventService
from ui.pages.create_page import render_create_page
from ui.styles import inject_global_styles
from ui.pages.detail_page import render_detail_page
from ui.pages.dashboard_page import render_dashboard_page


def main():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=PAGE_ICON,
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    inject_global_styles()

    repo = EventRepository()
    event_service = EventService(repo)

    query_page = st.query_params.get("page", "dashboard")
    event_id = st.query_params.get("event_id")

    if query_page == "detail" and event_id:
        render_detail_page(event_service, event_id)
        return

    if query_page == "create":
        render_create_page(event_service)
        return

    if query_page == "edit" and event_id:
        event = event_service.get_event_by_id(event_id)
        if not event:
            st.error("This countdown could not be found.")
            st.markdown(
                '<a class="detail-page-back" href="?page=dashboard" target="_self" aria-label="Back to dashboard">←</a>',
                unsafe_allow_html=True
            )
            return
        render_create_page(event_service, event=event)
        return

    if query_page != "dashboard":
        st.query_params.clear()
        st.query_params["page"] = "dashboard"
        render_dashboard_page(event_service)
        return

    render_dashboard_page(event_service)


if __name__ == "__main__":
    main()
