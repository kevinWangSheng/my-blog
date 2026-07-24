"""OpenTelemetry tracing for the expense-agent: one span per LLM call, one span
per tool call, error spans exported immediately.

Attribute keys follow the OpenTelemetry GenAI semantic conventions (Experimental,
2026): gen_ai.operation.name, gen_ai.provider.name, gen_ai.request.model,
gen_ai.response.model, gen_ai.usage.input_tokens, gen_ai.usage.output_tokens,
gen_ai.response.finish_reasons, error.type. Span name for inference is
"{gen_ai.operation.name} {gen_ai.request.model}"; span kind is CLIENT.

Console exporter is wired by default so the file runs with no collector. Swap
ConsoleSpanExporter for an OTLPSpanExporter in production.

Error spans are flushed synchronously via a SimpleSpanProcessor so a crash
mid-loop still emits the error span before the process dies.
"""

from __future__ import annotations

import contextlib
from collections.abc import Iterator
from typing import Any

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from opentelemetry.trace import SpanKind, Status, StatusCode

_PROVIDER_NAME = "anthropic"  # gen_ai.provider.name value for the Claude API

_tracer: trace.Tracer | None = None


def init_tracing(service_name: str = "expense-agent") -> trace.Tracer:
    """Initialize the global tracer once. Idempotent.

    Two processors: a Batch processor for normal spans, and a Simple processor
    so error spans are exported synchronously (immediate export on a failing
    call, even if the loop then aborts).
    """
    global _tracer
    if _tracer is not None:
        return _tracer

    provider = TracerProvider()
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    # SimpleSpanProcessor exports on span end synchronously — used as the
    # immediate-export path for error spans (we also force_flush below).
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
    _tracer = trace.get_tracer(service_name)
    return _tracer


def _tracer_or_init() -> trace.Tracer:
    return _tracer if _tracer is not None else init_tracing()


def _flush_now() -> None:
    """Force synchronous export — guarantees an error span leaves the process."""
    provider = trace.get_tracer_provider()
    flush = getattr(provider, "force_flush", None)
    if callable(flush):
        flush()


@contextlib.contextmanager
def llm_span(model: str, operation: str = "chat") -> Iterator[Any]:
    """Span for one Claude API call.

    Usage:
        with llm_span("claude-opus-4-8") as span:
            resp = client.messages.create(...)
            record_llm_response(span, resp)
    On exception: error.type is set, status ERROR, and the span is flushed
    immediately before re-raising.
    """
    tracer = _tracer_or_init()
    # Span name per GenAI semconv: "{gen_ai.operation.name} {gen_ai.request.model}"
    with tracer.start_as_current_span(
        f"{operation} {model}", kind=SpanKind.CLIENT
    ) as span:
        span.set_attribute("gen_ai.operation.name", operation)
        span.set_attribute("gen_ai.provider.name", _PROVIDER_NAME)
        span.set_attribute("gen_ai.request.model", model)
        try:
            yield span
        except Exception as exc:
            span.set_attribute("error.type", type(exc).__qualname__)
            span.set_status(Status(StatusCode.ERROR, str(exc)))
            span.record_exception(exc)
            _flush_now()  # export the error span now, before the loop aborts
            raise


def record_llm_response(span: Any, response: Any) -> None:
    """Stamp usage + stop_reason from an Anthropic SDK Message onto the span.

    Reads response.usage.input_tokens / output_tokens / response.model /
    response.stop_reason (the Anthropic Message shape).
    """
    usage = getattr(response, "usage", None)
    if usage is not None:
        span.set_attribute("gen_ai.usage.input_tokens", int(usage.input_tokens))
        span.set_attribute("gen_ai.usage.output_tokens", int(usage.output_tokens))
    resp_model = getattr(response, "model", None)
    if resp_model:
        span.set_attribute("gen_ai.response.model", resp_model)
    stop_reason = getattr(response, "stop_reason", None)
    if stop_reason:
        # finish_reasons is an array per the convention
        span.set_attribute("gen_ai.response.finish_reasons", [stop_reason])


@contextlib.contextmanager
def tool_span(tool_name: str) -> Iterator[Any]:
    """Span for one tool execution (ocr_extract / fx_rate / post_ledger_entry).

    Uses gen_ai.operation.name = "execute_tool" and gen_ai.tool.name per the
    GenAI execute-tool span shape. On exception: error.type + status ERROR,
    flushed immediately.
    """
    tracer = _tracer_or_init()
    with tracer.start_as_current_span(
        f"execute_tool {tool_name}", kind=SpanKind.INTERNAL
    ) as span:
        span.set_attribute("gen_ai.operation.name", "execute_tool")
        span.set_attribute("gen_ai.tool.name", tool_name)
        try:
            yield span
        except Exception as exc:
            span.set_attribute("error.type", type(exc).__qualname__)
            span.set_status(Status(StatusCode.ERROR, str(exc)))
            span.record_exception(exc)
            _flush_now()
            raise
