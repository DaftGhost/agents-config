import json

from recordtool.exporter import export_records

RECORDS = [{"id": 1, "title": "a", "tags": ["x", "y"], "created_at": "2026-03-01T08:12:00Z"}]


def test_export_json(tmp_path):
    out = tmp_path / "r.json"
    export_records(RECORDS, "json", out)
    assert json.loads(out.read_text(encoding="utf-8")) == RECORDS


def test_export_csv_joins_tags(tmp_path):
    out = tmp_path / "r.csv"
    export_records(RECORDS, "csv", out)
    assert "x,y" in out.read_text(encoding="utf-8")
