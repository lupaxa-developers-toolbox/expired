"""Tests for parse_datetime."""

from __future__ import annotations

from datetime import datetime

import pytest

from lupaxa.expired.exceptions import ParseError
from lupaxa.expired.parsing import parse_datetime


def test_passthrough_datetime() -> None:
    value = datetime(2024, 11, 6, 9, 0, 0)
    assert parse_datetime(value) is value


def test_sql_datetime() -> None:
    dt = parse_datetime("2022-10-19 14:43:57.563803")
    assert dt == datetime(2022, 10, 19, 14, 43, 57, 563803)


def test_iso_zulu() -> None:
    dt = parse_datetime("2024-11-06T08:45:00Z")
    assert dt == datetime(2024, 11, 6, 8, 45, 0)


def test_date_only() -> None:
    dt = parse_datetime("2022-10-19")
    assert dt == datetime(2022, 10, 19)


def test_custom_fmt() -> None:
    dt = parse_datetime("2024/11/06 09:00:00", fmt="%Y/%m/%d %H:%M:%S")
    assert dt == datetime(2024, 11, 6, 9, 0, 0)


def test_custom_formats_tuple() -> None:
    formats = ("%Y/%m/%d %H:%M:%S",)
    dt = parse_datetime("2024/11/06 09:00:00", formats=formats)
    assert dt == datetime(2024, 11, 6, 9, 0, 0)
    with pytest.raises(ParseError):
        parse_datetime("2024-11-06 09:00:00", formats=formats)


def test_unparseable_string() -> None:
    with pytest.raises(ParseError):
        parse_datetime("not-a-date")


def test_unsupported_type() -> None:
    with pytest.raises(ParseError):
        parse_datetime(12345)  # type: ignore[arg-type]
