"""lupaxa.expired — check whether a timestamp has expired relative to UTC now.

``is_expired(when)`` compares ``when`` to the current UTC time. Pass a
``delta`` or parts such as ``days=3`` to use a window instead.
"""

from __future__ import annotations

from .constants import DEFAULT_FORMATS
from .core import is_expired
from .delta import make_delta
from .exceptions import ExpiredError, ParseError
from .parsing import parse_datetime
from .version import __version__, get_version

__all__ = [
    "DEFAULT_FORMATS",
    "ExpiredError",
    "ParseError",
    "__version__",
    "get_version",
    "is_expired",
    "make_delta",
    "parse_datetime",
]
