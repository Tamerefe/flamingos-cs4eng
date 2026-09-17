"""The face of FactoryFlow: what the shift supervisor actually opens.

This dashboard talks to the API over HTTP. It does not import `factoryflow` and
it does not read the CSV. That separation is the whole point of yesterday's
work: the numbers have one source, and anything that wants them asks for them.

Run it with the API already running:

    uvicorn factoryflow.api:app --port 8000
    streamlit run dashboard/app.py

Set FACTORYFLOW_API to point somewhere else (docker compose does).
"""

from __future__ import annotations

import os
from datetime import date, datetime, timezone
from pathlib import Path

import httpx
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

API_BASE = os.environ.get("FACTORYFLOW_API", "http://localhost:8000")
REQUEST_TIMEOUT_S = 30.0

# â•â• THIS LAB â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#
#   CORE 1  fetch()      one HTTP GET, below                        ~5 min
#   CORE 2  the KPI frame, further down                            ~15 min
#   THEN    make it YOUR dashboard -- that is the other 45 minutes.
#
#   The two core gaps exist to get numbers on the screen. They are not the
#   lab. The lab is the brief:
#
#       Your supervisor gives this thirty seconds before the shift meeting.
#       FIVE numbers. If a sixth earns its place, say which one it replaces.
#
#   Everything on this page right now is a suggestion, including the charts.
#   Delete what does not earn its place. The BONUS list at the bottom is the
#   menu if you would rather add than subtract.
#
#   YOU NEED TWO TERMINALS. This is the single most common stumble of the
#   afternoon:
#       terminal 1:  uv run uvicorn factoryflow.api:app --port 8000
#       terminal 2:  uv run streamlit run dashboard/app.py
#   If the page shows an API error, terminal 1 is not running. The sidebar
#   says so; read it before you change any code.
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

# TODO(EXPLAIN): Reading the CSV directly here would be fewer moving parts. Why go through the
# API instead?
# Two or three sentences, in your own words. Not what the code
# does line by line -- why it does it that way.
#
# Your answer:
#

# --- palette -----------------------------------------------------------------
SURFACE = "#fcfcfb"
GRID    = "#e1e0d9"
AXIS    = "#c3c2b7"
INK_MUTED     = "#898781"
INK_SECONDARY = "#52514e"

# Dark canvas used by the OEE time-series.
CHART_BG   = "#13151f"
CHART_GRID = "#252838"
CHART_AXIS = "#353854"

MACHINE_COLOUR = {"M-01": "#4f9cf9", "M-02": "#f97b4f", "M-03": "#30d9a0"}
_MACHINE_RGBA  = {"M-01": "79,156,249", "M-02": "249,123,79", "M-03": "48,217,160"}
FALLBACK_COLOUR = "#a78bfa"
FALLBACK_RGBA   = "167,139,250"

STATUS_GOOD     = "#0ca30c"
STATUS_WARNING  = "#fab219"
STATUS_SERIOUS  = "#ec835a"
STATUS_CRITICAL = "#ef4444"
REJECT_COLOUR   = STATUS_CRITICAL


def colour_for(machine_id: str) -> str:
    return MACHINE_COLOUR.get(machine_id, FALLBACK_COLOUR)


def rgba_for(machine_id: str) -> str:
    return _MACHINE_RGBA.get(machine_id, FALLBACK_RGBA)


def severity_band(severity: float) -> tuple[str, str]:
    """Map a severity to a reserved status colour and a word."""
    if severity >= 0.75:
        return STATUS_CRITICAL, "critical"
    if severity >= 0.5:
        return STATUS_SERIOUS, "serious"
    if severity >= 0.25:
        return STATUS_WARNING, "warning"
    return STATUS_GOOD, "minor"


# --- data --------------------------------------------------------------------


@st.cache_data(ttl=60, show_spinner=False)
def fetch(path: str, **params) -> list[dict]:
    """GET a route on the API and hand back its JSON.

    Cached for a minute: a supervisor changing the machine filter should not
    make the service re-read a month of data every click.
    """
    # TODO(L1): GET {API_BASE}{path} with params, return .json()
    response = httpx.get(f"{API_BASE}{path}", params=params, timeout=REQUEST_TIMEOUT_S)
    response.raise_for_status()
    return response.json()


