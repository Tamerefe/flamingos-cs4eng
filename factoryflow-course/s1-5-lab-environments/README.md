# S1.5 — Lab: environments and dependencies

**Day 1 · 16:00–18:00 · You work in pairs. From 17:30 you work with another pair.**

Goal: **another pair clones your repository and gets it running in five minutes, using only your README.**

## What you need open

| **Terminal**      | in `~/dev/<your-repo>`                                |
| ----------------- | ----------------------------------------------------- |
| **Course folder** | `~/dev/factoryflow-course`                            |
| **On the wall**   | the register sheet — you need other pairs' URLs later |

## 1 · Get today's files

```bash
cd ~/dev/factoryflow-course/s1-5-lab-environments/start
cp pyproject.toml README.md ~/dev/<your-repo>/

cd ~/dev/<your-repo>
git status
git add -A && git commit -m "S1.5 starting point"
```

Open `pyproject.toml`. Every line has a comment explaining it.

## 2 · The build checklist (~70 min)

Work down it in order. Tick as you go.

| #   | Do this                                                                                 |
| --- | --------------------------------------------------------------------------------------- |
| 1   | `uv venv` — then look at what appeared on disk                                          |
| 2   | Read `pyproject.toml` top to bottom                                                     |
| 3   | `uv add pandas` — and anything else the code actually imports                           |
| 4   | `uv add --dev pytest ruff` — the tools _you_ need, which a user does not                |
| 5   | Open `uv.lock` and read a bit of it. Do not edit it.                                    |
| 6   | `rm -rf .venv`, then `uv sync`                                                          |
| 7   | Install a wrong pandas version on purpose, watch the code break, restore with `uv sync` |
| 8   | Write your `README.md`                                                                  |
| 9   | Commit `pyproject.toml` **and** `uv.lock`. Check `.venv` is ignored.                    |
| 10  | Push to GitHub                                                                          |

**Step 6 is the one to actually do.** Delete the folder, feel the moment, rebuild it in four seconds. After that, `.venv` stops being mysterious.

### Two ideas you need for this

- **`pyproject.toml` is an intention:** "this project needs pandas."
- **`uv.lock` is a fact:** "pandas 2.2.3, and these 14 other packages, exactly."

A bill of materials, and a parts list with supplier part numbers.

### Step 8 — writing the README

This is the step that decides whether today worked. Write it for **the version of you that has forgotten everything.** That person is real and they turn up in October.

Write it **from the terminal**: run each command as you write it down.

It has to answer three things:

1. What is this?
2. What does it need?
3. How do I run it?

## 3 · The clone test (17:30–17:50)

Another pair clones your repo and runs it **using only your README**. You may not help them. You do the same to theirs.

First, two minutes of access:

- Get the URL off the register sheet.
- Add the other pair on **Settings → Collaborators**. They accept.

Then:

```bash
git clone <their-repo-url>
cd <their-repo>
uv sync
uv run python -m factoryflow --help
```

**Write down every point where you got stuck.** Hand that list to the authors.

Almost every README fails the first time. That is the exercise, and it is the most useful twenty minutes of the day.

## 4 · Fix and push

Fix your README from the list you were handed. Commit. Push. That is the last commit of day 1.

## Checkpoint

Someone else's laptop runs your project from a fresh clone. Say so out loud.

## Finished early?

Run the clone test on yourselves: a fresh clone into a new folder, and follow your own README literally, doing nothing it does not tell you to do.
