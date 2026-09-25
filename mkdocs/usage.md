# Usage

## How Comparison Works

`is_expired(when)` returns `True` when `when < (now - delta)`.

| Situation                         | Result           |
| --------------------------------- | ---------------- |
| `when` is earlier than the cutoff | expired (`True`) |
| `when` equals the cutoff          | not expired      |
| `when` is later than the cutoff   | not expired      |

`now` defaults to the current UTC time. `delta` defaults to zero. Naive
`when` and `now` values are given UTC (`tzinfo=timezone.utc`).

## Library

### Compare to UTC Now

```python
from lupaxa.expired import is_expired

is_expired("2022-10-19 14:43:57.563803")
```

### Use a Window

Pass a `timedelta` or keyword parts. Parts are ignored when `delta=` is
set. `fmt` is a parse format, not a delta part.

```python
from datetime import datetime, timedelta, timezone
from lupaxa.expired import is_expired

is_expired("2022-10-19 14:43:57.563803", days=3)
is_expired(datetime.now(timezone.utc) - timedelta(hours=72), hours=48)
```

Accepted parts: `years`, `months`, `weeks`, `days`, `hours`, `minutes`,
`seconds`. They add together. `timedelta` has no year or month fields, so
this package treats **1 year as 365 days** and **1 month as 30 days**.

An unknown part raises `ExpiredError`:

```python
from lupaxa.expired import ExpiredError, is_expired

try:
    is_expired("2022-10-19", dayz=3)
except ExpiredError:
    print("Unknown delta part")
```

### Pin the Reference Time

```python
from datetime import datetime, timezone
from lupaxa.expired import is_expired

cutoff = datetime(2025, 11, 6, tzinfo=timezone.utc)
is_expired("2025-10-01", now=cutoff)
is_expired("2025-10-01", days=3, now=cutoff)
```

### Custom Parse Format

```python
is_expired("2025/11/01 14:43:57", fmt="%Y/%m/%d %H:%M:%S", days=2)
```

Without `fmt`, strings are tried against the built-in list in
[Reference](reference.md#default_formats). Unparseable input raises
`ParseError` (a subclass of `ExpiredError`).

### Helpers

`parse_datetime` and `make_delta` are public if you want the pieces
without running the check:

```python
from lupaxa.expired import make_delta, parse_datetime

parse_datetime("2024-11-06T08:45:00Z")
make_delta(days=2, hours=3)
```

## CLI

```bash
expired --time "2022-10-19 14:43:57.563803"
expired --time "2022-10-19 14:43:57.563803" --days 3
expired --time "2024-11-06T09:00:00Z" --hours 12
expired --time "2024/11/06 09:00:00" --format "%Y/%m/%d %H:%M:%S" --days 1
expired --version
expired --help
```

`--time` is required unless you pass `--version`. Delta flags:
`--years`, `--months`, `--weeks`, `--days`, `--hours`, `--minutes`,
`--seconds`. Months are 30 days; years are 365 days.

### Output and Exit Codes

| Result              | Stdout           | Exit |
| ------------------- | ---------------- | ---- |
| Still valid         | `not expired`    | `0`  |
| Expired             | `expired`        | `1`  |
| `--version`         | `expired x.y.z`  | `0`  |
| Missing or bad time | error on stderr  | `2`  |

Use the exit status in scripts. The `if` branch below runs when the CLI
exits `0` (not expired):

```bash
if expired --time "2022-10-19" >/dev/null; then
    echo "Still valid"
else
    echo "Date has expired or the input was invalid"
fi
```
