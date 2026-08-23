"""Helpers to construct timedelta objects from flexible parts."""

from __future__ import annotations

from datetime import timedelta


def make_delta(
    *,
    years: int = 0,
    months: int = 0,
    weeks: int = 0,
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
) -> timedelta:
    """Create a timedelta from keyword parts.

    ``timedelta`` has no year or month fields, so this approximates
    ``1 year = 365 days`` and ``1 month = 30 days``.
    """
    total_days = days + (years * 365) + (months * 30)
    return timedelta(
        days=total_days,
        weeks=weeks,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
    )
