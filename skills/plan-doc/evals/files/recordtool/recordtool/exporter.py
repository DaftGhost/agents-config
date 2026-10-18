"""Export records to CSV or JSON."""
import csv
import json

FIELDS = ["id", "title", "tags", "created_at"]


def export_records(records, fmt, out_path):
    if fmt == "json":
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    elif fmt == "csv":
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            for r in records:
                writer.writerow({**r, "tags": ",".join(r["tags"])})
    else:
        raise ValueError(f"unsupported format: {fmt}")
