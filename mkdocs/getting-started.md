# Getting started

## Requirements

- Python 3.10 or newer
- No runtime dependencies

## Install

```bash
python3 -m pip install lupaxa-expired
```

The PyPI name is `lupaxa-expired`. The import path is `lupaxa.expired`.
The console script is `expired`. `lupaxa` is a namespace package — there
is no `lupaxa/__init__.py`.

### From source (development)

```bash
make init
make python-install-dev
```

Site Markdown lives in `mkdocs/` (not GitHub’s special `docs/` directory).
After makefile-skills are installed:

```bash
make mkdocs-serve
```

## First check

A timestamp is expired when it is strictly earlier than
`(now - delta)`. With no window, that is UTC now:

```python
from lupaxa.expired import is_expired

if is_expired("2022-10-19 14:43:57.563803"):
    print("Expired")
else:
    print("Still valid")
```

Pin the reference time when you need a stable result (tests, docs,
reproducible scripts):

```python
from datetime import datetime, timezone
from lupaxa.expired import is_expired

cutoff = datetime(2025, 11, 6, 12, 0, 0, tzinfo=timezone.utc)
is_expired("2025-11-01 12:00:00", now=cutoff)  # True
is_expired(cutoff, now=cutoff)                 # False — equal is not expired
```

The same check from the shell:

```bash
expired --time "2022-10-19 14:43:57.563803"
```

The CLI prints `expired` or `not expired` and exits `1` or `0`. Exit `2`
means the timestamp could not be parsed or `--time` was missing.

## Add a window

Keyword parts (or `--days` and friends on the CLI) subtract a window from
now before comparing:

```python
from datetime import datetime, timezone
from lupaxa.expired import is_expired

now = datetime(2025, 11, 6, 12, 0, 0, tzinfo=timezone.utc)
is_expired("2025-11-05 12:00:00", days=3, now=now)  # False — still inside 3 days
is_expired("2025-11-01 12:00:00", days=3, now=now)  # True — older than 3 days
```

```bash
expired --time "2022-10-19 14:43:57.563803" --days 3
```

Years are 365 days and months are 30 days. See [Usage](usage.md) for the
full set of parts and flags.

## Makefile helpers

```bash
make init                 # clone makefile-skills into .makefiles/
make python-install-dev   # editable install with [dev]
make python-check         # lint + type + test (via makefile-skills)
make mkdocs-serve         # local docs site
```
