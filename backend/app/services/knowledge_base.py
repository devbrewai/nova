"""Load and parse knowledge base markdown files."""

from pathlib import Path
from typing import TypedDict

from app.config import settings


class Document(TypedDict):
    id: str
    source: str
    content: str
    category: str


def _derive_category(filename: str) -> str:
    """Derive category from filename prefix (e.g. 'account-opening.md' -> 'account')."""
    stem = Path(filename).stem
    parts = stem.split("-")
    return parts[0] if parts else "general"


def load_documents(kb_dir: str | None = None) -> list[Document]:
    """Load all .md files from the knowledge base directory.

    Args:
        kb_dir: Override path to the knowledge base directory.
                Defaults to settings.knowledge_base_dir.

    Returns:
        List of Document dicts with id, source, content, and category.
        Returns empty list if directory doesn't exist or is empty.
    """
    directory = Path(kb_dir or settings.knowledge_base_dir)

    if not directory.is_dir():
        return []

    documents: list[Document] = []
    for md_file in sorted(directory.glob("*.md")):
        content = md_file.read_text(encoding="utf-8").strip()
        if not content:
            continue
        documents.append(
            Document(
                id=md_file.stem,
                source=md_file.name,
                content=content,
                category=_derive_category(md_file.name),
            )
        )

    return documents