def api_is_up() -> tuple[bool, str]:
    try:
        health = fetch("/health")
    except httpx.HTTPError as error:
        return False, f"{type(error).__name__}: {error}"
    if not health.get("rows_loaded"):
        return False, "API running but 0 rows loaded â€” check CSV path."
    return True, f"{health['rows_loaded']:,} readings loaded"


# --- charts ------------------------------------------------------------------


def kpi_pie(
    availability: float, performance: float, quality: float
) -> go.Figure:
    """Four individual donut pies: OEE, Availability, Performance, Quality.

    Each donut shows the metric as a filled arc and the remainder as a dark
    background arc, with the percentage annotated in the centre hole.
    """
    from plotly.subplots import make_subplots

    oee_val = (
        availability * performance * quality
        if not any(pd.isna(v) for v in (availability, performance, quality))
        else float("nan")
    )

    metrics = [
        ("OEE",          oee_val,      "#a78bfa"),          # purple
        ("Availability", availability, MACHINE_COLOUR["M-01"]),
        ("Performance",  performance,  MACHINE_COLOUR["M-02"]),
        ("Quality",      quality,      MACHINE_COLOUR["M-03"]),
    ]

    # 1-row × 4-column grid — all donuts in a single horizontal strip
    n_cols = 4
    h_spacing = 0.04   # gap between donuts
    fig = make_subplots(
        rows=1, cols=n_cols,
        specs=[[{"type": "domain"}] * n_cols],
        horizontal_spacing=h_spacing,
    )

    positions = [(1, c) for c in range(1, n_cols + 1)]
    # Dynamically compute each column's centre x in paper space
    col_w = (1.0 - (n_cols - 1) * h_spacing) / n_cols
    centres = [
        ((c - 1) * (col_w + h_spacing) + col_w / 2, 0.5)
        for c in range(1, n_cols + 1)
    ]

    for (label, val, color), (row, col), (cx, cy) in zip(metrics, positions, centres):
        pct = (val * 100) if not pd.isna(val) else 0.0
        remainder = max(0.0, 100.0 - pct)
        txt = "n/a" if pd.isna(val) else f"{val:.1%}"

        fig.add_trace(
            go.Pie(
                labels=[label, ""],
                values=[pct, remainder],
                hole=0.62,
                marker=dict(
                    colors=[color, CHART_GRID],
                    line=dict(color="rgba(0,0,0,0)", width=0),
                ),
                textinfo="none",
                hovertemplate=f"%{{label}}: %{{value:.1f}}%<extra></extra>",
                showlegend=False,
                opacity=0.92,
            ),
            row=row, col=col,
        )

        # Value — large, bold, centred in the hole
        fig.add_annotation(
            text=f"<b style='font-size:18px'>{txt}</b>"
                 f"<br><span style='font-size:9px;color:#64748b'>{label}</span>",
            x=cx, y=0.5,
            xref="paper", yref="paper",
            xanchor="center", yanchor="middle",
            showarrow=False,
            font=dict(size=18, color="#f1f5f9",
                      family='system-ui, -apple-system, "Segoe UI", sans-serif'),
            align="center",
        )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=220,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        font=dict(family='system-ui, -apple-system, "Segoe UI", sans-serif', color="#94a3b8"),
    )
    return fig






