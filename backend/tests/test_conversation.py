import time
from unittest.mock import patch

from app.services.conversation import (
    MAX_MESSAGES,
    TTL_SECONDS,
    Conversation,
    ConversationManager,
)


def test_add_message_appends() -> None:
    conv = Conversation()
    conv.add_message("user", "hello")
    conv.add_message("assistant", "hi there")

    messages = conv.get_messages()
    assert len(messages) == 2
    assert messages[0] == {"role": "user", "content": "hello"}
    assert messages[1] == {"role": "assistant", "content": "hi there"}


def test_sliding_window_trims_to_max() -> None:
    conv = Conversation()
    for i in range(MAX_MESSAGES + 5):
        conv.add_message("user", f"msg {i}")

    messages = conv.get_messages()
    assert len(messages) == MAX_MESSAGES
    assert messages[0]["content"] == "msg 5"
    assert messages[-1]["content"] == f"msg {MAX_MESSAGES + 4}"


def test_is_expired_false_when_fresh() -> None:
    conv = Conversation()
    assert not conv.is_expired()


def test_is_expired_true_after_ttl() -> None:
    conv = Conversation()
    with patch.object(time, "time", return_value=conv.last_active + TTL_SECONDS + 1):
        assert conv.is_expired()


def test_get_or_create_returns_new() -> None:
    manager = ConversationManager()
    cid, conv = manager.get_or_create()

    assert cid is not None
    assert isinstance(conv, Conversation)
    assert conv.get_messages() == []


def test_get_or_create_returns_existing() -> None:
    manager = ConversationManager()
    cid, conv = manager.get_or_create()
    conv.add_message("user", "hello")

    cid2, conv2 = manager.get_or_create(cid)
    assert cid2 == cid
    assert len(conv2.get_messages()) == 1


def test_get_or_create_replaces_expired() -> None:
    manager = ConversationManager()
    cid, conv = manager.get_or_create("test-id")
    conv.add_message("user", "old message")

    with patch.object(time, "time", return_value=conv.last_active + TTL_SECONDS + 1):
        cid2, conv2 = manager.get_or_create("test-id")

    assert cid2 == "test-id"
    assert conv2.get_messages() == []


def test_cleanup_removes_expired() -> None:
    manager = ConversationManager()
    cid, conv = manager.get_or_create("old")
    conv.add_message("user", "stale")

    with patch.object(time, "time", return_value=conv.last_active + TTL_SECONDS + 1):
        manager.get_or_create("new")

    assert "old" not in manager._conversations
    assert "new" in manager._conversations
