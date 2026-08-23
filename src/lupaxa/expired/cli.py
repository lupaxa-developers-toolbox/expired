"""Command-line interface for lupaxa.expired."""

from __future__ import annotations

import argparse
import sys

from lupaxa.expired import __version__, is_expired, make_delta, parse_datetime


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check if a given timestamp has expired compared to now (UTC)."
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information and exit.",
    )
    parser.add_argument(
        "--time",
        help="Timestamp to check (e.g. '2022-10-19 14:43:57.563803').",
    )
    parser.add_argument(
        "--format",
        help="Optional strptime() format to parse the time.",
    )
    parser.add_argument("--years", type=int, default=0, help="Years to subtract from now.")
    parser.add_argument(
        "--months",
        type=int,
        default=0,
        help="Months to subtract from now (30d each).",
    )
    parser.add_argument("--weeks", type=int, default=0, help="Weeks to subtract from now.")
    parser.add_argument("--days", type=int, default=0, help="Days to subtract from now.")
    parser.add_argument("--hours", type=int, default=0, help="Hours to subtract from now.")
    parser.add_argument("--minutes", type=int, default=0, help="Minutes to subtract from now.")
    parser.add_argument("--seconds", type=int, default=0, help="Seconds to subtract from now.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(f"expired {__version__}")
        return 0

    if not args.time:
        parser.error("--time is required unless --version is used")

    try:
        ts = parse_datetime(args.time, fmt=args.format)
    except Exception as exc:
        print(f"error: failed to parse time: {exc}", file=sys.stderr)
        return 2

    delta = make_delta(
        years=args.years,
        months=args.months,
        weeks=args.weeks,
        days=args.days,
        hours=args.hours,
        minutes=args.minutes,
        seconds=args.seconds,
    )

    if is_expired(ts, delta=delta):
        print("expired")
        return 1

    print("not expired")
    return 0
