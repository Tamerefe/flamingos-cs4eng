# S3.2 — Testing

**Day 3 · 09:30–11:00 · You work in pairs.**

Half an hour ago this room spent fifteen minutes failing to find three changes by
reading. `pytest` turns four tests red in 2.2 seconds — including the one nobody
in the room spotted — every time anyone touches the code, forever.

## What you need open

| | |
| --- | --- |
| **Terminal** | in `~/dev/<your-repo>` |
| **Editor** | `tests/test_metrics.py` and `tests/test_pipeline.py` |
| **Course folder** | `~/dev/factoryflow-course` |

## 1 · Get the files

```bash
cd ~/dev/factoryflow-course/s3-2-testing/start
cp -r tests ~/dev/<your-repo>/
cp pyproject.toml ~/dev/<your-repo>/

cd ~/dev/<your-repo>
git add -A && git commit -m "S3.2 starting point"
```

## 2 · Read what you were given

**The whole test suite is written except five bodies.** The sixteen intact
tests are your reference — when you are unsure how to write something, find the
test that already does it and copy its shape. That is also how the job works.

`conftest.py` is complete. It gives you `make_readings()`, which builds a known
situation to test against.

## 3 · Write five assertions (~50 min)

| Where | Test | What it teaches |
| --- | --- | --- |
| `test_metrics.py` | `test_availability_ignores_setup` | comparing floats approximately |
| `test_metrics.py` | `test_quality_counts_good_units` | the same, shorter |
| `test_metrics.py` | `test_quality_on_empty_bucket` | asserting **NaN** |
| `test_metrics.py` | `test_quality_never_exceeds_one_on_clean_data` | a rule over the whole real dataset |
| `test_pipeline.py` | `test_resample_preserves_total_units` | a conservation law across three frequencies |

### The reflex to build today

**Write the assertion → run it → watch it fail → make it pass.**

Every time. A test you have never seen fail might be asserting nothing at all.

### What a test is

> A test is a written-down promise that the code still does what it did when
> you understood it.

You cannot test everything. Test where being wrong is expensive:

- **The boundaries.** Zero, empty, negative, one, maximum.
- **The rules you would say out loud to a colleague.** "Quality is always
  between 0 and 1."
- **Every bug you have ever fixed.** Write the test the moment you fix it and
  that bug can never come back quietly.

### The test name is documentation

`test_quality_is_one_when_nothing_rejected` tells you the rule without reading
the body. Write names like sentences all session.

## 4 · Add a regression test

Pick one of this morning's three bugs and write the test that would have
refused to let it in.

## 5 · Check it

```bash
uv run pytest
```

Green, with **at least five tests**, including at least one for an overnight
bug. Then commit.

## A question to ask yourselves about every assertion

> *"Could this still pass if the function returned 7?"*

If yes, the assertion is decoration.
