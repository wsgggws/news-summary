from fastapi import Request, Response
from opentelemetry import trace
from opentelemetry.context import get_current
from opentelemetry.trace import format_trace_id
from starlette.middleware.base import BaseHTTPMiddleware


class TraceIDHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)

        span = trace.get_current_span(get_current())
        ctx = span.get_span_context()
        if ctx and ctx.trace_id != 0:
            trace_id = format_trace_id(ctx.trace_id)
            response.headers["x-trace-id"] = trace_id
        return response
