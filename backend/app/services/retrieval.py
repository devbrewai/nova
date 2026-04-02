from chromadb import Collection
from openai import OpenAI

from app.services.embedding import embed_texts
from app.services.vector_store import search
from app.types import RetrievalResult


def retrieve(
    query: str,
    client: OpenAI,
    collection: Collection,
    n_results: int = 3,
    threshold: float = 1.5,
) -> list[RetrievalResult]:
    """Search ChromaDB and return results filtered by distance."""
    [query_vector] = embed_texts(texts=[query], client=client)
    raw = search(collection, query_vector=query_vector, n_results=n_results)

    documents = raw["documents"][0] if raw["documents"] else []
    metadatas = raw["metadatas"][0] if raw["metadatas"] else []
    distances = raw["distances"][0] if raw["distances"] else []

    results: list[RetrievalResult] = []
    for doc, meta, dist in zip(documents, metadatas, distances, strict=True):
        if dist <= threshold:
            results.append(
                RetrievalResult(
                    text=doc,
                    source=str(meta["source"]),
                    distance=dist,
                )
            )

    return results
