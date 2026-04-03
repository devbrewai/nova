import json
from collections.abc import Iterator
from typing import Any

from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse

from app.config import settings
from app.models import ChatRequest
from app.services.chat_orchestrator import orchestrate_chat

router = APIRouter()

_RATE_LIMIT_MSG = (
    f"You've reached the demo limit ({settings.chat_rate_limit} messages/hour)."
)


def _get_client_ip(request: Request) -> str:
    """Extract real client IP, respecting X-Forwarded-For from Render proxy."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _event_stream(request: Request, chat_request: ChatRequest) -> Iterator[str]:
    """Generate SSE events from the chat orchestrator."""
    manager = request.app.state.conversation_manager
    conv_id, conversation = manager.get_or_create(chat_request.conversation_id)

    # Yield conversation_id as first event
    yield json.dumps({"type": "conversation_id", "id": conv_id})

    events: Iterator[dict[str, Any]] = orchestrate_chat(
        user_message=chat_request.message,
        conversation=conversation,
        anthropic_client=request.app.state.anthropic_client,
        openai_client=request.app.state.openai_client,
        collection=request.app.state.collection,
    )

    for event in events:
        yield json.dumps(event)


def _rate_limit_stream() -> Iterator[str]:
    """Single-event SSE stream returned when rate limit is exceeded."""
    yield json.dumps({"type": "error", "message": _RATE_LIMIT_MSG})


@router.post("/chat")
async def chat(request: Request, body: ChatRequest) -> EventSourceResponse:
    """Chat endpoint with SSE streaming."""
    ip = _get_client_ip(request)
    if not request.app.state.rate_limiter.is_allowed(ip):
        return EventSourceResponse(_rate_limit_stream())
    return EventSourceResponse(_event_stream(request, body))
