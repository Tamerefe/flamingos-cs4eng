# FactoryFlow

OEE reporting for production line A. Reads the per-minute sensor export from the
three CNC machines and answers one question: **how much of the time we planned to
produce, did we actually produce good parts?**

```
OEE = Availability x Performance x Quality
```

## Clone and run in five minutes

You need [uv](https://docs.astral.sh/uv/) and nothing else -- it fetches the
right Python for you.

```bash
git clone <your-fork-url> factoryflow
cd factoryflow
uv sync                                  # builds the environment from uv.lock
uv run python -m factoryflow oee         # the headline numbers
```

Expected output:

```
machine_id  availability  performance  quality    oee  units_produced  units_rejected
      M-01        0.8772       0.8274   0.9690 0.7032          427355           13261
      M-02        0.8349       0.8396   0.9590 0.6723          421078           17245
      M-03        0.8559       0.8308   0.9638 0.6853          423957           15364
```

If your numbers differ, something is wrong -- start with `uv run pytest`.

## The service and the dashboard

```bash
uv run uvicorn factoryflow.api:app --reload --port 8000   # http://localhost:8000/docs
uv run streamlit run dashboard/app.py                     # http://localhost:8501
```

The dashboard reads from the API over HTTP; it never touches the CSV. Start the
API first or the dashboard will tell you it cannot reach it.

Or run both in containers, which needs no Python on your machine at all:

```bash
docker compose up --build
```

## What is in here

| Path | What it does |
|---|---|
| `src/factoryflow/config.py` | Every constant, named. Nothing else holds a bare number. |
| `src/factoryflow/loading.py` | Reads the CSV. Does **not** clean it. |
| `src/factoryflow/pipeline.py` | Cleans, buckets in time, builds the KPI table. |
| `src/factoryflow/metrics.py` | The four formulas. |
| `src/factoryflow/anomalies.py` | Two detectors and two rules. No ML. |
| `src/factoryflow/api.py` | Four read-only HTTP routes. |
| `src/factoryflow/schemas.py` | The shapes that cross the network. |
| `dashboard/app.py` | What the shift supervisor opens. |
| `tests/` | 35 tests. Three of them exist because of a specific incident. |
| `data/raw/` | The March export. Committed on purpose: it is the input everything else is derived from. |

## The commands you will actually type

```bash
uv run pytest                      # the tests
uv run ruff check src tests        # lint
uv run python -m factoryflow kpis --freq 8h --machine M-02
uv run python -m factoryflow anomalies --min-severity 0.75
```

`make` wraps all of these if you have it (`make help`).

## Things worth knowing before you change anything

**Timestamps in the export have no timezone suffix. They are UTC.** Read them as
local time and every shift boundary after 29 March 2026 lands an hour off,
because that is the day the clocks change. `test_shift_boundaries_are_utc` exists
to stop that coming back.

**`SETUP` is excluded from planned production time.** A changeover is planned
work, so it is not held against the machine. This is a modelling choice that
could have gone the other way, and it is the single assumption most worth
arguing about -- change `config.PLANNED_STATES` and availability moves for
every machine at once.

**A metric with a zero denominator is `NaN`.** An idle night shift produced
nothing; its quality is unknown. Returning zero would drag
every average down quietly, which is how a report starts lying.

**`data/processed/` is gitignored.** Anything you compute can be recomputed.
Committing derived data means someone will eventually trust a stale copy of it.
