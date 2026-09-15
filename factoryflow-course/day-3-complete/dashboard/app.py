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
from datetime import date

import httpx
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

API_BASE = os.environ.get("FACTORYFLOW_API", "http://localhost:8000")
REQUEST_TIMEOUT_S = 30.0


# Because then the OEE formula would exist in two places, and the day one of
# them changes is the day the dashboard and the report disagree in front of the
# supervisor. Going through the API keeps exactly one definition of the number.
# The price is honest: two processes to start instead of one, and a dashboard
# that shows an error when the API is down -- which is better than a dashboard
# that shows a plausible wrong number.

# --- palette -------------------------------------------------------------
# Validated as a categorical set against this surface. One fixed colour per
# machine, assigned by identity: filtering M-02 out must not repaint M-03.

SURFACE = "#fcfcfb"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
INK_MUTED = "#898781"
INK_SECONDARY = "#52514e"

MACHINE_COLOUR = {"M-01": "#2a78d6", "M-02": "#eb6834", "M-03": "#1baf7a"}
FALLBACK_COLOUR = "#4a3aa7"

# Reserved for state, never for a series.
STATUS_GOOD = "#0ca30c"
STATUS_WARNING = "#fab219"
STATUS_SERIOUS = "#ec835a"
STATUS_CRITICAL = "#d03b3b"

GOOD_UNITS_COLOUR = "#9ec5f4"
REJECT_COLOUR = STATUS_CRITICAL


def colour_for(machine_id: str) -> str:
    return MACHINE_COLOUR.get(machine_id, FALLBACK_COLOUR)


def severity_band(severity: float) -> tuple[str, str]:
    """Map a severity to a reserved status colour and a word.

    The word is not decoration. A status colour never carries meaning on its
    own -- roughly one reader in twelve cannot separate these four hues.
    """
    if severity >= 0.75:
        return STATUS_CRITICAL, "critical"
    if severity >= 0.5:
        return STATUS_SERIOUS, "serious"
    if severity >= 0.25:
        return STATUS_WARNING, "warning"
    return STATUS_GOOD, "minor"


# --- data ----------------------------------------------------------------


@st.cache_data(ttl=60, show_spinner=False)
def fetch(path: str, **params) -> list[dict]:
    """GET a route on the API and hand back its JSON.

    Cached for a minute: a supervisor changing the machine filter should not
    make the service re-read a month of data every click.
    """
    response = httpx.get(f"{API_BASE}{path}", params=params, timeout=REQUEST_TIMEOUT_S)
    response.raise_for_status()
    return response.json()


def api_is_up() -> tuple[bool, str]:
    try:
        health = fetch("/health")
    except httpx.HTTPError as error:
        return False, f"{type(error).__name__}: {error}"
    if not health.get("rows_loaded"):
        return False, "The API is running but loaded 0 rows. Check where it is looking for the CSV."
    return True, f"{health['rows_loaded']:,} readings loaded"


# --- charts --------------------------------------------------------------


def _style(figure: go.Figure, y_title: str) -> go.Figure:
    """Recessive chrome. The data is the only thing with contrast."""
    figure.update_layout(
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        margin=dict(l=8, r=96, t=8, b=8),
        height=340,
        hovermode="x unified",
        font=dict(family='system-ui, -apple-system, "Segoe UI", sans-serif', color=INK_SECONDARY),
        legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0, bgcolor="rgba(0,0,0,0)"),
    )
    figure.update_xaxes(showgrid=False, linecolor=AXIS, tickcolor=AXIS, tickfont_color=INK_MUTED)
    figure.update_yaxes(
        title=dict(text=y_title, font=dict(color=INK_MUTED, size=12)),
        gridcolor=GRID,
        zerolinecolor=AXIS,
        linecolor="rgba(0,0,0,0)",
        tickfont_color=INK_MUTED,
    )
    return figure


def oee_over_time(kpis: pd.DataFrame) -> go.Figure:
    """One line per machine. Identity is carried by colour, legend AND end label."""
    figure = go.Figure()
    for machine_id in sorted(kpis.machine_id.unique()):
        series = kpis[kpis.machine_id == machine_id].sort_values("bucket_start")
        colour = colour_for(machine_id)
        figure.add_trace(
            go.Scatter(
                x=series.bucket_start,
                y=series.oee,
                name=machine_id,
                mode="lines",
                line=dict(color=colour, width=2),
                connectgaps=False,  # a gap is missing data, not a straight line
                hovertemplate="%{y:.1%}<extra>" + machine_id + "</extra>",
            )
        )
        labelled = series.dropna(subset=["oee"])
        if not labelled.empty:
            figure.add_annotation(
                x=labelled.bucket_start.iloc[-1],
                y=labelled.oee.iloc[-1],
                text=f" {machine_id}",
                showarrow=False,
                xanchor="left",
                font=dict(color=INK_SECONDARY, size=12),
            )

    figure.update_yaxes(tickformat=".0%", rangemode="tozero")
    return _style(figure, "OEE")


