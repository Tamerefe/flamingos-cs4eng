# FactoryFlow — the course material

Everything you need for the three days. **You never write anything in here.**
Your own repository is the one you create in S1.3, and all your work lives
there.

Most sessions have a folder:

```
s1-4-clean-code/
  README.md     what this session is, where to stand, how you know you are done
  start/        the files to copy into your repository at the start
  solution/     the same files, finished
```

## The loop, every session

```bash
cd ~/dev/factoryflow-course
cp -r s1-4-clean-code/start/* ~/dev/<your-repo>/

cd ~/dev/<your-repo>
git status                                  # exactly what arrived
git add -A
git commit -m "S1.4 starting point"
```

Then work in your own repository, and commit as you go.

## Stuck for fifteen minutes?

Take the finished file. No discussion, no loss of face:

```bash
cp ~/dev/factoryflow-course/s1-4-clean-code/solution/src/factoryflow/metrics.py \
   ~/dev/<your-repo>/src/factoryflow/
```

…and commit it like anything else. *"Take the finished metrics.py"* is an honest
line in a history.

## Completely lost?

`day-1-complete/`, `day-2-complete/` and `day-3-complete/` hold the whole
application as it should look at 18:00 on that day. Copy one over your
repository and you rejoin cleanly the next morning. **It overwrites your work** —
so commit first, and it stays in your history either way.

## What the markers mean

| Marker | What it wants |
|---|---|
| `TODO(L1)` | one to five lines; the code around it is already there |
| `TODO(L2)` | a whole function body, written to the signature above it |
| `TODO(EXPLAIN)` | prose, not code. Two or three sentences under `Your answer:` |

The explanations are not decoration. From S3.2 a test fails while any of them is
still empty, and before then a facilitator will ask you the same question out
loud.

## How to work through a file

The first block in the file lists the session's **CORE** tasks in order, with a
time budget for each. Do them in that order. Every task carries a **HINT 1 / 2 /
3** ladder that ends very close to the answer — the hints are there to be used.

Some functions are already written and marked *read this one*. Read them; the
ones you write are shaped after them.

Finished the core and committed it? There is a **BONUS** list at the bottom of
the file. Take one.

## Before day 1

[SETUP.md](SETUP.md) — do it on the laptop you are bringing, four weeks ahead.

## The commands, all week

[s1-2-professional-workbench/cheatsheet.md](s1-2-professional-workbench/cheatsheet.md)
— moving around, copying files, running Python, and what each error message
means. Keep it open in a tab.