def oee_modern(kpis: pd.DataFrame, target: float = 0.85) -> go.Figure:
    """Dark-canvas OEE time series with per-machine gradient fills and target line."""
    fig = go.Figure()

    for machine_id in sorted(kpis.machine_id.unique()):
        series = kpis[kpis.machine_id == machine_id].sort_values("bucket_start")
        hex_c = colour_for(machine_id)
        rgb   = rgba_for(machine_id)

        fig.add_trace(
            go.Scatter(
                x=series.bucket_start,
                y=series.oee,
                name=machine_id,
                mode="lines",
                line=dict(color=hex_c, width=2.5, shape="spline", smoothing=0.4),
                fill="tozeroy",
                fillcolor=f"rgba({rgb},0.10)",
                connectgaps=False,
                hovertemplate=f"<b>{machine_id}</b>: %{{y:.1%}}<extra></extra>",
            )
        )
        labelled = series.dropna(subset=["oee"])
        if not labelled.empty:
            fig.add_annotation(
                x=labelled.bucket_start.iloc[-1],
                y=labelled.oee.iloc[-1],
                text=f" {machine_id}",
                showarrow=False,
                xanchor="left",
                font=dict(color=hex_c, size=10,
                          family='system-ui, -apple-system, "Segoe UI", sans-serif'),
            )

    # B2 -- target reference line (shape, not trace -- stays out of legend/hover)
    fig.add_hline(
        y=target,
        line=dict(color=STATUS_CRITICAL, width=1.5, dash="dot"),
        annotation_text=f"Target {target:.0%}",
        annotation_position="right",
        annotation_font=dict(color=STATUS_CRITICAL, size=10),
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=220,
        margin=dict(l=8, r=90, t=8, b=8),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#1e2235",
            font_color="#e2e8f0",
            font_size=12,
            font_family='system-ui, -apple-system, "Segoe UI", sans-serif',
        ),
        font=dict(
            family='system-ui, -apple-system, "Segoe UI", sans-serif',
            color="#94a3b8",
        ),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, x=0,
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94a3b8", size=11),
        ),
    )
    fig.update_xaxes(
        showgrid=False, linecolor=CHART_AXIS, tickcolor=CHART_AXIS,
        tickfont=dict(color="#64748b", size=10),
    )
    fig.update_yaxes(
        tickformat=".0%", rangemode="tozero",
        gridcolor=CHART_GRID, zerolinecolor=CHART_AXIS,
        linecolor="rgba(0,0,0,0)",
        tickfont=dict(color="#64748b", size=10),
        title=dict(text="OEE", font=dict(color="#64748b", size=11)),
    )
    return fig


def worst_buckets_table(kpis: pd.DataFrame, n: int = 3) -> pd.DataFrame:
    """Return the n worst time-buckets (by OEE) and the limiting factor."""
    agg = (
        kpis.groupby("bucket_start", as_index=False)
        .agg(
            run_minutes=("run_minutes", "sum"),
            planned_minutes=("planned_minutes", "sum"),
            units_produced=("units_produced", "sum"),
            units_rejected=("units_rejected", "sum"),
        )
    )
    agg["availability"] = agg.run_minutes / agg.planned_minutes.replace(0, float("nan"))
    agg["performance"]  = (4.0 * agg.units_produced) / (
        (agg.run_minutes * 60).replace(0, float("nan"))
    )
    agg["quality"] = (agg.units_produced - agg.units_rejected) / agg.units_produced.replace(
        0, float("nan")
    )
    agg["oee"] = agg.availability * agg.performance * agg.quality

    factor_cols = ["availability", "performance", "quality"]
    agg = agg.dropna(subset=["oee"])
    if agg.empty:
        return pd.DataFrame(columns=["Bucket", "OEE", "Avail.", "Perf.", "Quality", "Limiting factor"])
    agg["drag"] = agg[factor_cols].apply(
        lambda row: row.idxmin() if row.notna().any() else "unknown", axis=1
    )
    worst = agg.nsmallest(n, "oee")[
        ["bucket_start", "oee", "availability", "performance", "quality", "drag"]
    ].copy()
    worst["bucket_start"] = worst.bucket_start.dt.strftime("%d %b %H:%M")
    worst = worst.rename(
        columns={
            "bucket_start": "Bucket",
            "oee": "OEE",
            "availability": "Avail.",
            "performance": "Perf.",
            "quality": "Quality",
            "drag": "Limiting factor",
        }
    )
    return worst.reset_index(drop=True)


