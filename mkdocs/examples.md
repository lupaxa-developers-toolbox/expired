# Examples

## Filter a list

```python
from lupaxa.expired import is_expired

timestamps = [
    "2022-09-01 12:00:00",
    "2024-10-01 12:00:00",
    "2025-01-01 12:00:00",
]
expired_items = [item for item in timestamps if is_expired(item)]
```

## Shared cutoff

Pin `now` so every item is judged against the same instant:

```python
from datetime import datetime, timezone
from lupaxa.expired import is_expired

cutoff = datetime(2025, 11, 6, tzinfo=timezone.utc)
dates = ["2025-10-01", "2025-06-01", "2025-11-01"]
expired_list = [item for item in dates if is_expired(item, now=cutoff)]
```

A three-day window against that same cutoff:

```python
stale = [item for item in dates if is_expired(item, days=3, now=cutoff)]
```

## Custom format

```python
from lupaxa.expired import is_expired

is_expired("2025/11/01 14:43:57", fmt="%Y/%m/%d %H:%M:%S", days=2)
```

`parse_datetime` accepts the same `fmt`, or a custom `formats` tuple:

```python
from lupaxa.expired import parse_datetime

parse_datetime("2024/11/06 09:00:00", fmt="%Y/%m/%d %H:%M:%S")
parse_datetime("06-11-2024", formats=("%d-%m-%Y",))
```

## Handle bad input

```python
from lupaxa.expired import ParseError, is_expired

try:
    is_expired("next Tuesday")
except ParseError as exc:
    print(f"Could not parse: {exc}")
```

## Combined window

```python
from datetime import datetime, timezone
from lupaxa.expired import is_expired, make_delta

now = datetime(2025, 11, 6, 12, 0, 0, tzinfo=timezone.utc)
is_expired("2025-10-01 12:00:00", weeks=2, days=3, now=now)
is_expired("2025-10-01 12:00:00", delta=make_delta(weeks=2, days=3), now=now)
```

## Shell

The `if` branch runs when the CLI exits `0` (not expired). Exit `1` is
expiry. Redirect stdout if you only care about the status:

```bash
if expired --time "2022-10-19" >/dev/null; then
    echo "Still valid"
else
    echo "Date has expired"
fi
```

Window and custom format:

```bash
expired --time "2024/11/06 09:00:00" --format "%Y/%m/%d %H:%M:%S" --days 1
expired --time "2024-11-06T09:00:00Z" --hours 12
```
