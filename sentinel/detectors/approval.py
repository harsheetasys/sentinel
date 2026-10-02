from sentinel.trace.schema import SentinelTrace, SideEffect, ToolCall


def find_unapproved_irreversible_calls(trace: SentinelTrace) -> list[ToolCall]:
    violations = []
    for call in trace.tool_calls():
        if call.side_effect == SideEffect.IRREVERSIBLE and call.approved is not True:
            violations.append(call)
    return violations