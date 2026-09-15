# S3.3 — Containers and licensing

**Day 3 · 11:30–13:00 · You work in pairs.**

Day 1 made your Python dependencies reproducible. Today you do it for
everything else: the operating system, the system libraries, the Python version
itself.

## What you need open

| | |
| --- | --- |
| **Terminal** | in `~/dev/<your-repo>` |
| **Editor** | `Dockerfile` and `docker-compose.yml` |
| **Running** | Docker Desktop — start it now, it takes a minute |

## 1 · Get the files

```bash
cd ~/dev/factoryflow-course/s3-3-containers-licensing/start
cp Dockerfile docker-compose.yml .dockerignore ~/dev/<your-repo>/

cd ~/dev/<your-repo>
git add -A && git commit -m "S3.3 starting point"
```

The Dockerfile is **written for you**. You read it, you do not write it.

## 2 · Three ideas

**An image is the recipe. A container is the meal cooked from it.** Cook the
same image a thousand times, get the same meal.

**What is in the box:**

```
your code           <- changes every commit
your dependencies   <- pyproject.toml + uv.lock, from day 1
Python 3.12         <- the thing you fought with on Tuesday
a minimal Linux     <- the thing you never thought about
─────────────────
the host's kernel   <- NOT in the box. That is why it is not a VM.
```

**A container is a building with sealed windows.** `-p 8000:8000` drills one
hole in the wall. Nothing else gets in or out.

## 3 · Do it (30–60 min)

| # | Do this |
| --- | --- |
| 1 | Build the image. Watch the layers go by. Time it. |
| 2 | `docker compose up`. Open both URLs in a browser. |
| 3 | Change the host port to 9000. **Predict what happens before you look.** |
| 4 | Change one line of Python and rebuild. Notice how much was cached. |
| 5 | `docker compose down`, then up again. Notice what survived. |

Two lines in the Dockerfile are worth arguing about:

- **`COPY pyproject.toml uv.lock` comes before `COPY src/`.** Your code changes
  hourly, your dependencies monthly. That ordering turns a 3-minute rebuild into
  a 5-second one.
- **`--host 0.0.0.0`.** Inside the container, `localhost` means "this
  container", which is not where you are sitting.

## 4 · Licensing (60–75 min)

| Family | Example | In one sentence |
| --- | --- | --- |
| Permissive | MIT, Apache-2.0 | "Do what you want, keep my name on it" |
| Weak copyleft | LGPL, MPL | "Changes to *my* part stay open" |
| Strong copyleft | GPL-3.0 | "If you ship it, ship your source too" |
| Source-available | BSL, SSPL | "Read the actual terms" |

**Your job: add a `LICENSE` file to your repo and one line in your README
saying why you picked it.** Ninety seconds of real decision.

Then a question worth sitting with: you are shipping pandas, FastAPI and
Streamlit inside that image. Do you know what those permit?

## 5 · Pick two (75–88 min)

Take **two** items off the hardening menu. The choosing is the exercise.

## Checkpoint

`docker compose up` runs your API and your dashboard on a machine with none of
your tools installed. A `LICENSE` file is committed.
