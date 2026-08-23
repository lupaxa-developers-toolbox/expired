"""Tests for make_delta."""

from __future__ import annotations

from datetime import timedelta

from lupaxa.expired.delta import make_delta


def test_hours_and_days() -> None:
    assert make_delta(days=2, hours=3) == timedelta(days=2, hours=3)


def test_year_is_365_days() -> None:
    assert make_delta(years=1) == timedelta(days=365)


def test_month_is_30_days() -> None:
    assert make_delta(months=2) == timedelta(days=60)


def test_weeks() -> None:
    assert make_delta(weeks=1) == timedelta(weeks=1)
