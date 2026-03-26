from unittest.mock import Mock

from app.services.embedding import embed_texts


def test_embed_chunks_extract_text() -> None:
    chunks = [
        {
            "id": "doc-000",
            "text": "first chunk",
            "source": "doc.md",
            "category": "doc",
            "chunk_index": 0,
        },
        {
            "id": "doc-001",
            "text": "second chunk",
            "source": "doc.md",
            "category": "doc",
            "chunk_index": 1,
        },
    ]
    texts = [chunk["text"] for chunk in chunks]
    assert texts == ["first chunk", "second chunk"]


def test_embed_texts_with_mock() -> None:

    mock_client = Mock()

    fake_embedding_1 = Mock()
    fake_embedding_1.embedding = [0.1, 0.2, 0.3]

    fake_embedding_2 = Mock()
    fake_embedding_2.embedding = [0.4, 0.5, 0.6]

    mock_response = Mock()
    mock_response.data = [fake_embedding_1, fake_embedding_2]
    mock_client.embeddings.create.return_value = mock_response

    result = embed_texts(["text one", "text two"], mock_client)

    assert result == [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
