from unittest.mock import Mock, patch

from app.services.retrieval import retrieve


@patch("app.services.retrieval.search")
@patch("app.services.retrieval.embed_texts")
def test_retrieve(mock_embed_texts: Mock, mock_search: Mock) -> None:
    mock_embed_texts.return_value = [[0.1, 0.2, 0.3]]
    mock_search.return_value = {"documents": [["chunk one"]]}

    mock_client = Mock()
    mock_collection = Mock()

    retrieve("how do transfers work?", mock_client, mock_collection, 3)

    mock_embed_texts.assert_called_once_with(
        texts=["how do transfers work?"], client=mock_client
    )

    mock_search.assert_called_once_with(
        mock_collection, query_vector=[0.1, 0.2, 0.3], n_results=3
    )
