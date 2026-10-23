import csv


def build_report(path):
    with open(path) as f:
        count = sum(1 for _ in csv.DictReader(f))
    with open(path) as f:
        total = sum(float(row["amount"]) for row in csv.DictReader(f))
    return {"count": count, "total": total}
