import streamlit as st


def inject_global_styles():
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    .app-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.3rem;
    }

    .app-subtitle {
        font-size: 1rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
    }

    .event-card {
        background: white;
        border-radius: 20px;
        padding: 1.2rem 1.2rem;
        box-shadow: 0 6px 24px rgba(15, 23, 42, 0.08);
        margin-bottom: 1rem;
        border: 1px solid rgba(226, 232, 240, 0.8);
    }

    .event-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: #111827;
    }

    .event-main {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2563eb;
        margin-top: 0.3rem;
        margin-bottom: 0.3rem;
    }

    .event-meta {
        font-size: 0.92rem;
        color: #6b7280;
    }
    </style>
    """, unsafe_allow_html=True)
