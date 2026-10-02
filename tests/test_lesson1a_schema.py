"""Lesson 1, Part A spec: the trace schema.

Run with:  pytest tests/test_lesson1a_schema.py -v
All green means Part A is done.
"""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from sentinel.trace.schema import Operation, SentinelTrace, SideEffect, Span

FIXTURE = Path(__file__).parent / "fixtures" / "payout_without_approval.json"


@pytest.fixture
def trace() -> SentinelTrace:
    return SentinelTrace.model_validate(json.loads(FIXTURE.read_text()))


# --- Part A: the schema -------------------------------------------------------

def test_fixture_loads(trace):
    assert trace.trace_id == "tr_0001"
    assert trace.target.framework == "openai-agents"
    assert len(trace.spans) == 8


def test_strings_become_enums(trace):
    # Pydantic turns the JSON string "execute_tool" into Operation.EXECUTE_TOOL
    assert trace.spans[2].operation is Operation.EXECUTE_TOOL
    assert trace.spans[6].tool.side_effect is SideEffect.IRREVERSIBLE


def test_tool_calls_in_order(trace):
    names = [c.name for c in trace.tool_calls()]
    assert names == ["get_claim", "get_claim", "issue_payout"]


def test_total_usage(trace):
    usage = trace.total_usage()
    assert usage.input_tokens == 812 + 1104 + 1190
    assert usage.output_tokens == 41 + 37 + 28


def test_duration_ms(trace):
    assert trace.spans[0].duration_ms == pytest.approx(6400)


def test_tool_span_without_tool_is_rejected():
    with pytest.raises(ValidationError):
        Span(
            span_id="bad",
            operation="execute_tool",
            name="execute_tool mystery",
            start_time="2026-10-02T10:00:00Z",
        )


def test_round_trip_json(trace):
    again = SentinelTrace.model_validate_json(trace.model_dump_json())
    assert again == trace
