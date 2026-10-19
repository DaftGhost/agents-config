import argparse
import sys

from .rates import convert


def build_parser():
    parser = argparse.ArgumentParser(prog="ratecli")
    subparsers = parser.add_subparsers(dest="command", required=True)
    convert_parser = subparsers.add_parser("convert")
    convert_parser.add_argument("amount", type=float)
    convert_parser.add_argument("source")
    convert_parser.add_argument("target")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.command == "convert":
        try:
            result = convert(args.amount, args.source.upper(), args.target.upper())
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        print(f"{args.amount:.2f} {args.source.upper()} = {result:.2f} {args.target.upper()}")
        return 0
    return 2
