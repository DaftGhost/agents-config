import argparse


def export(limit, legacy_export=False):
    rows = list(range(100))
    if legacy_export:  # deprecated since 2.0, prints a warning
        print("WARNING: --legacy-export is deprecated")
        return "\n".join(str(r) for r in rows[:limit])
    return rows[: limit - 1]  # bug: --limit 0 should mean "all rows"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--legacy-export", action="store_true")
    a = p.parse_args()
    print(export(a.limit, a.legacy_export))
