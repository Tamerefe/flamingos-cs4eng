"""Tests for the four metric functions.

A test is not there to prove the code works. It is there to pin down behaviour
so that the next person -- including you, in March -- cannot change it by
accident. Every test below corresponds to a decision somebody made.
"""

from __future__ import annotations

import math

import pandas as pd
import pytest

from factoryflow import metrics



def test_availability_ignores_setup(sample_readings: pd.DataFrame) -> None:
    """SETUP is not held against the machine, so it leaves planned time.

    Six run minutes out of nine planned. If this comes out as 0.6, the SETUP
    minute is being counted as planned production time -- which is a defensible
    model, but not this one, and every downstream number moves with it.
    """
    assert metrics.availability(sample_readings) == pytest.approx(2 / 3)


def test_performance_uses_run_time_not_wall_clock(sample_readings: pd.DataFrame) -> None:
    """A machine is only judged on output while it was actually running."""
    assert metrics.performance(sample_readings, ideal_cycle_time_s=4.0) == pytest.approx(2 / 3)


def test_quality_counts_good_units(sample_readings: pd.DataFrame) -> None:
    assert metrics.quality(sample_readings) == pytest.approx(0.9)


def test_oee_is_the_product_of_the_three(sample_readings: pd.DataFrame) -> None:
    assert metrics.oee(sample_readings, ideal_cycle_time_s=4.0) == pytest.approx(0.4)


def test_quality_on_empty_bucket(idle_readings: pd.DataFrame) -> None:
    """Quality of nothing is unknown -- not zero, not infinity.

    This is the bug that put `inf` in a shift report. Dividing by a zero unit
    count gives infinity in floating point, and infinity times anything is still
    infinity, so a single idle night shift poisoned the monthly OEE.
    """
    result = metrics.quality(idle_readings)
    assert math.isnan(result), f"expected NaN for a bucket with no units, got {result}"
    assert not math.isinf(result)


def test_metrics_are_undefined_when_the_machine_never_ran(idle_readings: pd.DataFrame) -> None:
    """No run time means no performance figure, and NaN must propagate into OEE."""
    assert math.isnan(metrics.performance(idle_readings))
    assert math.isnan(metrics.oee(idle_readings))
    # Availability is still defined: the machine was available to run and did not.
    assert metrics.availability(idle_readings) == pytest.approx(0.0)


def test_availability_is_undefined_without_planned_time(sample_readings: pd.DataFrame) -> None:
    """A bucket that was entirely changeover has no planned production time."""
    all_setup = sample_readings.assign(machine_state="SETUP")
    assert math.isnan(metrics.availability(all_setup))


@pytest.mark.parametrize(
    ("rejected", "expected"),
    [(0, 1.0), (6, 0.9), (30, 0.5), (60, 0.0)],
)
def test_quality_across_reject_rates(
    sample_readings: pd.DataFrame, rejected: int, expected: float
) -> None:
    """Quality falls linearly with rejects and reaches exactly 0 and 1 at the ends."""
    readings = sample_readings.copy()
    readings.loc[readings.machine_state == "RUN", "units_rejected"] = rejected // 6
    assert metrics.quality(readings) == pytest.approx(expected)


# Both, and the distinction is what it is for. It proves nothing about whether
# the formulas are right -- it only proves they still produce what they produced
# yesterday. That makes it useless as a specification and valuable as an alarm:
# refactor the pipeline, and this is the test that notices you changed the
# answer. It is fragile on purpose, and it is only allowed to exist because the
# tests above it pin the actual behaviour on data you can check by hand.


def test_quality_never_exceeds_one_on_clean_data(real_readings: pd.DataFrame) -> None:
    """The 104 % bug, pinned down.

    The raw export contains rows where more units were rejected than produced.
    Cleaning caps them. If this ever fails, either cleaning regressed or someone
    fed the metrics raw data.
    """
    for machine_id, group in real_readings.groupby("machine_id"):
        value = metrics.quality(group)
        assert 0.0 <= value <= 1.0, f"{machine_id} reported quality {value:.4f}"


def test_march_numbers_are_stable(real_readings: pd.DataFrame) -> None:
    """Regression guard against the known-good March figures.

    These come from facilitator/ground_truth.json, block `expected_after_cleaning`.
    Regenerating the dataset with a different seed will break this test on
    purpose -- the numbers are only meaningful for this exact export.
    """
    expected = {
        "M-01": 0.7032,
        "M-02": 0.6723,
        "M-03": 0.6853,
    }
    for machine_id, group in real_readings.groupby("machine_id"):
        assert metrics.oee(group) == pytest.approx(expected[machine_id], abs=5e-5)


