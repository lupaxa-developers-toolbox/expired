<!-- markdownlint-disable -->
<p align="center">
  <a href="https://github.com/lupaxa-developers-toolbox">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/developers-toolbox/readme-logo.png" alt="Project Logo" width="256"/><br/>
  </a>
</p>
<h3 align="center">
  The Lupaxa Developers Toolbox<br />
  Part of The Lupaxa Project
</h3>

<br />

# lupaxa-expired

Tiny utility to check whether a timestamp has expired relative to UTC now.
A value is expired when it is strictly earlier than `(now - delta)`. With
no window, `delta` is zero: anything before UTC now is expired, and a time
equal to now is not.

Built for scripts and tools used by The Lupaxa Project.

The PyPI name is `lupaxa-expired`. The import path is `lupaxa.expired`.
The CLI is installed as `expired`.

## Features

- Accepts ISO, SQL, and date-only timestamp strings, or a `datetime`
- Optional window via `timedelta` or parts: years, months, weeks, days, hours, minutes, seconds
- Timezone-aware UTC comparison (naive values treated as UTC)
- Library API returns a boolean; equal-to-cutoff is not expired
- CLI with `--version`, stdout `expired` / `not expired`, and shell exit codes
- Fully typed, linted, formatted, and tested
- No runtime dependencies

## Installation

### From PyPI

```bash
pip install lupaxa-expired
```

### From source (development mode)

```bash
pip install -e ".[dev]"
```

Requires Python 3.10+. `lupaxa` is a namespace package — there is no
`lupaxa/__init__.py`.

## Usage

```python
from datetime import datetime, timedelta, timezone
from lupaxa.expired import is_expired

if is_expired("2022-10-19 14:43:57.563803"):
    print("Expired")

cutoff = datetime(2025, 11, 6, 12, 0, 0, tzinfo=timezone.utc)
is_expired("2025-10-01", days=3, now=cutoff)
is_expired(cutoff - timedelta(hours=72), hours=48, now=cutoff)
is_expired("2025/11/01 14:43:57", fmt="%Y/%m/%d %H:%M:%S", days=2, now=cutoff)
```

Built-in string formats include `YYYY-MM-DD`, `YYYY-MM-DD HH:MM:SS[.ffffff]`,
and ISO-8601 with an optional `Z`. Pass `fmt=` for anything else. Years
are 365 days and months are 30 days.

```bash
expired --time "2022-10-19 14:43:57.563803"
expired --time "2022-10-19 14:43:57.563803" --days 3
expired --time "2024-11-06T09:00:00Z" --hours 12
expired --time "2024/11/06 09:00:00" --format "%Y/%m/%d %H:%M:%S" --days 1
expired --version
expired --help
```

The CLI prints `expired` or `not expired`. Exit `0` means not expired
(or `--version`), `1` means expired, and `2` means bad input.

Delta flags: `--years`, `--months`, `--weeks`, `--days`, `--hours`,
`--minutes`, `--seconds`.

## Development

```bash
make init
make python-install-dev
make python-check
make mkdocs-serve
```

Documentation: <https://expired.thelupaxaproject.org/>.

<a href="https://github.com/the-lupaxa-project">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/components/footer-for-child-orgs.svg" alt="The Lupaxa Project Footer" width="100%" />
</a>
