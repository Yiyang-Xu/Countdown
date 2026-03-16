import html
import json
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components

from core.calendar_utils import format_event_date_summary


def _format_datetime(value: str) -> str:
    return datetime.fromisoformat(value).strftime("%Y-%m-%d %H:%M:%S")


def render_detail_page(event_service, event_id: str):
    payload = event_service.get_event_with_status(event_id)

    if not payload:
        st.error("This event could not be found.")
        st.markdown('<a class="detail-back-link" href="?page=dashboard">Back to dashboard</a>', unsafe_allow_html=True)
        return

    event = payload["event"]
    status_info = payload["status_info"]

    quote = event.quote or "时间并不喧哗，它只是安静地靠近。"
    note = event.description or ""
    target_text = _format_datetime(status_info["target_datetime"])
    repeat_label = "yearly" if event.repeat_type.value == "yearly" else "once"
    detail_caption = "正在靠近" if status_info["detail_mode"] == "countdown" else "已经走过"

    title_text = html.escape(event.title)
    quote_text = html.escape(quote)
    note_text = html.escape(note)
    date_text = format_event_date_summary(
        event.date_type,
        event.date,
        event.lunar_month,
        event.lunar_day,
        event.lunar_is_leap_month,
    )
    target_meta = html.escape(
        f"{date_text} · 下次发生 {target_text} · {status_info['timezone']} · {event.event_type.value} · {repeat_label}"
    )

    st.markdown(f"""
    <div class="detail-page-chrome">
        <a class="detail-page-back" href="?page=dashboard" target="_self" aria-label="Back to dashboard">←</a>
        <a class="detail-edit-link" href="?page=edit&event_id={event.id}" target="_self">Edit</a>
    </div>
    """, unsafe_allow_html=True)

    components.html(
        f"""
        <!doctype html>
        <html lang="en">
        <head>
          <meta charset="utf-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <style>
            :root {{
              color-scheme: dark;
              --bg: #17161b;
              --surface: #111015;
              --text: #f8f4ee;
              --muted: rgba(248, 244, 238, 0.62);
              --soft: rgba(248, 244, 238, 0.12);
              --line: rgba(248, 244, 238, 0.18);
            }}

            * {{
              box-sizing: border-box;
            }}

            html, body {{
              margin: 0;
              min-height: 100%;
              background: transparent;
              font-family: "Manrope", "Noto Sans SC", sans-serif;
            }}

            body {{
              padding: 0;
            }}

            .detail-page {{
              min-height: 780px;
              border-radius: 34px;
              background: var(--surface);
              color: var(--text);
              padding: 30px 34px;
              display: flex;
              flex-direction: column;
              justify-content: space-between;
            }}

            .detail-back {{
              display: inline-flex;
              align-items: center;
              width: fit-content;
              color: var(--muted);
              text-decoration: none;
              font-size: 13px;
              letter-spacing: 0.12em;
              text-transform: uppercase;
            }}

            .detail-stage {{
              flex: 1;
              display: flex;
              flex-direction: column;
              justify-content: center;
              align-items: center;
              text-align: center;
              padding: 28px 12px 10px;
            }}

            .detail-kicker {{
              font-size: 12px;
              letter-spacing: 0.18em;
              text-transform: uppercase;
              color: var(--muted);
              margin-bottom: 20px;
            }}

            .detail-timer {{
              display: grid;
              grid-template-columns: repeat(7, auto);
              align-items: center;
              gap: 16px;
              margin-bottom: 34px;
            }}

            .detail-time-block {{
              min-width: 118px;
            }}

            .detail-time-value {{
              font-size: clamp(60px, 7vw, 110px);
              line-height: 0.92;
              letter-spacing: -0.08em;
              font-weight: 800;
              color: var(--text);
              font-variant-numeric: tabular-nums;
            }}

            .detail-time-label {{
              margin-top: 12px;
              font-size: 15px;
              letter-spacing: 0.04em;
              color: var(--muted);
            }}

            .detail-divider {{
              width: 1px;
              height: 72px;
              background: var(--line);
            }}

            .detail-title {{
              font-size: clamp(28px, 2.4vw, 42px);
              line-height: 1.16;
              letter-spacing: -0.04em;
              font-weight: 700;
              margin-bottom: 18px;
            }}

            .detail-quote {{
              max-width: 760px;
              font-size: 18px;
              line-height: 1.9;
              color: var(--muted);
              margin-bottom: 18px;
            }}

            .detail-meta {{
              font-size: 14px;
              line-height: 1.7;
              color: rgba(248, 244, 238, 0.48);
            }}

            .detail-note {{
              max-width: 560px;
              margin: 20px auto 0;
              font-size: 15px;
              line-height: 1.85;
              color: rgba(248, 244, 238, 0.56);
            }}

            @media (max-width: 980px) {{
              .detail-page {{
                min-height: 700px;
                padding: 24px 22px;
                border-radius: 26px;
              }}

              .detail-timer {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 18px 10px;
              }}

              .detail-divider {{
                display: none;
              }}

              .detail-time-block {{
                min-width: 0;
              }}
            }}
          </style>
        </head>
        <body>
          <section class="detail-page">
            <div class="detail-stage">
              <div class="detail-kicker">{html.escape(detail_caption)}</div>
              <div class="detail-timer">
                <div class="detail-time-block">
                  <div id="days" class="detail-time-value">0</div>
                  <div class="detail-time-label">Days</div>
                </div>
                <div class="detail-divider"></div>
                <div class="detail-time-block">
                  <div id="hours" class="detail-time-value">00</div>
                  <div class="detail-time-label">Hours</div>
                </div>
                <div class="detail-divider"></div>
                <div class="detail-time-block">
                  <div id="minutes" class="detail-time-value">00</div>
                  <div class="detail-time-label">Minutes</div>
                </div>
                <div class="detail-divider"></div>
                <div class="detail-time-block">
                  <div id="seconds" class="detail-time-value">00</div>
                  <div class="detail-time-label">Seconds</div>
                </div>
              </div>
              <div class="detail-title">{title_text}</div>
              <div class="detail-quote">“{quote_text}”</div>
              <div class="detail-meta">{target_meta}</div>
              {"<div class='detail-note'>" + note_text + "</div>" if note_text else ""}
            </div>
          </section>
          <script>
            const target = new Date({json.dumps(status_info["target_datetime"])}).getTime();
            const mode = {json.dumps(status_info["detail_mode"])};

            function splitTime(totalSeconds) {{
              const safe = Math.max(0, Math.floor(Math.abs(totalSeconds)));
              const days = Math.floor(safe / 86400);
              const hours = Math.floor((safe % 86400) / 3600);
              const minutes = Math.floor((safe % 3600) / 60);
              const seconds = safe % 60;
              return {{ days, hours, minutes, seconds }};
            }}

            function pad(value) {{
              return String(value).padStart(2, "0");
            }}

            function updateClock() {{
              const now = Date.now();
              const diffSeconds = mode === "countup"
                ? (now - target) / 1000
                : (target - now) / 1000;
              const parts = splitTime(diffSeconds);
              document.getElementById("days").textContent = String(parts.days);
              document.getElementById("hours").textContent = pad(parts.hours);
              document.getElementById("minutes").textContent = pad(parts.minutes);
              document.getElementById("seconds").textContent = pad(parts.seconds);
            }}

            updateClock();
            window.setInterval(updateClock, 1000);
          </script>
        </body>
        </html>
        """,
        height=790,
        scrolling=False,
    )
