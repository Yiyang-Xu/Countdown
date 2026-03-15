import streamlit as st

from config.settings import APP_TITLE, PAGE_ICON
from repository.event_repository import EventRepository
from services.event_service import EventService
from ui.styles import inject_global_styles
from ui.pages.dashboard_page import render_dashboard_page
from ui.pages.events_page import render_events_page


def main():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=PAGE_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_global_styles()

    repo = EventRepository()
    event_service = EventService(repo)

    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Dashboard", "My Events"],
        label_visibility="collapsed"
    )

    if page == "Dashboard":
        render_dashboard_page(event_service)
    elif page == "My Events":
        render_events_page(event_service)


if __name__ == "__main__":
    main()
