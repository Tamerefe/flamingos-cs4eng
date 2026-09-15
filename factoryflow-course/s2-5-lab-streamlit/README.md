# S2.5 — Lab: the dashboard

**Day 2 · 16:00–18:00 · You work in pairs. Every pair presents at 17:40.**

## The brief

> The shift supervisor has 30 seconds at the start of each shift. They are
> standing, holding coffee, looking at a screen on the wall.
>
> They do not want your data. They want to know **whether to do something
> differently today.**

**You may show at most five numbers and two charts.** Choosing is the exercise.

## What you need open

| | |
| --- | --- |
| **Terminal 1** | `uv run uvicorn factoryflow.api:app --port 8000` |
| **Terminal 2** | `uv run streamlit run dashboard/app.py` |
| **Editor** | `dashboard/app.py` |
| **On paper** | your sketch — see step 2 |

Both terminals stay running the whole afternoon.

## 1 · Get the files (5 min)

```bash
cd ~/dev/factoryflow-course/s2-5-lab-streamlit/start
cp -r dashboard ~/dev/<your-repo>/

cd ~/dev/<your-repo>
git add -A && git commit -m "S2.5 starting point"
```

## 2 · Sketch it on paper (16:20–16:35) — before any code

Pens, paper, keyboards untouched. Draw your layout, and next to every element
write **the decision it supports**.

If an element does not support a decision, take it off the sketch.

The question to keep asking each other: *"if this number is red, what does the
supervisor do differently?"*

## 3 · Get numbers on screen (~20 min)

| | Gap | Where | Roughly |
| --- | --- | --- | --- |
| **CORE 1** | `fetch()` — one HTTP GET | `dashboard/app.py` | 5 min |
| **CORE 2** | the KPI frame — one `/metrics` call per machine | `dashboard/app.py` | 15 min |

The page is already laid out for you. These two gaps connect it to your API.

**The dashboard reads from your API.** Reading the CSV directly gives you two
places that compute OEE, and then one of them is wrong.

## 4 · The actual lab (16:35–17:40)

Build the dashboard on your sketch. Everything on the page is a suggestion,
including the charts. **Deleting something is as good an answer as adding
something**, and it is the harder one.

Be ready to say what a sixth number would have replaced.

### One thing about Streamlit

The whole script re-runs top to bottom every time you touch anything on the
page. That explains almost every confusing thing it does.

It is also pure Python. No HTML, no CSS, no JavaScript.

## 5 · Show and tell (100–118 min)

**90 seconds per pair, on the projector.** Say what you show, why, and what you
decided to leave out.

The screen freeze is at 100 minutes, whatever state you are in.

## Checkpoint

A browser shows numbers that come from **your API**, which reads **your
pipeline**. Committed and pushed.

## Finished early?

Take **B6** from the bonus menu at the bottom of `app.py`: show your dashboard
to another pair, say nothing, point at nothing, and watch where they look
first. It rehearses Friday.
