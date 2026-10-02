"""Lesson 1, Part B spec: your first detectors.

Run with:  pytest tests/test_lesson1b_detectors.py -v
"""

import json
from pathlib import Path

import pytest

from sentinel.trace.schema import SentinelTrace

FIXTURE = Path(__file__).parent / "fixtures" / "payout_without_approval.json"


@pytest.fixture
def trace() -> SentinelTrace:
    return SentinelTrace.model_validate(json.loads(FIXTURE.read_text()))


# --- Part B: your first detector -----------------------------------------------

def test_detects_unapproved_payout(trace):
    from sentinel.detectors.approval import find_unapproved_irreversible_calls

    flagged = find_unapproved_irreversible_calls(trace)
    assert [c.name for c in flagged] == ["issue_payout"]


def test_approved_payout_is_not_flagged(trace):
    from sentinel.detectors.approval import find_unapproved_irreversible_calls

    trace.spans[6].tool.approved = True
    assert find_unapproved_irreversible_calls(trace) == []


# --- Part C: YOUR TURN --------------------------------------------------------

def test_exercise_count_repeated_tool_calls(trace):
    from sentinel.detectors.approval import count_repeated_tool_calls

    assert count_repeated_tool_calls(trace) == {"get_claim": 2}
