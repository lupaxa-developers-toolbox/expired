<p align="center">
  <a href="https://github.com/lupaxa-developers-toolbox">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/developers-toolbox/readme-logo.png" alt="Developers Toolbox" />
  </a>
</p>

<h1 align="center">Expired</h1>

Tiny utility to check whether a timestamp has expired relative to the
current UTC time. A value is expired when it is strictly earlier than
`(now - delta)`. With no window, `delta` is zero, so anything before
UTC now is expired and a time equal to now is not.

The PyPI name is `lupaxa-expired`. The import path is `lupaxa.expired`.
The console script is `expired`. `lupaxa` is a namespace package — there
is no `lupaxa/__init__.py`.

Public names: `is_expired`, `parse_datetime`, `make_delta`,
`ExpiredError`, `ParseError`, `DEFAULT_FORMATS`, `__version__`,
`get_version()`.

## Install

```bash
pip install lupaxa-expired
```

Requires Python 3.10+. No runtime dependencies.

## Library

```python
from datetime import datetime, timezone
from lupaxa.expired import is_expired

if is_expired("2022-10-19 14:43:57.563803"):
    print("Expired")

cutoff = datetime(2025, 11, 6, tzinfo=timezone.utc)
is_expired("2025-10-01", days=3, now=cutoff)
is_expired(cutoff, now=cutoff)  # False — equal is not expired
```

| Situation                         | Result           |
| --------------------------------- | ---------------- |
| `when` is earlier than the cutoff | expired (`True`) |
| `when` equals the cutoff          | not expired      |
| `when` is later than the cutoff   | not expired      |

`now` defaults to current UTC. `delta` defaults to zero. Naive datetimes
are treated as UTC.

Pass a `timedelta` or keyword parts (`years`, `months`, `weeks`, `days`,
`hours`, `minutes`, `seconds`). Parts add together and are ignored when
`delta=` is set. `fmt` is a parse format, not a delta part. Years are
365 days and months are 30 days. An unknown part raises `ExpiredError`.

```python
from lupaxa.expired import ExpiredError, ParseError, is_expired, make_delta, parse_datetime

is_expired("2025/11/01 14:43:57", fmt="%Y/%m/%d %H:%M:%S", days=2)
parse_datetime("2024-11-06T08:45:00Z")
make_delta(weeks=2, days=3)
```

Without `fmt`, strings are tried in this order:

| Format                       | Example                       |
| ---------------------------- | ----------------------------- |
| `%Y-%m-%d %H:%M:%S.%f`       | `2022-10-19 14:43:57.563803`  |
| `%Y-%m-%d %H:%M:%S`          | `2022-10-19 14:43:57`         |
| `%Y-%m-%d`                   | `2022-10-19`                  |
| `%Y-%m-%dT%H:%M:%S.%fZ`      | `2024-11-06T08:45:00.123456Z` |
| `%Y-%m-%dT%H:%M:%S.%f`       | `2024-11-06T08:45:00.123456`  |
| `%Y-%m-%dT%H:%M:%SZ`         | `2024-11-06T08:45:00Z`        |
| `%Y-%m-%dT%H:%M:%S`          | `2024-11-06T08:45:00`         |

The `Z` is a literal suffix, not a timezone conversion. Unparseable
input raises `ParseError` (a subclass of `ExpiredError`).

## CLI

```bash
expired --time "2022-10-19 14:43:57.563803"
expired --time "2022-10-19 14:43:57.563803" --days 3
expired --time "2024-11-06T09:00:00Z" --hours 12
expired --time "2024/11/06 09:00:00" --format "%Y/%m/%d %H:%M:%S" --days 1
expired --version
```

`--time` is required unless you pass `--version`.

| Flag        | Meaning                                      |
| ----------- | -------------------------------------------- |
| `--time`    | Timestamp to check (required unless version) |
| `--format`  | Optional `strptime` format for `--time`      |
| `--years`   | Years to subtract from now (365 days each)   |
| `--months`  | Months to subtract from now (30 days each)   |
| `--weeks`   | Weeks to subtract from now                   |
| `--days`    | Days to subtract from now                    |
| `--hours`   | Hours to subtract from now                   |
| `--minutes` | Minutes to subtract from now                 |
| `--seconds` | Seconds to subtract from now                 |
| `--version` | Print `expired x.y.z` and exit `0`           |
| `--help`    | Show argparse help                           |

The CLI prints `expired` or `not expired`.

| Result              | Stdout           | Exit |
| ------------------- | ---------------- | ---- |
| Still valid         | `not expired`    | `0`  |
| Expired             | `expired`        | `1`  |
| `--version`         | `expired x.y.z`  | `0`  |
| Missing or bad time | error on stderr  | `2`  |

The `if` branch runs when the CLI exits `0` (not expired):

```bash
if expired --time "2022-10-19" >/dev/null; then
    echo "Still valid"
else
    echo "Date has expired or the input was invalid"
fi
```

## Examples

```python
from datetime import datetime, timezone
from lupaxa.expired import is_expired

timestamps = [
    "2022-09-01 12:00:00",
    "2024-10-01 12:00:00",
    "2025-01-01 12:00:00",
]
expired_items = [item for item in timestamps if is_expired(item)]

cutoff = datetime(2025, 11, 6, tzinfo=timezone.utc)
dates = ["2025-10-01", "2025-06-01", "2025-11-01"]
stale = [item for item in dates if is_expired(item, days=3, now=cutoff)]
```

## Development

```bash
make init
make python-install-dev
make python-check
```

<a href="https://github.com/the-lupaxa-project">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/components/footer-for-child-orgs.svg" alt="The Lupaxa Project Footer" width="100%" />
</a>
