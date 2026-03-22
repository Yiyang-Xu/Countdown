import streamlit as st


def inject_global_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;600;700;800&display=swap');

    :root {
        color-scheme: light dark;
        --font-sans: "Manrope", "Noto Sans SC", sans-serif;
        --bg: #f2efea;
        --surface: #fbf8f3;
        --surface-soft: #f6f1ea;
        --surface-muted: #ece5dc;
        --border: rgba(86, 68, 54, 0.14);
        --text: #2d251f;
        --text-muted: #7a6b60;
        --heading: #201914;
        --accent: #b67a52;
        --accent-soft: #efe4d9;
        --shadow: 0 18px 48px rgba(56, 41, 31, 0.08);
        --card-shadow: 0 10px 30px rgba(56, 41, 31, 0.06);
        --card-1-bg: #f6efe7;
        --card-1-accent: #8f6a51;
        --card-2-bg: #efe7df;
        --card-2-accent: #7d6a58;
        --card-3-bg: #f3eadf;
        --card-3-accent: #94775d;
        --card-4-bg: #ece4dc;
        --card-4-accent: #7b6254;
        --card-5-bg: #f5eee5;
        --card-5-accent: #8b715d;
        --card-6-bg: #efe8e0;
        --card-6-accent: #756255;
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --bg: #1e1d21;
            --surface: #252429;
            --surface-soft: #2b2a30;
            --surface-muted: #323139;
            --border: rgba(255, 240, 230, 0.08);
            --text: #f4eee7;
            --text-muted: #b6aba1;
            --heading: #fcf7f2;
            --accent: #d8a27f;
            --accent-soft: #302923;
            --shadow: 0 20px 54px rgba(0, 0, 0, 0.22);
            --card-shadow: 0 12px 30px rgba(0, 0, 0, 0.18);
            --card-1-bg: #2c2b31;
            --card-1-accent: #d6b39a;
            --card-2-bg: #302e35;
            --card-2-accent: #d6c0ac;
            --card-3-bg: #2b2a30;
            --card-3-accent: #d8a27f;
            --card-4-bg: #313037;
            --card-4-accent: #cab1a0;
            --card-5-bg: #2e2c33;
            --card-5-accent: #d3b59b;
            --card-6-bg: #29282e;
            --card-6-accent: #cdb09c;
        }
    }

    html, body, [class*="css"] {
        font-family: var(--font-sans);
    }

    body {
        color: var(--text);
    }

    .main {
        background: var(--bg);
    }

    .block-container {
        padding-top: 3.25rem;
        padding-bottom: 3rem;
        max-width: 1240px;
    }

    [data-testid="stAppViewContainer"] {
        background: transparent;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"],
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }

    .app-shell {
        border-radius: 34px;
        padding: 2.2rem 2.4rem;
        background: var(--surface);
        box-shadow: var(--shadow);
    }

    .content-shell {
        margin-bottom: 1.4rem;
    }

    .hero {
        display: grid;
        grid-template-columns: minmax(0, 1fr) 220px;
        gap: 2rem;
        align-items: end;
        margin-bottom: 1.8rem;
    }

    .hero-copy {
        max-width: 44rem;
    }

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.25rem 0;
        border-radius: 999px;
        color: var(--accent);
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
    }

    .app-title {
        font-size: clamp(3rem, 4.4vw, 4.6rem);
        line-height: 0.95;
        letter-spacing: -0.02em;
        font-weight: 800;
        color: var(--heading);
        margin-bottom: 0.8rem;
        max-width: 8ch;
    }

    .app-subtitle {
        font-size: 0.98rem;
        line-height: 1.8;
        color: var(--text-muted);
        margin-bottom: 0;
        max-width: 34rem;
    }

    .hero-aside {
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 220px;
        border-radius: 28px;
        padding: 1.3rem;
        background: var(--surface-soft);
        border: 1px solid var(--border);
    }

    .hero-aside-label {
        color: var(--text-muted);
        font-size: 0.78rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        font-weight: 700;
        text-align: center;
    }

    .hero-aside-value {
        margin-top: 0.85rem;
        color: var(--accent);
        font-size: clamp(2.6rem, 3vw, 3.4rem);
        line-height: 1;
        letter-spacing: -0.04em;
        font-weight: 800;
        text-align: center;
    }

    .hero-aside-meta {
        margin-top: 0.9rem;
        color: var(--text-muted);
        font-size: 0.92rem;
        line-height: 1.8;
        text-align: center;
    }

    .section-heading {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .section-title {
        font-size: 1.85rem;
        line-height: 1.1;
        letter-spacing: 0em;
        font-weight: 800;
        color: var(--heading);
        margin: 0;
    }

    .section-note {
        margin: 0;
        color: var(--text-muted);
        font-size: 0.95rem;
    }

    .dashboard-actions,
    .empty-shell {
        display: flex;
        justify-content: center;
        margin-top: 1.6rem;
    }

    .empty-shell {
        flex-direction: column;
        align-items: center;
        gap: 0.9rem;
        min-height: 18rem;
        border-radius: 28px;
        background: var(--surface);
        box-shadow: var(--card-shadow);
    }

    .empty-copy {
        margin: 0;
        color: var(--text-muted);
        font-size: 1rem;
    }

    .create-link-button,
    .create-link-button:link,
    .create-link-button:visited,
    .create-link-button:hover,
    .create-link-button:active {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 10rem;
        height: 3rem;
        padding: 0 1.2rem;
        border-radius: 999px;
        background: var(--heading);
        color: var(--surface) !important;
        text-decoration: none !important;
        font-weight: 700;
        letter-spacing: 0.01em;
    }

    .event-card {
        background: var(--card-bg, var(--surface-soft));
        border-radius: 26px;
        padding: 1.15rem 1rem 1.05rem;
        box-shadow: var(--card-shadow);
        border: 1px solid color-mix(in srgb, var(--card-accent, var(--border)) 16%, transparent);
        margin-bottom: 1rem;
        min-height: 228px;
        display: grid;
        grid-template-rows: auto auto 1fr auto auto;
        align-items: start;
    }

    .event-card-link {
        display: block;
        text-decoration: none !important;
        color: inherit !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }

    .event-card-link:hover .event-card {
        transform: translateY(-2px);
    }

    .event-card-link:link,
    .event-card-link:visited,
    .event-card-link:hover,
    .event-card-link:active {
        text-decoration: none !important;
        color: inherit !important;
    }

    .event-card-link .event-card {
        transition: transform 180ms ease;
    }

    .tone-1 { --card-bg: var(--card-1-bg); --card-accent: var(--card-1-accent); }
    .tone-2 { --card-bg: var(--card-2-bg); --card-accent: var(--card-2-accent); }
    .tone-3 { --card-bg: var(--card-3-bg); --card-accent: var(--card-3-accent); }
    .tone-4 { --card-bg: var(--card-4-bg); --card-accent: var(--card-4-accent); }
    .tone-5 { --card-bg: var(--card-5-bg); --card-accent: var(--card-5-accent); }
    .tone-6 { --card-bg: var(--card-6-bg); --card-accent: var(--card-6-accent); }

    .event-card-topline {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.35rem 0.8rem;
        border-radius: 999px;
        background: color-mix(in srgb, var(--card-accent) 14%, transparent);
        color: var(--card-accent);
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin: 0 auto 0.8rem;
    }

    .event-main-block {
        text-align: center;
        margin-top: 0.15rem;
    }

    .event-main {
        font-size: clamp(2rem, 2.4vw, 2.5rem);
        line-height: 1.02;
        letter-spacing: -0.06em;
        font-weight: 800;
        color: var(--heading);
        margin-top: 0;
        margin-bottom: 0;
    }

    .event-unit {
        margin-top: 0.18rem;
        color: var(--card-accent);
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        text-align: center;
    }

    .event-label {
        margin-top: 0.6rem;
        color: var(--text-muted);
        font-size: 0.88rem;
        line-height: 1.5;
        text-align: center;
    }

    .event-title {
        font-size: 1.2rem;
        line-height: 1.35;
        letter-spacing: -0.03em;
        font-weight: 700;
        color: var(--heading);
        text-align: center;
        align-self: end;
        margin-top: 1rem;
    }

    .event-meta {
        font-size: 0.82rem;
        color: var(--text-muted);
        line-height: 1.7;
        text-align: center;
        margin-top: 0.4rem;
    }

    .event-meta strong {
        display: block;
        margin-bottom: 0.2rem;
        color: var(--card-accent);
        font-weight: 700;
    }

    .page-header {
        margin-bottom: 1.3rem;
    }

    .page-title {
        margin: 0 0 0.5rem;
        font-size: clamp(2.2rem, 3.2vw, 3rem);
        line-height: 1;
        letter-spacing: -0.05em;
        font-weight: 800;
        color: var(--heading);
    }

    .page-subtitle {
        margin: 0;
        max-width: 38rem;
        color: var(--text-muted);
        line-height: 1.7;
    }

    .panel {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 28px;
        padding: 1.4rem;
        box-shadow: var(--card-shadow);
        height: auto;
        margin-bottom: 1rem;
    }

    .panel-title {
        margin: 0 0 0.45rem;
        font-size: 1.2rem;
        letter-spacing: -0.03em;
        font-weight: 800;
        color: var(--heading);
    }

    .panel-copy {
        margin: 0;
        color: var(--text-muted);
        font-size: 0.95rem;
        line-height: 1.65;
    }

    .event-list-item {
        padding: 1rem 0;
        border-bottom: 1px solid var(--border);
    }

    .event-list-item:last-child {
        border-bottom: none;
        padding-bottom: 0;
    }

    .event-list-title {
        margin: 0;
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--heading);
    }

    .event-inline-link {
        color: inherit !important;
        text-decoration: none !important;
        border-bottom: 1px solid transparent;
    }

    .event-inline-link:hover {
        border-bottom-color: currentColor;
    }

    .detail-back-link,
    .detail-back-link:link,
    .detail-back-link:visited,
    .detail-back-link:hover,
    .detail-back-link:active {
        color: var(--accent) !important;
        text-decoration: none !important;
    }

    .detail-page-back,
    .detail-page-back:link,
    .detail-page-back:visited,
    .detail-page-back:hover,
    .detail-page-back:active {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 2rem;
        height: 2rem;
        margin-bottom: 0.9rem;
        color: rgba(248, 244, 238, 0.72) !important;
        text-decoration: none !important;
        font-size: 1.35rem;
        line-height: 1;
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        transition: color 160ms ease, transform 160ms ease;
    }

    .detail-page-back:hover {
        color: rgba(248, 244, 238, 0.96) !important;
        transform: translateX(-2px);
    }

    .detail-page-chrome {
        width: min(72rem, 100%);
        margin: 0 auto 0.8rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .detail-edit-link,
    .detail-edit-link:link,
    .detail-edit-link:visited,
    .detail-edit-link:hover,
    .detail-edit-link:active {
        color: rgba(248, 244, 238, 0.66) !important;
        text-decoration: none !important;
        font-size: 0.92rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        transition: color 160ms ease;
    }

    .detail-edit-link:hover {
        color: rgba(248, 244, 238, 0.92) !important;
    }

    .create-shell {
        max-width: 48rem;
        margin: 0 auto 1.2rem;
    }

    .create-eyebrow {
        color: var(--accent);
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    .create-title {
        margin: 0 0 0.9rem;
        font-size: clamp(2.8rem, 4.8vw, 4.6rem);
        line-height: 0.95;
        letter-spacing: -0.06em;
        color: var(--heading);
    }

    .create-subtitle {
        margin: 0;
        max-width: 42rem;
        color: var(--text-muted);
        font-size: 1rem;
        line-height: 1.8;
    }

    .field-label {
        margin: 0.1rem 0 0.48rem;
        color: rgba(248, 244, 238, 0.78);
        font-size: 1.5 rem;
        font-weight: 700;
        letter-spacing: -0.01em;
        text-transform: none;
    }

    .field-hint {
        margin-top: 0.6rem;
        margin-bottom: 0.1rem;
        color: var(--text-muted);
        font-size: 0.88rem;
        line-height: 1.6;
    }

    .submit-wrap {
        display: flex;
        justify-content: center;
    }

    .color-placeholder {
        display: flex;
        align-items: center;
        min-height: 3.4rem;
        padding: 0 1rem;
        border-radius: 18px;
        background: var(--surface-soft);
        border: 1px dashed var(--border);
        color: var(--text-muted);
        font-size: 0.92rem;
    }

    .event-list-meta, .event-list-description {
        margin: 0.45rem 0 0;
        color: var(--text-muted);
        line-height: 1.65;
    }

    .stFormSubmitButton {
        display: flex;
        justify-content: center;
        margin-top: 1.7rem;
    }

    .stFormSubmitButton > button {
        min-width: 12rem;
        border-radius: 999px;
        border: 1px solid transparent;
        background: var(--accent);
        color: #fff9f4;
        font-weight: 700;
        padding: 0.62rem 1.1rem;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        border-color: transparent;
        color: #fffdf8;
    }

    .stTextInput input,
    .stDateInput input,
    .stTextArea textarea,
    .stSelectbox [data-baseweb="select"] > div {
        border-radius: 18px;
        background: var(--surface-soft);
        border-color: var(--border);
    }

    .stCheckbox label,
    .stSelectbox label,
    .stDateInput label,
    .stTextInput label,
    .stTextArea label {
        color: var(--text);
        font-weight: 600;
    }

    [data-testid="stVerticalBlock"]:has(.create-form-marker) {
        width: min(48rem, 100%);
        margin: 0 auto;
    }

    [data-testid="stVerticalBlock"]:has(.create-form-marker) > [data-testid="stVerticalBlockBorderWrapper"] {
        padding: 1.7rem 1.7rem 1.8rem;
        border-radius: 32px;
        border: 1px solid color-mix(in srgb, var(--border) 88%, transparent);
        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.025), rgba(255, 255, 255, 0)),
            var(--surface-soft);
        box-shadow: 0 18px 42px rgba(0, 0, 0, 0.12);
    }

    .form-section-heading {
        margin: 0rem 0 1rem;
    }

    .form-section-kicker {
        color: var(--accent);
        font-size: 1.2rem;
        font-weight: 800;
        letter-spacing: 0.05rem;
        text-transform: uppercase;
        margin-bottom: 0.1rem;
    }

    .form-section-title {
        color: rgba(248, 244, 238, 0.94);
        font-size: 1.2rem;
        font-weight: 700;
        line-height: 1.35;
        letter-spacing: 0rem;
    }

    [data-testid="stVerticalBlock"]:has(.create-form-marker) .form-section-heading:not(:first-of-type) {
        margin-top: 1.55rem;
    }

    [data-testid="stVerticalBlock"]:has(.create-form-marker) .field-label {
        margin: 0.08rem 0 0.42rem;
    }

    [data-testid="stVerticalBlock"]:has(.create-form-marker) .stTextInput,
    [data-testid="stVerticalBlock"]:has(.create-form-marker) .stDateInput,
    [data-testid="stVerticalBlock"]:has(.create-form-marker) .stNumberInput,
    [data-testid="stVerticalBlock"]:has(.create-form-marker) .stSelectbox {
        margin-bottom: 0;
    }

    [data-testid="stVerticalBlock"]:has(.create-form-marker) .stTextInput [data-baseweb="base-input"],
    [data-testid="stVerticalBlock"]:has(.create-form-marker) .stDateInput [data-baseweb="base-input"],
    [data-testid="stVerticalBlock"]:has(.create-form-marker) .stNumberInput [data-baseweb="input"] > div,
    [data-testid="stVerticalBlock"]:has(.create-form-marker) .stSelectbox [data-baseweb="select"] > div {
        min-height: 3rem;
        padding: 0 1rem;
        display: flex;
        align-items: center;
        box-sizing: border-box;
    }

    [data-testid="stVerticalBlock"]:has(.create-form-marker) .stTextInput input,
    [data-testid="stVerticalBlock"]:has(.create-form-marker) .stDateInput input,
    [data-testid="stVerticalBlock"]:has(.create-form-marker) .stNumberInput input {
        width: 100%;
        height: auto;
        min-height: 0;
        margin: 0;
        padding: 0;
        border: none;
        background: transparent;
        font-size: 1.08rem;
        line-height: 1.2;
        text-align: center;
        align-self: center;
        box-sizing: border-box;
    }

    [data-testid="stVerticalBlock"]:has(.create-form-marker) .stTextInput input::placeholder,
    [data-testid="stVerticalBlock"]:has(.create-form-marker) .stDateInput input::placeholder {
        font-size: 1.08rem;
        line-height: 1.2;
        text-align: center;
    }

    [data-testid="stVerticalBlock"]:has(.create-form-marker) .stSelectbox [data-baseweb="select"] > div > div:first-child {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 0;
    }

    [data-testid="stVerticalBlock"]:has(.create-form-marker) .stSelectbox [data-baseweb="select"] span {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        min-height: 0;
        font-size: 1.08rem;
        line-height: 1.2;
        text-align: center;
    }

    [data-testid="stVerticalBlock"]:has(.create-form-marker) [data-testid="stCaptionContainer"] {
        margin-top: -0.08rem;
        margin-bottom: 0.8rem;
        color: rgba(248, 244, 238, 0.54);
        font-size: 0.84rem;
        line-height: 1.55;
        text-align: center;
    }

    [data-testid="stVerticalBlock"]:has(.create-form-marker) .color-placeholder {
        min-height: 3.2rem;
        padding: 0 1.05rem;
        border-radius: 20px;
    }

    [data-testid="stVerticalBlock"]:has(.create-form-marker) .stButton {
        display: flex;
        justify-content: center;
        margin-top: 1.35rem;
    }

    [data-testid="stVerticalBlock"]:has(.create-form-marker) .stButton > button {
        min-width: 12rem;
        border-radius: 999px;
        border: 1px solid transparent;
        background: var(--accent);
        color: #fff9f4;
        font-weight: 700;
        padding: 0.62rem 1.1rem;
    }

    [data-testid="stForm"] {
        width: min(44rem, 100%);
        margin: 0 auto;
        display: block;
        background: transparent;
        border: none;
        border-radius: 0;
        padding: 0;
        box-shadow: none;
    }

    .stTextInput,
    .stDateInput,
    .stSelectbox {
        width: 100%;
    }

    .stTextInput > div,
    .stDateInput > div,
    .stSelectbox > div {
        width: 100%;
    }

    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 24px;
        border-color: var(--border);
        background: var(--surface-soft);
    }

    @media (max-width: 980px) {
        .block-container {
            padding-top: 1.4rem;
            padding-bottom: 1.8rem;
        }

        .app-shell {
            border-radius: 24px;
            padding: 1.4rem;
        }

        .hero {
            grid-template-columns: 1fr;
        }

        .hero-aside {
            min-height: auto;
        }

        .section-heading {
            flex-direction: column;
            align-items: flex-start;
        }

    }

    @media (max-width: 640px) {
        .event-card {
            border-radius: 22px;
            padding: 1.1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
