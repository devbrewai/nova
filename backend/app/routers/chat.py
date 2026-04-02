import json
from collections.abc import Iterator
from typing import Any

from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse

from app.models import ChatRequest
from app.services.chat_orchestrator import orchestrate_chat

router = APIRouter()


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


@router.post("/chat")
async def chat(request: Request, body: ChatRequest) -> EventSourceResponse:
    """Chat endpoint with SSE streaming."""
    return EventSourceResponse(_event_stream(request, body))
