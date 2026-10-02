from sentinel.trace.schema import SentinelTrace, SideEffect, ToolCall


def find_unapproved_irreversible_calls(trace: SentinelTrace) -> list[ToolCall]:
    violations = []
    for call in trace.tool_calls():
        if call.side_effect == SideEffect.IRREVERSIBLE and call.approved is not True:
            violations.append(call)
    return violations

def count_repeated_tool_calls(trace: SentinelTrace) -> dict[str, int]:
    counts = {}
    for call in trace.tool_calls():
        counts[call.name] = counts.get(call.name, 0) + 1
    return {name: n for name, n in counts.items() if n > 1}