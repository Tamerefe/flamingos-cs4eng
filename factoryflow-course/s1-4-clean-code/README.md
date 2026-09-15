# S1.4 — Clean code

**Day 1 · 14:00–15:30 · You work in pairs.**

Turn the unreadable part of the legacy script into functions with names that say what they do.

## What you need open

| **Terminal**      | in your own repository, `~/dev/<your-repo>`                   |
| ----------------- | ------------------------------------------------------------- |
| **Editor**        | the same folder                                               |
| **Course folder** | `~/dev/factoryflow-course` — the drawer you take files out of |

You never edit anything inside `factoryflow-course`. You copy out of it.

## 1 · Get the files (5 min)

```bash
cd ~/dev/factoryflow-course/s1-4-clean-code/start

cp -r src ~/dev/<your-repo>/     # take them across

cd ~/dev/<your-repo>
git status                       # see exactly what arrived
git add -A
git commit -m "S1.4 starting point"
```

Now open `src/factoryflow/metrics.py` in your editor. **Everything you need is in that file.** There is no other document to find.

## 2 · Read one function first (5 min)

`quality()` is already written — it is the one the facilitator just built on the projector. Read it before you write anything. The three functions you write have the same shape.

## 3 · Do the work (~35 min)

Four tasks, in this order. The full brief for each is in the file, at the task.

|            | What              | Where                        | Roughly |
| ---------- | ----------------- | ---------------------------- | ------- |
| **CORE 1** | `load_readings()` | `src/factoryflow/loading.py` | 10 min  |
| **CORE 2** | `availability()`  | `src/factoryflow/metrics.py` | 10 min  |
| **CORE 3** | `performance()`   | `src/factoryflow/metrics.py` | 10 min  |
| **CORE 4** | `oee()`           | `src/factoryflow/metrics.py` | 5 min   |

Two habits for this session, and they matter more than the code:

- **Change one thing, run it, commit.** Then the next thing.
- **Ninety seconds to pick a name.** A good-enough name that ships is worth more than a perfect name after 15 minutes.

Every task has a **HINT 1 / HINT 2 / HINT 3** ladder underneath it. HINT 3 is very close to the answer.

## 4 · Check it

```bash
uv run python -m factoryflow oee
```

It prints a table:

```
machine_id  availability  performance  quality    oee
      M-01        0.8750       0.8000   0.9619 0.6733
      M-02        0.7941       0.8313   0.9604 0.6340
      M-03        0.8614       0.8023   0.9589 0.6627
      M-01        0.8771       0.8274   0.9690 0.7032
      M-02        0.8350       0.7740   0.9556 0.6176
      M-03        0.8559       0.8309   0.9638 0.6855
       M-1        0.8966       0.8231   0.9616 0.7096
       M-2        0.8523       0.8284   0.9592 0.6773
       M-3        0.8333       0.8124   0.9606 0.6504
      m-01        0.8889       0.8358   0.9791 0.7274
      m-02        0.8804       0.8420   0.9580 0.7101
      m-03        0.8587       0.8135   0.9544 0.6667
```

**Twelve rows. The factory has three machines** — and `M-01` is in there twice. `M-01`, `M-1`, `m-01` and `M-01`are all the same machine, written four ways, so every number above is computed over a fraction of the rows it should cover. Your code is right; the data is not.

That is tomorrow morning.

The gate for today is smaller, and it is about your code only:

```bash
uv run python -c "from factoryflow.metrics import oee; print('ok')"
```

Prints `ok`? Commit.

## Stuck?

**Fifteen minutes on one thing is the limit.** Then take the finished file:

```bash
cd ~/dev/factoryflow-course/s1-4-clean-code/solution
cp src/factoryflow/metrics.py ~/dev/<your-repo>/src/factoryflow/
```

Commit it in your repo like anything else. `"Take the finished metrics.py"` is an honest line in a history.

Afterwards, `git diff` in your own repo shows you exactly what you were meant to write.

## Finished early?

There is a **BONUS** list at the bottom of `metrics.py`. Commit the core first, then take **one**.