def worst_bucket_bar(row: pd.Series) -> go.Figure:
    """Compact grouped bar for one worst-bucket: OEE, Avail, Perf, Quality."""
    factors = ["OEE", "Avail.", "Perf.", "Quality"]
    values  = [row.get(f, 0) for f in factors]
    values  = [v if not pd.isna(v) else 0.0 for v in values]
    colors  = ["#a78bfa", MACHINE_COLOUR["M-01"], MACHINE_COLOUR["M-02"], MACHINE_COLOUR["M-03"]]

    fig = go.Figure(
        go.Bar(
            x=factors,
            y=values,
            marker=dict(color=colors, opacity=0.88,
                        line=dict(color="rgba(255,255,255,0.1)", width=1)),
            text=[f"{v:.0%}" for v in values],
            textposition="outside",
            textfont=dict(size=10, color=INK_SECONDARY,
                          family='system-ui, -apple-system, "Segoe UI", sans-serif'),
            cliponaxis=False,
            hovertemplate="%{x}: %{y:.1%}<extra></extra>",
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=220,
        margin=dict(l=2, r=2, t=28, b=2),
        title=dict(
            text=f"<b>{row.get('Bucket', '')}</b>",
            font=dict(size=11, color="#94a3b8",
                      family='system-ui, -apple-system, "Segoe UI", sans-serif'),
            x=0.5,
        ),
        showlegend=False,
        yaxis=dict(
            tickformat=".0%", range=[0, 1.2],
            gridcolor=CHART_GRID, tickfont=dict(color="#64748b", size=9),
            zerolinecolor=CHART_AXIS, linecolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(
            tickfont=dict(color="#94a3b8", size=10,
                          family='system-ui, -apple-system, "Segoe UI", sans-serif'),
            showgrid=False, linecolor=CHART_AXIS,
        ),
        font=dict(family='system-ui, -apple-system, "Segoe UI", sans-serif', color="#94a3b8"),
    )
    return fig


def units_glass(kpis: pd.DataFrame) -> go.Figure:
    """Glassmorphism stacked bars: transparent fill, coloured border."""
    fig = go.Figure()

    n_buckets = kpis.bucket_start.nunique()
    bargap = max(0.05, 0.40 - 0.003 * n_buckets)

    for machine_id in sorted(kpis.machine_id.unique()):
        series = kpis[kpis.machine_id == machine_id].sort_values("bucket_start")
        rgb  = rgba_for(machine_id)
        good = series.units_produced - series.units_rejected

        fig.add_trace(
            go.Bar(
                x=series.bucket_start,
                y=good,
                name=machine_id,
                legendgroup=machine_id,
                legendgrouptitle_text=machine_id,
                marker=dict(
                    color=f"rgba({rgb},0.28)",
                    line=dict(color=f"rgba({rgb},0.85)", width=1.6),
                ),
                hovertemplate="%{y:,.0f}<extra>" + machine_id + " good</extra>",
            )
        )
        fig.add_trace(
            go.Bar(
                x=series.bucket_start,
                y=series.units_rejected,
                name=f"{machine_id} rej.",
                legendgroup=machine_id,
                marker=dict(
                    color="rgba(239,68,68,0.25)",
                    line=dict(color="rgba(239,68,68,0.75)", width=1.6),
                ),
                hovertemplate="%{y:,.0f}<extra>" + machine_id + " rej.</extra>",
            )
        )

    fig.update_layout(
        barmode="stack",
        bargap=bargap,
        height=248,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=8, r=8, t=8, b=8),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#1e2235", font_color="#e2e8f0", font_size=12),
        uniformtext_minsize=7,
        uniformtext_mode="hide",
        font=dict(family='system-ui, -apple-system, "Segoe UI", sans-serif', color="#94a3b8"),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.0, x=0,
            bgcolor="rgba(0,0,0,0)", groupclick="toggleitem",
            font=dict(size=10, color="#94a3b8"),
        ),
    )
    fig.update_xaxes(
        showgrid=False, linecolor=CHART_AXIS, tickcolor=CHART_AXIS,
        tickfont=dict(color="#64748b", size=9), tickangle=-30,
    )
    fig.update_yaxes(
        title=dict(text="Units", font=dict(color="#64748b", size=11)),
        gridcolor=CHART_GRID, zerolinecolor=CHART_AXIS,
        linecolor="rgba(0,0,0,0)", tickfont=dict(color="#64748b", size=9),
    )
    return fig


# --- page --------------------------------------------------------------------

