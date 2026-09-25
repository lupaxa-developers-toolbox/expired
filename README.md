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

## Install

```bash
pip install lupaxa-expired
```

Requires Python 3.10+. No runtime dependencies.

## Usage

```python
from datetime import datetime, timezone
from lupaxa.expired import is_expired

if is_expired("2022-10-19 14:43:57.563803"):
    print("Expired")

cutoff = datetime(2025, 11, 6, tzinfo=timezone.utc)
is_expired("2025-10-01", days=3, now=cutoff)
```

Strings may be SQL-style, ISO-8601 (with or without `Z`), or date-only.
Pass `fmt=` for a custom `strptime` format. Naive datetimes are treated
as UTC. Keyword parts such as `days=3` or an explicit `timedelta` set
the window; years are 365 days and months are 30 days.

```bash
expired --time "2022-10-19 14:43:57.563803"
expired --time "2022-10-19 14:43:57.563803" --days 3
expired --version
```

The CLI prints `expired` or `not expired`. Exit `0` means not expired
(or `--version`), `1` means expired, and `2` means bad input.

## Documentation

Site pages live in `mkdocs/` and publish to
<https://expired.thelupaxaproject.org/>.

```bash
make init
make python-install-dev
make mkdocs-serve
```

<a href="https://github.com/the-lupaxa-project">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/components/footer-for-child-orgs.svg" alt="The Lupaxa Project Footer" width="100%" />
</a>
