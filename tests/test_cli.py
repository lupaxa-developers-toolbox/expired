"""Tests for the expired CLI."""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timedelta, timezone

import pytest

from lupaxa.expired import __version__
from lupaxa.expired.cli import main


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--version"]) == 0
    assert f"expired {__version__}" in capsys.readouterr().out


def test_expired(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    fixed = datetime(2025, 11, 6, 12, 0, 0, tzinfo=timezone.utc)

    class _FrozenDateTime(datetime):
        @classmethod
        def now(cls, tz: timezone | None = None) -> datetime:
            return fixed if tz is not None else fixed.replace(tzinfo=None)

    monkeypatch.setattr("lupaxa.expired.core.datetime", _FrozenDateTime)
    when = (fixed - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")
    assert main(["--time", when, "--days", "3"]) == 1
    assert capsys.readouterr().out.strip() == "expired"


def test_time_only_compares_to_utc_now(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    fixed = datetime(2025, 11, 6, 12, 0, 0, tzinfo=timezone.utc)

    class _FrozenDateTime(datetime):
        @classmethod
        def now(cls, tz: timezone | None = None) -> datetime:
            return fixed if tz is not None else fixed.replace(tzinfo=None)

    monkeypatch.setattr("lupaxa.expired.core.datetime", _FrozenDateTime)
    when = (fixed - timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")
    assert main(["--time", when]) == 1
    assert capsys.readouterr().out.strip() == "expired"


def test_not_expired(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    fixed = datetime(2025, 11, 6, 12, 0, 0, tzinfo=timezone.utc)

    class _FrozenDateTime(datetime):
        @classmethod
        def now(cls, tz: timezone | None = None) -> datetime:
            return fixed if tz is not None else fixed.replace(tzinfo=None)

    monkeypatch.setattr("lupaxa.expired.core.datetime", _FrozenDateTime)
    when = (fixed - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    assert main(["--time", when, "--days", "3"]) == 0
    assert capsys.readouterr().out.strip() == "not expired"


def test_bad_time(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--time", "not-a-date", "--days", "1"]) == 2
    err = capsys.readouterr().err
    assert "error:" in err


def test_missing_time() -> None:
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code == 2


def test_module_entry_version() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "lupaxa.expired", "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert __version__ in proc.stdout
