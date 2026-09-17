# S2.3 — APIs

**Day 2 · 11:30–13:00 · You work in pairs.**

Your numbers currently exist in your terminal. By 13:00 they have a URL.

## What you need open

| **Terminal 1** | running the API server       |
| -------------- | ---------------------------- |
| **Terminal 2** | for git and everything else  |
| **Editor**     | `src/factoryflow/api.py`     |
| **Browser**    | `http://localhost:8000/docs` |

## 1 · Get the files

```bash
cd ~/dev/factoryflow-course/s2-3-apis/start
cp -r src ~/dev/<your-repo>/

cd ~/dev/<your-repo>
git add -A && git commit -m "S2.3 starting point"
```

## 2 · Start the server and leave it running

```bash
uv run uvicorn factoryflow.api:app --reload --port 8000
```

`--reload` restarts it whenever you save. If the port is taken, use `--port 8001` and adjust your URLs.

Now open `http://localhost:8000/docs` in a browser. That page is generated from the type hints you wrote yesterday. Nobody wrote that page.

## 3 · Do the work (~50 min)

|            | Route                   | Where    | Roughly                            |
| ---------- | ----------------------- | -------- | ---------------------------------- |
| **CORE 1** | `/health`               | `api.py` | 5 min, built with the facilitator  |
| **CORE 2** | `/machines`             | `api.py` | 10 min, built with the facilitator |
| **CORE 3** | `/metrics` — two gaps   | `api.py` | 20 min                             |
| **CORE 4** | `/anomalies` — two gaps | `api.py` | 15 min                             |

The routes, the signatures and the fiddly parts are given. What is left in CORE 3 and CORE 4 is the part with a decision in it:

- **`/metrics`:** does "the 14th to the 15th" mean one day or two? Your answer shows up in every number the dashboard draws tomorrow.
- **`/anomalies`:** what order do results come back in? Nobody scrolls an alert list. If the six-hour breakdown is not in the first three rows, it may as well not be in the response.

## 4 · Reading a status code

Ask _whose fault is it_:

| **200** | Fine                               |
| ------- | ---------------------------------- |
| **404** | That thing does not exist          |
| **422** | You sent nonsense — **your** fault |
| **500** | The server broke — **its** fault   |

## 5 · Check it

In a browser:

```
http://localhost:8000/metrics?machine=M-01&freq=1h
```

returns JSON with real numbers, and `/docs` loads. Then commit.

**This has to work by 13:00** — this afternoon's dashboard reads from it.

## Finished early?

Point your browser at another pair's API. Same routes, different laptop.
