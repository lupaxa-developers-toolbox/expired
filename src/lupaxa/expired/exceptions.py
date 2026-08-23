"""Custom exceptions for the expired package."""


class ExpiredError(Exception):
    """Base error for the expired package."""


class ParseError(ExpiredError):
    """Raised when a datetime string cannot be parsed."""
