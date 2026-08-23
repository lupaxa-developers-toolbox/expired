# expired

Tiny utility to check whether a timestamp has expired relative to UTC now.

Install the **`lupaxa-expired`** package and import the `lupaxa.expired`
namespace. Use it from Python or from the `expired` CLI in shell scripts.

```bash
pip install lupaxa-expired
```

```python
from lupaxa.expired import is_expired

if is_expired("2022-10-19 14:43:57.563803"):
    print("Expired")
```

```bash
expired --time "2022-10-19 14:43:57.563803"
expired --version
```

## What counts as expired

`is_expired(when)` compares `when` to `(now - delta)`:

-   With no window, `delta` is zero. Any time strictly before UTC now is
    expired. A time equal to now is not.
-   Pass `days=3` (or other parts) or an explicit `timedelta` to use a
    window instead of a hard cutoff at now.
-   Naive datetimes are treated as UTC.

That is the same rule the CLI uses.

## What you get

-   A boolean library API (`is_expired`) plus helpers to parse timestamps
    and build windows
-   Built-in SQL, ISO-8601, and date-only formats; `fmt=` for anything else
-   A small CLI with stdout `expired` / `not expired` and exit codes for
    scripts
-   Python 3.10+, no runtime dependencies

## Next steps

- [Getting started](getting-started.md) — install and first checks
- [Usage](usage.md) — library options and CLI flags
- [Reference](reference.md) — public API and exit codes
- [Examples](examples.md) — copy-paste recipes
