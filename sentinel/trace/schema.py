from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field, model_validator

class Operation(str, Enum):
    INVOKE_AGENT= "invoke_agent"
    CHAT="chat"
    EXECUTE_TOOL="execute_tool"
    RETRIEVAL="retrieval"

class SideEffect(str, Enum):
    READ_ONLY="read_only"
    REVERSIBLE="reversible"
    IRREVERSIBLE="irreversible"

class TokenUsage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0

class ToolCall(BaseModel):
    name: str
    call_id: str | None = None
    arguments: dict[str, Any] = Field(default_factory=dict)
    result: Any = None
    side_effect: SideEffect = SideEffect.READ_ONLY
    approved: bool | None = None

class RetrievedChunk(BaseModel):
    doc_id: str
    text: str
    score: float | None = None
    trusted: bool = True


class Span(BaseModel):
    span_id: str
    parent_id: str | None = None
    operation: Operation
    name: str
    start_time: datetime
    end_time: datetime | None = None
    agent_name: str | None = None
    model: str | None = None
    usage: TokenUsage | None = None
    tool: ToolCall | None = None
    chunks: list[RetrievedChunk] = Field(default_factory=list)
    error: str | None = None

    @model_validator(mode="after")
    def tool_spans_need_a_tool(self) -> "Span":
        if self.operation == Operation.EXECUTE_TOOL and self.tool is None:
            raise ValueError("an execute_tool span must include `tool`")
        return self

    @property
    def duration_ms(self) -> float | None:
        if self.end_time is None:
            return None
        return (self.end_time - self.start_time).total_seconds() * 1000


class Target(BaseModel):
    agent_name: str
    framework: str
    model: str
    provider: str = "gemini"


class SentinelTrace(BaseModel):
    schema_version: str = "0.1"
    trace_id: str
    target: Target
    user_input: str
    final_output: str | None = None
    probe_id: str | None = None
    spans: list[Span] = Field(default_factory=list)

    def tool_calls(self) -> list[ToolCall]:
        return [s.tool for s in self.spans if s.tool is not None]

    def total_usage(self) -> TokenUsage:
        total = TokenUsage()
        for s in self.spans:
            if s.usage:
                total.input_tokens += s.usage.input_tokens
                total.output_tokens += s.usage.output_tokens
        return total