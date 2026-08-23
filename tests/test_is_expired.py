"""Tests for is_expired."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from lupaxa.expired.core import is_expired
from lupaxa.expired.exceptions import ExpiredError

FIXED_NOW = datetime(2025, 11, 6, 12, 0, 0, tzinfo=timezone.utc)


def test_expired_by_days() -> None:
    when = FIXED_NOW - timedelta(days=5)
    assert is_expired(when, days=3, now=FIXED_NOW) is True


def test_not_expired_by_days() -> None:
    when = FIXED_NOW - timedelta(days=1)
    assert is_expired(when, days=3, now=FIXED_NOW) is False


def test_explicit_delta() -> None:
    when = FIXED_NOW - timedelta(hours=10)
    assert is_expired(when, delta=timedelta(hours=4), now=FIXED_NOW) is True


def test_no_delta_past_is_expired() -> None:
    when = FIXED_NOW - timedelta(seconds=1)
    assert is_expired(when, now=FIXED_NOW) is True


def test_no_delta_future_is_not_expired() -> None:
    when = FIXED_NOW + timedelta(seconds=1)
    assert is_expired(when, now=FIXED_NOW) is False


def test_no_delta_equal_now_is_not_expired() -> None:
    assert is_expired(FIXED_NOW, now=FIXED_NOW) is False


def test_no_delta_string_compares_to_now() -> None:
    assert is_expired("2025-11-01 12:00:00", now=FIXED_NOW) is True


def test_unknown_delta_part_raises() -> None:
    with pytest.raises(ExpiredError):
        is_expired(FIXED_NOW, dayz=3, now=FIXED_NOW)


def test_naive_datetime_treated_as_utc() -> None:
    when = datetime(2025, 11, 1, 12, 0, 0)
    now = datetime(2025, 11, 6, 12, 0, 0)
    assert is_expired(when, days=3, now=now) is True


def test_fmt_is_passed_to_parser() -> None:
    ts = "2025/11/01 14:43:57"
    fmt = "%Y/%m/%d %H:%M:%S"
    assert is_expired(ts, fmt=fmt, days=2, now=FIXED_NOW) is True


def test_fmt_is_not_a_delta_kwarg() -> None:
    ts = "2025/11/05 14:43:57"
    fmt = "%Y/%m/%d %H:%M:%S"
    assert is_expired(ts, fmt=fmt, days=2, now=FIXED_NOW) is False
