"""Core logic for checking whether a given datetime has expired."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from .delta import make_delta
from .exceptions import ExpiredError
from .parsing import parse_datetime


def is_expired(
    when: str | datetime,
    *,
    delta: timedelta | None = None,
    now: datetime | None = None,
    fmt: str | None = None,
    **delta_kwargs: Any,
) -> bool:
    """Return True if ``when`` is older than ``(now - delta)``.

    With no ``delta`` and no keyword parts, ``delta`` is zero: ``when`` is
    compared to UTC ``now``. Pass ``delta=timedelta(...)`` or parts such as
    ``days=3`` to use a window. ``fmt`` is a parse format, not a delta part.
    """
    dt = parse_datetime(when, fmt=fmt)

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    if now is None:
        now = datetime.now(timezone.utc)
    elif now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)

    if delta is None:
        if delta_kwargs:
            try:
                delta = make_delta(**delta_kwargs)
            except TypeError as exc:
                raise ExpiredError(str(exc)) from exc
        else:
            delta = timedelta(0)

    return dt < (now - delta)
