from app.services.knowledge_base import load_documents


def test_load_documents_returns_list() -> None:
    docs = load_documents()
    assert isinstance(docs, list)
    assert len(docs) > 0


def test_document_has_required_keys() -> None:
    docs = load_documents()
    for doc in docs:
        assert "id" in doc
        assert "source" in doc
        assert "content" in doc
        assert "category" in doc


def test_document_content_is_nonempty() -> None:
    docs = load_documents()
    for doc in docs:
        assert len(doc["content"]) > 0


def test_load_documents_handles_missing_dir() -> None:
    docs = load_documents(kb_dir="/nonexistent/path")
    assert docs == []


def test_document_category_derived_from_filename() -> None:
    docs = load_documents()
    categories = {doc["category"] for doc in docs}
    assert "account" in categories
    assert "transfer" in categories or "transaction" in categories
