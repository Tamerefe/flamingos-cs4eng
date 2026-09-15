# S2.2 — The data stack

**Day 2 · 09:30–11:00 · You work in pairs.**

Yesterday you computed four numbers. Today you compute them for 133 000 rows,
sliced by machine and by hour.

## What you need open

| | |
| --- | --- |
| **Terminal** | in `~/dev/<your-repo>` |
| **Editor** | `src/factoryflow/pipeline.py` and `anomalies.py` |
| **Course folder** | `~/dev/factoryflow-course` |

## 1 · Get the files

```bash
cd ~/dev/factoryflow-course/s2-2-data-stack/start
cp -r src ~/dev/<your-repo>/

cd ~/dev/<your-repo>
git status
git add -A && git commit -m "S2.2 starting point"
```

## 2 · Read two functions first

`clean()` is the one built on the projector. `rolling_zscore()` and `detect()`
are written for you. Each has a **read this one** block above it naming the
single idea worth taking from it. Read those three before you write anything.

## 3 · Do the work (~50 min)

| | What | Where | Roughly |
| --- | --- | --- | --- |
| **CORE 1** | `resample_readings()` — two flag columns | `pipeline.py` | 15 min |
| **CORE 2** | `kpi_table()` — four metric columns | `pipeline.py` | 25 min |
| **CORE 3** | `stuck_sensor()` — one line | `anomalies.py` | 10 min |

**CORE 2 is the session.** It is yesterday's four formulas producing 2232
answers instead of one. If you finish CORE 1 and CORE 2 you have had a good
session — tomorrow's dashboard needs the KPI table.

Hint ladders are in the file. Use them early.

## 4 · Check it

```bash
uv run python -m factoryflow kpis --freq 1h
```

**Sanity check:** OEE per machine should land between **0.62 and 0.71**.

Above 0.9 or below 0.3 means a bug. The usual culprit is which machine states
count as planned production time.

Then commit.

## Two things worth knowing today

**A dtype you did not notice causes half of all pandas confusion.** When
something behaves strangely, run `df.info()` and `df.head()` first, before
anything else.

**A flag is a request for a human to look.** Count your anomaly flags. If you
are flagging more than about 50 in a month, your threshold is wrong, and
finding that out yourselves is the exercise.

## Finished early?

The **BONUS** list is at the bottom of `anomalies.py`. Take **B2, the vibration
story** — it makes a good Friday demo.
