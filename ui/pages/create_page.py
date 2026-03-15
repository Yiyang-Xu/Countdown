import streamlit as st

from ui.components.forms import render_countdown_form


def render_create_page(event_service, event=None):
    is_edit = event is not None
    title = "Edit Countdown" if is_edit else "New Countdown"
    eyebrow = "Edit this moment" if is_edit else "Create a moment"
    subtitle = (
        "回到最初的输入，把这个时刻重新校准。标题、日期、时间与时区都可以改。"
        if is_edit else
        "用最少的信息，记住一个具体时刻。先写下标题，再确定它发生的日期、时间与时区。"
    )

    st.markdown(
        f'<a class="detail-page-back" href="?page={"detail&event_id=" + event.id if is_edit else "dashboard"}" target="_self" aria-label="Back">←</a>',
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <section class="create-shell">
        <div class="create-eyebrow">{eyebrow}</div>
        <h1 class="create-title">{title}</h1>
        <p class="create-subtitle">{subtitle}</p>
    </section>
    """, unsafe_allow_html=True)

    render_countdown_form(
        event_service,
        event=event,
        submit_label="Save Countdown" if is_edit else "Create Countdown",
    )
