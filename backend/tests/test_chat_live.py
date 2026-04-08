"""Live Anthropic API tests for emoji stripping.

These tests hit the real Claude API and validate that the prompt rule plus
runtime strip safety net keep emojis out of streamed responses end-to-end.

Skipped by default. Run explicitly with:
    ANTHROPIC_API_KEY=... uv run pytest -m live -v
"""

import json
from collections.abc import Iterator
from contextlib import asynccontextmanager
from datetime import timedelta
from unittest.mock import Mock, patch

import anthropic
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.config import settings
from app.services.chat_orchestrator import orchestrate_chat
from app.services.conversation import Conversation, ConversationManager
from app.services.rate_limiter import RateLimiter
from app.services.text import strip_emojis

pytestmark = pytest.mark.live


PROMPTS = [
    "I just opened my new account today, I'm so excited! Welcome me!",
    "hey what's up",
    "thanks so much, you're a lifesaver!",
]


@pytest.fixture(scope="module")
def anthropic_client() -> anthropic.Anthropic:
    if not settings.anthropic_api_key:
        pytest.skip("ANTHROPIC_API_KEY not set")
    from app.services.llm import get_anthropic_client

    return get_anthropic_client()


# --- Layer 1: orchestrator-level ---


def _collect_orchestrator_text(
    prompt: str, anthropic_client: anthropic.Anthropic
) -> str:
    with patch("app.services.chat_orchestrator.retrieve", return_value=[]):
        events = list(
            orchestrate_chat(
                user_message=prompt,
                conversation=Conversation(),
                anthropic_client=anthropic_client,
                openai_client=Mock(),
                collection=Mock(),
            )
        )
    return "".join(e["content"] for e in events if e["type"] == "text_delta")


@pytest.mark.parametrize("prompt", PROMPTS)
def test_live_orchestrator_response_has_no_emojis(
    anthropic_client: anthropic.Anthropic, prompt: str
) -> None:
    text = _collect_orchestrator_text(prompt, anthropic_client)
    assert text, "expected non-empty response"
    assert strip_emojis(text) == text, f"emoji leaked: {text!r}"


# --- Layer 2: full HTTP /api/chat endpoint ---


@pytest.fixture()
def live_client(
    anthropic_client: anthropic.Anthropic,
) -> Iterator[TestClient]:
    """TestClient with REAL Anthropic, mocked OpenAI/Chroma + RAG."""

    @asynccontextmanager
    async def live_lifespan(app: FastAPI):  # type: ignore[no-untyped-def]
        app.state.openai_client = Mock()
        app.state.collection = Mock()
        app.state.anthropic_client = anthropic_client
        app.state.conversation_manager = ConversationManager()
        app.state.rate_limiter = RateLimiter(limit=100, window=timedelta(hours=1))
        yield

    from app.main import app

    app.router.lifespan_context = live_lifespan
    with (
        patch("app.services.chat_orchestrator.retrieve", return_value=[]),
        TestClient(app) as client,
    ):
        yield client


def _collect_endpoint_text(client: TestClient, prompt: str) -> str:
    """POST /api/chat, parse SSE stream, return concatenated text deltas."""
    with client.stream("POST", "/api/chat", json={"message": prompt}) as response:
        assert response.status_code == 200
        chunks: list[str] = []
        for line in response.iter_lines():
            if not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if not payload:
                continue
            event = json.loads(payload)
            if event.get("type") == "text_delta":
                chunks.append(event.get("content", ""))
    return "".join(chunks)


@pytest.mark.parametrize("prompt", PROMPTS)
def test_live_chat_endpoint_response_has_no_emojis(
    live_client: TestClient, prompt: str
) -> None:
    text = _collect_endpoint_text(live_client, prompt)
    assert text, "expected non-empty response from /api/chat"
    assert strip_emojis(text) == text, f"emoji leaked from endpoint: {text!r}"
