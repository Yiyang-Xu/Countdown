import streamlit as st


def render_event_card(title: str, primary_text: str, meta_text: str):
    st.markdown(f"""
    <div class="event-card">
        <div class="event-title">{title}</div>
        <div class="event-main">{primary_text}</div>
        <div class="event-meta">{meta_text}</div>
    </div>
    """, unsafe_allow_html=True)
