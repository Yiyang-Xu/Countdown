from pathlib import Path

APP_TITLE = "Life Countdown"
PAGE_ICON = "⏳"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
EVENTS_FILE = DATA_DIR / "events.json"
