import argparse

from .models import Item
from .service import Inventory


def build_inventory():
    return Inventory(
        [
            Item("A-1", "Widget", 2),
            Item("A-2", "Gadget", 5),
            Item("A-3", "Gizmo", 0),
            Item("A-4", "Doohickey", 3),
        ]
    )


def build_parser():
    parser = argparse.ArgumentParser(prog="inventory")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.command == "list":
        for item in build_inventory().all():
            print(f"{item.sku}  {item.name}  {item.quantity}")
        return 0
    return 2
