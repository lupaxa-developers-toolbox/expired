"""Helpers for turning strings into datetime objects."""

from __future__ import annotations

from datetime import datetime

from .constants import DEFAULT_FORMATS
from .exceptions import ParseError


def parse_datetime(
    value: str | datetime,
    *,
    fmt: str | None = None,
    formats: tuple[str, ...] | None = None,
) -> datetime:
    """Convert a string or datetime into a datetime.

    If ``value`` is already a datetime, it is returned as-is. If ``fmt`` is
    provided, that single ``strptime`` format is used. Otherwise the default
    format list is tried in order.
    """
    if isinstance(value, datetime):
        return value

    if not isinstance(value, str):
        raise ParseError(f"Unsupported datetime value type: {type(value)!r}")

    if fmt:
        try:
            return datetime.strptime(value, fmt)
        except ValueError as exc:
            raise ParseError(f"Unable to parse datetime {value!r} with format {fmt!r}") from exc

    last_error: Exception | None = None
    for candidate in formats or DEFAULT_FORMATS:
        try:
            return datetime.strptime(value, candidate)
        except ValueError as exc:
            last_error = exc

    raise ParseError(f"Unable to parse datetime string {value!r}") from last_error
