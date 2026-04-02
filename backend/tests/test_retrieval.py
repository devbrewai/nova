from unittest.mock import Mock, patch

from app.services.retrieval import retrieve


@patch("app.services.retrieval.search")
@patch("app.services.retrieval.embed_texts")
def test_retrieve_returns_filtered_results(
    mock_embed_texts: Mock, mock_search: Mock
) -> None:
    mock_embed_texts.return_value = [[0.1, 0.2, 0.3]]
    mock_search.return_value = {
        "documents": [["chunk one", "chunk two", "chunk three"]],
        "metadatas": [
            [{"source": "a.md"}, {"source": "b.md"}, {"source": "c.md"}],
        ],
        "distances": [[0.5, 1.2, 2.0]],
    }

    mock_client = Mock()
    mock_collection = Mock()

    results = retrieve("how do transfers work?", mock_client, mock_collection)

    mock_embed_texts.assert_called_once_with(
        texts=["how do transfers work?"], client=mock_client
    )
    mock_search.assert_called_once_with(
        mock_collection, query_vector=[0.1, 0.2, 0.3], n_results=3
    )

    # Only chunks with distance <= 1.5 (default threshold) should be returned
    assert len(results) == 2
    assert results[0]["text"] == "chunk one"
    assert results[0]["source"] == "a.md"
    assert results[0]["distance"] == 0.5
    assert results[1]["text"] == "chunk two"
    assert results[1]["distance"] == 1.2


@patch("app.services.retrieval.search")
@patch("app.services.retrieval.embed_texts")
def test_retrieve_with_custom_threshold(
    mock_embed_texts: Mock, mock_search: Mock
) -> None:
    mock_embed_texts.return_value = [[0.1, 0.2, 0.3]]
    mock_search.return_value = {
        "documents": [["close match", "far match"]],
        "metadatas": [[{"source": "a.md"}, {"source": "b.md"}]],
        "distances": [[0.3, 0.8]],
    }

    mock_client = Mock()
    mock_collection = Mock()

    results = retrieve("test query", mock_client, mock_collection, threshold=0.5)

    assert len(results) == 1
    assert results[0]["text"] == "close match"


@patch("app.services.retrieval.search")
@patch("app.services.retrieval.embed_texts")
def test_retrieve_empty_results(mock_embed_texts: Mock, mock_search: Mock) -> None:
    mock_embed_texts.return_value = [[0.1, 0.2, 0.3]]
    mock_search.return_value = {
        "documents": [[]],
        "metadatas": [[]],
        "distances": [[]],
    }

    mock_client = Mock()
    mock_collection = Mock()

    results = retrieve("no matches", mock_client, mock_collection)

    assert results == []
