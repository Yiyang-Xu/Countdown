import json
from pathlib import Path
from typing import List

from config.settings import EVENTS_FILE
from core.models import Event


class EventRepository:
    def __init__(self, file_path: Path = EVENTS_FILE):
        self.file_path = file_path
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def get_all_events(self) -> List[Event]:
        raw = json.loads(self.file_path.read_text(encoding="utf-8"))
        return [Event.from_dict(item) for item in raw]

    def save_all_events(self, events: List[Event]) -> None:
        payload = [event.to_dict() for event in events]
        self.file_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