st.set_page_config(
    page_title="FactoryFlow - Line A",
    page_icon="=",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Shrink Streamlit's default padding so everything fits on one screen.
st.markdown(
    """
    <style>
        /* Collapse top padding and remove footer whitespace */
        .block-container {
            padding-top: 0.6rem !important;
            padding-bottom: 0rem !important;
        }
        /* Tighter spacing between element blocks */
        div[data-testid="stVerticalBlock"] > div {
            gap: 0.25rem;
        }
        /* Slim horizontal rule */
        hr { margin: 0.3rem 0 !important; }
        /* Smaller h1 */
        h1 { font-size: 1.4rem !important; margin-bottom: 0 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# â”€â”€ Sidebar â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
with st.sidebar:
    st.markdown(
        "<b style='font-size:16px'>FactoryFlow</b>"
        "<div style='font-size:11px;color:#898781;margin-bottom:8px'>Line A Â· OEE</div>",
        unsafe_allow_html=True,
    )
    reachable, status_message = api_is_up()
    (st.success if reachable else st.error)(status_message)
    if not reachable:
        st.caption(f"Trying {API_BASE}. Is the API running?")
        st.stop()

    with st.expander("Data Settings", expanded=True):
        machine_ids = [m["machine_id"] for m in fetch("/machines")]
        chosen = st.multiselect("Machines", machine_ids, default=machine_ids)
        freq   = st.select_slider("Time bucket", options=["15min", "1h", "8h"], value="1h")
        window = st.date_input(
            "Period",
            value=(date(2026, 3, 1), date(2026, 3, 31)),
            format="YYYY-MM-DD",
        )

    with st.expander("Chart Settings", expanded=False):
        target_oee = st.slider(
            "Target OEE", 0.0, 1.0, 0.85, 0.05, format="%.0f%%",
            help="Red dotted reference line on the OEE chart.",
        )
        min_severity = st.slider(
            "Min anomaly severity", 0.0, 1.0, 0.5, 0.05,
            help="Raise until the list is short enough to act on.",
        )

    st.divider()
    freshness_slot = st.empty()  # B4 -- filled after kpis loads

if not chosen:
    st.info("Pick at least one machine.")
    st.stop()

start, end = (
    window if isinstance(window, tuple) and len(window) == 2
    else (window[0], window[0])
)

# â”€â”€ CORE 2 â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ about 15 minutes â”€â”€
#
# TODO(L1): call /metrics once per selected machine and concatenate
frames = [
    pd.DataFrame(
        fetch("/metrics", machine=m, freq=freq, **{"from": str(start), "to": str(end)})
    )
    for m in chosen
]
kpis = pd.concat([f for f in frames if not f.empty], ignore_index=True)

if kpis.empty:
    st.warning("No data in that window.")
    st.stop()

kpis["bucket_start"] = pd.to_datetime(kpis.bucket_start)

# B4 -- freshness
_newest   = kpis.bucket_start.max() + pd.Timedelta(minutes={"15min": 15, "1h": 60, "8h": 480}.get(freq, 60))
_age_min  = int((datetime.now(timezone.utc) - _newest.to_pydatetime().replace(tzinfo=timezone.utc)).total_seconds() / 60)
if _age_min < 0:
    freshness_slot.info(f"Historical â€” newest: {_newest.strftime('%d %b %H:%M')}")
elif _age_min < 60:
    freshness_slot.success(f"Fresh â€” {_age_min} min ago")
elif _age_min < 1440:
    _h, _m = divmod(_age_min, 60)
    freshness_slot.warning(f"Stale â€” {_h}h {_m}m ago")
else:
    freshness_slot.error(f"Old â€” {_age_min // 1440} day(s) ago")

# --- KPI computation (weighted -- never average ratios over unequal buckets) --
run_minutes     = kpis.run_minutes.sum()
planned_minutes = kpis.planned_minutes.sum()
produced        = kpis.units_produced.sum()
rejected        = kpis.units_rejected.sum()

availability = run_minutes / planned_minutes if planned_minutes else float("nan")
performance  = (4.0 * produced) / (run_minutes * 60) if run_minutes else float("nan")
quality      = (produced - rejected) / produced if produced else float("nan")
oee          = availability * performance * quality

# â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• 
# PAGE HEADER
# â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• 
st.title("Line A")

# Pre-resolve machine filter from session_state so top-right Output chart has kpis_vis
all_machines = sorted(kpis.machine_id.unique())
if "oee_pills" in st.session_state:
    _cur_vis = st.session_state["oee_pills"]
else:
    _cb_active = [m for m in all_machines if st.session_state.get(f"vis_{m}", True)]
    _cur_vis = _cb_active if any(f"vis_{m}" in st.session_state for m in all_machines) else all_machines

kpis_vis = kpis[kpis.machine_id.isin(_cur_vis)] if _cur_vis else kpis.head(0)

# ─────────────────────────────────────────────────────────────────────────────
# ROW 1 — OEE metric + 3 gauges | Output chart (top-right)
# ─────────────────────────────────────────────────────────────────────────────
c_left, c_output = st.columns([1, 1], gap="medium")

with c_left:
    st.plotly_chart(kpi_pie(availability, performance, quality), use_container_width=True)

with c_output:
    if kpis_vis.empty:
        st.info("Select at least one machine.")
    else:
        st.plotly_chart(units_glass(kpis_vis), use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# ROW 2 — Visible machines + OEE chart (bottom-left) | Worst buckets (bottom-right)
# ─────────────────────────────────────────────────────────────────────────────
c_oee, c_worst = st.columns([1, 1], gap="medium")

with c_oee:
    all_machines = sorted(kpis.machine_id.unique())
    try:
        visible = st.pills(
            "Visible machines",
            options=all_machines,
            selection_mode="multi",
            default=all_machines,
            key="oee_pills",
            label_visibility="collapsed",
        )
    except (AttributeError, TypeError):
        _tcols = st.columns(len(all_machines))
        visible = [
            m for m, tc in zip(all_machines, _tcols)
            if tc.checkbox(m, value=True, key=f"vis_{m}")
        ]

    kpis_vis = kpis[kpis.machine_id.isin(visible)] if visible else kpis.head(0)
    if kpis_vis.empty:
        st.info("Select at least one machine above.")
    else:
        st.plotly_chart(oee_modern(kpis_vis, target=target_oee), use_container_width=True)

with c_worst:
    st.markdown("<div style='height:36px'></div>", unsafe_allow_html=True)
    bottom3 = worst_buckets_table(kpis)
    if bottom3.empty:
        st.info("No data to rank.")
    else:
        # Three mini bar charts — no table, the charts carry all the info
        b_cols = st.columns(len(bottom3))
        for col, (_, row) in zip(b_cols, bottom3.iterrows()):
            with col:
                st.plotly_chart(worst_bucket_bar(row), use_container_width=True)


if hasattr(st, "dialog"):
    @st.dialog("Brainrot", width="large")
    def video_popup_dialog(src):
        st.video(src, loop=True, autoplay=True, muted=False)
else:
    def video_popup_dialog(src):
        st.video(src, loop=True, autoplay=True, muted=False)

# â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• 
# ROW 3 â€” Secondary info, both collapsed by default (no vertical space cost)
# â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• â• 
c_info, c_video = st.columns([1, 1], gap="medium")

with c_info:
    with st.expander("All data + download", expanded=False):
        _display = (
            kpis
            .sort_values(["machine_id", "bucket_start"])
            .assign(
                bucket_start=lambda df: df.bucket_start.dt.strftime("%d %b %H:%M"),
                oee=lambda df: df.oee.map(lambda v: f"{v:.1%}" if pd.notna(v) else "—"),
            )
        )
        st.dataframe(
            _display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "bucket_start":    st.column_config.TextColumn("Time"),
                "machine_id":      st.column_config.TextColumn("Machine"),
                "run_minutes":     st.column_config.NumberColumn("Run (min)",     format="%d"),
                "planned_minutes": st.column_config.NumberColumn("Planned (min)", format="%d"),
                "units_produced":  st.column_config.NumberColumn("Produced",      format="%d"),
                "units_rejected":  st.column_config.NumberColumn("Rejected",      format="%d"),
            },
        )
        # B5 -- download
        st.download_button(
            label="Download current selection as CSV",
            data=(
                kpis.sort_values(["machine_id", "bucket_start"])
                .to_csv(index=False)
                .encode("utf-8-sig")
            ),
            file_name=f"factoryflow_{start}_{end}_{freq}.csv",
            mime="text/csv",
            help="Downloads what is on screen: selected machines, period, bucket size.",
        )

    with st.expander("Anomaly log", expanded=False):
        st.caption(
            f"Min severity: {min_severity:.2f}  ·  "
            "A flag is a request for human inspection, not a fault report."
        )
        episodes = pd.DataFrame(fetch("/anomalies", min_severity=min_severity))
        episodes = (
            episodes[episodes.machine_id.isin(chosen)]
            if not episodes.empty else episodes
        )
        if episodes.empty:
            st.success(f"Nothing above severity {min_severity:.2f} in selected machines.")
        else:
            episodes = episodes.copy()
            episodes["band"] = [severity_band(v)[1] for v in episodes.severity]
            st.dataframe(
                episodes[["timestamp", "machine_id", "kind", "band", "value",
                           "duration_min", "severity"]],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "severity": st.column_config.ProgressColumn(
                        "severity", min_value=0.0, max_value=1.0, format="%.2f"
                    ),
                    "duration_min": st.column_config.NumberColumn("duration", format="%d min"),
                },
            )

with c_video:
    st.markdown(
        """
        <style>
        div[data-testid="stVideo"] {
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        }
        div[data-testid="stVideo"] video {
            max-height: 220px;
            width: 100%;
            object-fit: contain;
            background-color: #0b0f19;
            border-radius: 8px;
        }
        div[data-testid="stDialog"] div[data-testid="stVideo"] video {
            max-height: 75vh !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    dashboard_dir = Path(__file__).parent
    default_video = dashboard_dir / "Minecraft Parkour Gameplay No Copyright.mp4"
    if not default_video.exists():
        mp4s = list(dashboard_dir.glob("*.mp4"))
        if mp4s:
            default_video = mp4s[0]

    col_vtitle, col_vpop, col_vopt = st.columns([3, 1.2, 0.8], gap="small")
    with col_vtitle:
        st.markdown(
            "<div style='padding-top:6px;font-size:13px;font-weight:600;color:#94a3b8'>"
            "Brainrot <span style='font-size:10px;color:#22c55e;background:#14532d44;padding:2px 6px;border-radius:4px;margin-left:4px'>● LIVE</span>"
            "</div>",
            unsafe_allow_html=True,
        )

    with col_vopt:
        with st.popover("⚙️", help="Video kaynağını değiştir / Change source"):
            custom_file = st.file_uploader(
                "Upload video",
                type=["mp4", "webm", "mov", "avi", "mkv"],
                key="video_uploader",
            )
            custom_url = st.text_input(
                "Video URL / Path",
                placeholder="https://... or path",
                key="video_url_input",
            )

    video_to_play = None
    if custom_file is not None:
        video_to_play = custom_file
    elif custom_url and custom_url.strip():
        video_to_play = custom_url.strip()
    elif default_video.exists():
        video_to_play = str(default_video)

    with col_vpop:
        if st.button("⛶ Pop-up", key="btn_video_popup", help="Videoyu pop-up pencerede aç", use_container_width=True):
            if video_to_play:
                video_popup_dialog(video_to_play)

    if video_to_play:
        st.video(
            video_to_play,
            loop=True,
            autoplay=True,
            muted=True,
        )
    else:
        st.warning("Video not found in dashboard directory.")


# â•â• BONUS â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#
#   B1  THE SUPERVISOR'S ONE SCREEN. Delete everything that is not one of the
#       five numbers. No scrolling, no tabs, readable from two metres away.
#       This is the hardest one on the list and the best one to demo.
#
#   B2  DONE -- dotted red target line in the OEE chart.
#
#   B3  DONE -- compact table + 3 grouped bar charts.
#
#   B4  DONE -- sidebar freshness indicator, amber past an hour.
#
#   B5  DONE -- CSV download inside "All data" expander.
#
#   B6  SHOW IT TO ANOTHER PAIR. No explaining, no pointing. Ask them what
#       the line did last Tuesday and watch where they look first.
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

