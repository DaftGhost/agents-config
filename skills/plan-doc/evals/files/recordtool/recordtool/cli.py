import argparse
import sys
from datetime import datetime, timezone

from recordtool import exporter, storage


def cmd_add(args):
    records = storage.load_records()
    new_id = max((r["id"] for r in records), default=0) + 1
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    records.append({"id": new_id, "title": args.title, "tags": args.tag or [], "created_at": now})
    storage.save_records(records)


def cmd_list(args):
    for r in storage.load_records():
        print(r["id"], r["created_at"], r["title"])


def cmd_export(args):
    exporter.export_records(storage.load_records(), args.format, args.out)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="recordtool")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("title")
    p_add.add_argument("--tag", action="append")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list")
    p_list.set_defaults(func=cmd_list)

    p_export = sub.add_parser("export")
    p_export.add_argument("--format", choices=["csv", "json"], default="csv")
    p_export.add_argument("--out", required=True)
    p_export.set_defaults(func=cmd_export)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
