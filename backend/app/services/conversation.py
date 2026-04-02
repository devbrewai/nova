import time
import uuid
from typing import TypedDict

MAX_MESSAGES = 20
TTL_SECONDS = 30 * 60  # 30 minutes


class Message(TypedDict):
    role: str
    content: str


class Conversation:
    """Single conversation with sliding window and TTL."""

    def __init__(self) -> None:
        self.messages: list[Message] = []
        self.last_active: float = time.time()

    def add_message(self, role: str, content: str) -> None:
        """Append a message and enforce the sliding window."""
        self.messages.append(Message(role=role, content=content))
        if len(self.messages) > MAX_MESSAGES:
            self.messages = self.messages[-MAX_MESSAGES:]
        self.last_active = time.time()

    def get_messages(self) -> list[Message]:
        """Return the current message history."""
        return list(self.messages)

    def is_expired(self) -> bool:
        """Check if this conversation has exceeded the TTL."""
        return (time.time() - self.last_active) > TTL_SECONDS


class ConversationManager:
    """Manages multiple conversations by ID with lazy cleanup."""

    def __init__(self) -> None:
        self._conversations: dict[str, Conversation] = {}

    def get_or_create(
        self, conversation_id: str | None = None
    ) -> tuple[str, Conversation]:
        """Return existing conversation or create a new one.

        Triggers lazy cleanup of expired conversations.
        """
        self._cleanup_expired()

        if conversation_id and conversation_id in self._conversations:
            conv = self._conversations[conversation_id]
            if not conv.is_expired():
                return conversation_id, conv

        new_id = conversation_id or str(uuid.uuid4())
        conv = Conversation()
        self._conversations[new_id] = conv
        return new_id, conv

    def _cleanup_expired(self) -> None:
        """Remove expired conversations."""
        expired = [
            cid for cid, conv in self._conversations.items() if conv.is_expired()
        ]
        for cid in expired:
            del self._conversations[cid]