def units_per_bucket(kpis: pd.DataFrame) -> go.Figure:
    """Good vs rejected units. Two parts of one whole, so: stacked, not grouped."""
    totals = (
        kpis.groupby("bucket_start", as_index=False)[["units_produced", "units_rejected"]]
        .sum()
        .sort_values("bucket_start")
    )
    good = totals.units_produced - totals.units_rejected

    figure = go.Figure()
    for name, values, colour in (
        ("Good units", good, GOOD_UNITS_COLOUR),
        ("Rejected", totals.units_rejected, REJECT_COLOUR),
    ):
        figure.add_trace(
            go.Bar(
                x=totals.bucket_start,
                y=values,
                name=name,
                marker=dict(color=colour, line=dict(color=SURFACE, width=2)),
                hovertemplate="%{y:,.0f}<extra>" + name + "</extra>",
            )
        )

    figure.update_layout(barmode="stack", bargap=0.15)
    return _style(figure, "Units")


# --- page ----------------------------------------------------------------

st.set_page_config(page_title="FactoryFlow - Line A", page_icon="=", layout="wide")

st.title("Line A")
st.caption("Overall Equipment Effectiveness, from the machine controllers.")

with st.sidebar:
    st.subheader("Filters")
    reachable, status_message = api_is_up()
    (st.success if reachable else st.error)(status_message)
    if not reachable:
        st.caption(f"Trying {API_BASE}. Is the API running?")
        st.stop()

    machine_ids = [machine["machine_id"] for machine in fetch("/machines")]
    chosen = st.multiselect("Machines", machine_ids, default=machine_ids)
    freq = st.select_slider("Time bucket", options=["15min", "1h", "8h"], value="1h")
    window = st.date_input(
        "Period", value=(date(2026, 3, 1), date(2026, 3, 31)), format="YYYY-MM-DD"
    )
    min_severity = st.slider(
        "Minimum anomaly severity",
        0.0,
        1.0,
        0.5,
        0.05,
        help="Raise this until the list is short enough to act on.",
    )

if not chosen:
    st.info("Pick at least one machine.")
    st.stop()

start, end = window if isinstance(window, tuple) and len(window) == 2 else (window[0], window[0])

frames = [
    pd.DataFrame(
        fetch("/metrics", machine=machine_id, freq=freq, **{"from": str(start), "to": str(end)})
    )
    for machine_id in chosen
]
kpis = pd.concat([frame for frame in frames if not frame.empty], ignore_index=True)

if kpis.empty:
    st.warning("No data in that window.")
    st.stop()

kpis["bucket_start"] = pd.to_datetime(kpis.bucket_start)

# --- headline numbers ----------------------------------------------------
# Four stat tiles, not four charts: a single number does not need axes.
# Weighted by minutes and units, never a mean of ratios -- averaging
# percentages over unequal buckets is how a report starts lying quietly.

run_minutes = kpis.run_minutes.sum()
planned_minutes = kpis.planned_minutes.sum()
produced = kpis.units_produced.sum()
rejected = kpis.units_rejected.sum()

availability = run_minutes / planned_minutes if planned_minutes else float("nan")
performance = (4.0 * produced) / (run_minutes * 60) if run_minutes else float("nan")
quality = (produced - rejected) / produced if produced else float("nan")

for column, (label, value, note) in zip(
    st.columns(4),
    [
        ("OEE", availability * performance * quality, "availability x performance x quality"),
        ("Availability", availability, f"{run_minutes:,.0f} of {planned_minutes:,.0f} planned min"),
        ("Performance", performance, f"{produced:,.0f} units"),
        ("Quality", quality, f"{rejected:,.0f} rejected"),
    ],
    strict=True,
):
    column.metric(label, "n/a" if pd.isna(value) else f"{value:.1%}", help=note)
    column.caption(note)

st.subheader("OEE over time")
st.plotly_chart(oee_over_time(kpis), width="stretch")

st.subheader("Output")
st.plotly_chart(units_per_bucket(kpis), width="stretch")

# The table view is not a fallback. It is how anyone who cannot separate three
# hues -- or who needs the exact number -- reads this page.
with st.expander("Show the numbers"):
    st.dataframe(
        kpis.sort_values(["machine_id", "bucket_start"]),
        width="stretch",
        hide_index=True,
    )

# --- anomalies -----------------------------------------------------------

st.subheader("Worth a look")
episodes = pd.DataFrame(fetch("/anomalies", min_severity=min_severity))
episodes = episodes[episodes.machine_id.isin(chosen)] if not episodes.empty else episodes

if episodes.empty:
    st.success(f"Nothing above severity {min_severity:.2f} in the selected machines.")
else:
    st.caption(f"{len(episodes)} episodes. A flag is a request for a human to look, not a fault.")
    episodes = episodes.copy()
    episodes["band"] = [severity_band(value)[1] for value in episodes.severity]
    st.dataframe(
        episodes[["timestamp", "machine_id", "kind", "band", "value", "duration_min", "severity"]],
        width="stretch",
        hide_index=True,
        column_config={
            "severity": st.column_config.ProgressColumn(
                "severity", min_value=0.0, max_value=1.0, format="%.2f"
            ),
            "duration_min": st.column_config.NumberColumn("duration", format="%d min"),
        },
    )

