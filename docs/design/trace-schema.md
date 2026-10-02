# Design doc: Sentinel trace schema

_Author: Dhanshree · Status: draft · Fill this in after Lesson 2. Write it in your own words: this is the document you will walk an interviewer through._

## 1. Problem
<!-- Why can't Sentinel judge an agent from its final answer alone? Use the
     payout_without_approval example. -->

## 2. Goals and non-goals
<!-- Goals: framework-agnostic, enough detail for every detector, ...
     Non-goals: replacing a full observability platform, ... -->

## 3. Why OpenTelemetry GenAI conventions instead of a custom format
<!-- Which frameworks emit OTel natively (ADK) and which don't (OpenAI Agents SDK)?
     What does that buy us (auditing agents we didn't build, exporting to Langfuse/Phoenix)?
     What is the risk? (Hint: the conventions are still at "Development" stability.) -->

## 4. The schema
<!-- SentinelTrace -> Span -> ToolCall / RetrievedChunk. One line per field that matters. -->

## 5. Sentinel-specific extensions beyond OTel
<!-- side_effect (from MCP tool annotations), approved, chunk.trusted (provenance).
     For each: which detector needs it and which OWASP risk it helps catch. -->

## 6. Privacy
<!-- OTel keeps prompt/response content OUT of span attributes by default. Why?
     What do we do with customer data in traces? -->

## 7. Open questions
-
