# Reference

Public names are exported from `lupaxa.expired`.

## Package

| Name                            | Description                                               |
| ------------------------------- | --------------------------------------------------------- |
| `is_expired(when, *, ...)`      | `True` if `when` < `(now - delta)`; `delta` defaults to 0 |
| `parse_datetime(value, *, ...)` | Parse a string or pass through a `datetime`               |
| `make_delta(**parts)`           | Build a `timedelta` from keyword parts                    |
| `ExpiredError`                  | Base error; also raised for an invalid delta part         |
| `ParseError`                    | Unparseable timestamp (`ExpiredError` subclass)           |
| `DEFAULT_FORMATS`               | Built-in `strptime` formats, tried in order               |
| `__version__`                   | Package version string                                    |
| `get_version()`                 | Return `__version__`                                      |

### `is_expired`

```text
is_expired(when, *, delta=None, now=None, fmt=None, **delta_kwargs) -> bool
```

| Parameter        | Type                  | Description                                   |
| ---------------- | --------------------- | --------------------------------------------- |
| `when`           | `str` or `datetime`   | Timestamp to evaluate                         |
| `delta`          | `timedelta`, optional | Window subtracted from `now` (default: zero)  |
| `now`            | `datetime`, optional  | Reference time (default: current UTC)         |
| `fmt`            | `str`, optional       | `strptime` format for a string `when`         |
| `**delta_kwargs` | e.g. `days=3`         | Used only when `delta` is omitted             |

Naive `when` and `now` values are treated as UTC. `fmt` is never treated
as a delta part. Unknown `delta_kwargs` raise `ExpiredError`.

### `parse_datetime`

```text
parse_datetime(value, *, fmt=None, formats=None) -> datetime
```

| Parameter | Type                        | Description                                                    |
| --------- | --------------------------- | -------------------------------------------------------------- |
| `value`   | `str` or `datetime`         | Input to parse; a `datetime` is returned as-is                 |
| `fmt`     | `str`, optional             | Single `strptime` format                                       |
| `formats` | `tuple[str, ...]`, optional | Format list when `fmt` is omitted (default: `DEFAULT_FORMATS`) |

Other types and unparseable strings raise `ParseError`. Parsed values
are naive; `is_expired` then treats them as UTC.

### `make_delta`

```text
make_delta(*, years=0, months=0, weeks=0, days=0, hours=0, minutes=0, seconds=0) -> timedelta
```

| Part      | Approximation                         |
| --------- | ------------------------------------- |
| `years`   | 365 days each                         |
| `months`  | 30 days each                          |
| `weeks`   | passed through to `timedelta`         |
| `days`    | passed through to `timedelta`         |
| `hours`   | passed through to `timedelta`         |
| `minutes` | passed through to `timedelta`         |
| `seconds` | passed through to `timedelta`         |

Parts add together (`years=1, days=1` is 366 days).

### `DEFAULT_FORMATS`

Tried in this order when `fmt` is omitted:

| Format                         | Example                         |
| ------------------------------ | ------------------------------- |
| `%Y-%m-%d %H:%M:%S.%f`         | `2022-10-19 14:43:57.563803`    |
| `%Y-%m-%d %H:%M:%S`            | `2022-10-19 14:43:57`           |
| `%Y-%m-%d`                     | `2022-10-19`                    |
| `%Y-%m-%dT%H:%M:%S.%fZ`        | `2024-11-06T08:45:00.123456Z`   |
| `%Y-%m-%dT%H:%M:%S.%f`         | `2024-11-06T08:45:00.123456`    |
| `%Y-%m-%dT%H:%M:%SZ`           | `2024-11-06T08:45:00Z`          |
| `%Y-%m-%dT%H:%M:%S`            | `2024-11-06T08:45:00`           |

The `Z` in those patterns is a literal suffix, not a timezone conversion.
The resulting `datetime` is still naive.

## CLI

The CLI is installed as `expired`.

| Flag          | Meaning                                      |
| ------------- | -------------------------------------------- |
| `--time`      | Timestamp to check (required unless version) |
| `--format`    | Optional `strptime` format for `--time`      |
| `--years`     | Years to subtract from now (365 days each)   |
| `--months`    | Months to subtract from now (30 days each)   |
| `--weeks`     | Weeks to subtract from now                   |
| `--days`      | Days to subtract from now                    |
| `--hours`     | Hours to subtract from now                   |
| `--minutes`   | Minutes to subtract from now                 |
| `--seconds`   | Seconds to subtract from now                 |
| `--version`   | Print `expired x.y.z` and exit `0`           |
| `--help`      | Show argparse help                           |

### Exit codes

| Code | Meaning                                      |
| ---- | -------------------------------------------- |
| `0`  | Not expired, or `--version` printed          |
| `1`  | Expired                                      |
| `2`  | Missing `--time`, parse failure, or bad args |
