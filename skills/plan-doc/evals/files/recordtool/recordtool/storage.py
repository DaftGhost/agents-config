"""JSON file storage. Each record: {"id": int, "title": str, "tags": [str], "created_at": "2026-03-01T08:12:00Z"}"""
import json
from pathlib import Path

DATA_FILE = Path.home() / ".recordtool" / "records.json"


def load_records():
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_records(records):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
