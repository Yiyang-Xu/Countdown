import streamlit as st

from ui.components.cards import render_event_card


def _build_card_display(event, status_info: dict) -> tuple[str, str, str]:
    if status_info["status"] == "today":
        return "Today", "now", "就在今天"

    days_value = status_info.get("days_value", 0)

    if event.event_type.value == "countup":
        return str(days_value), "days", "已经累计"

    if status_info["status"] == "passed":
        return str(days_value), "days", "已经过去"

    if event.repeat_type.value == "yearly":
        return str(days_value), "days", "距离下一次"

    return str(days_value), "days", "还有"


def render_dashboard_page(event_service):
    events = event_service.list_events_with_status()
    total_events = len(events)
    pinned_count = sum(1 for item in events if item["event"].pinned)

    st.markdown(f"""
    <section class="app-shell content-shell hero">
        <div class="hero-copy">
            <div class="eyebrow">Life in moments</div>
            <div class="app-title">Life Countdown</div>
            <div class="app-subtitle">把重要日子安静地摆放出来。少一点界面噪音，多一点呼吸感，让倒数与纪念本身成为页面的主角。</div>
        </div>
        <aside class="hero-aside">
            <div>
                <div class="hero-aside-label">Moments</div>
                <div class="hero-aside-value">{total_events}</div>
                <div class="hero-aside-meta">个时刻正在被记录，其中 {pinned_count} 个被放在最前面。</div>
            </div>
        </aside>
    </section>
    """, unsafe_allow_html=True)

    if not events:
        st.markdown("""
        <section class="empty-shell">
            <p class="empty-copy">No countdowns yet. Start with a single moment.</p>
            <a class="create-link-button" href="?page=create" target="_self">New Countdown</a>
        </section>
        """, unsafe_allow_html=True)
        return

    st.markdown(f"""
    <div class="section-heading">
        <div>
            <h2 class="section-title">Highlights</h2>
            <p class="section-note">先看到事件本身，再看到它和今天的距离。</p>
        </div>
        <p class="section-note">{total_events} events in view</p>
    </div>
    """, unsafe_allow_html=True)

    column_count = max(1, min(4, total_events))
    columns = st.columns(column_count, gap="medium")

    for index, item in enumerate(events):
        event = item["event"]
        status_info = item["status_info"]
        stat_value, stat_unit, stat_label = _build_card_display(event, status_info)
        meta = event.date
        badge = "Pinned" if event.pinned else event.event_type.value
        tone_class = f"tone-{(index % 6) + 1}"
        with columns[index % column_count]:
            render_event_card(
                event_id=event.id,
                title=event.title,
                stat_value=stat_value,
                stat_unit=stat_unit,
                stat_label=stat_label,
                meta_text=meta,
                badge_text=badge,
                tone_class=tone_class,
            )

    st.markdown("""
    <section class="dashboard-actions">
        <a class="create-link-button" href="?page=create" target="_self">New Countdown</a>
    </section>
    """, unsafe_allow_html=True)
