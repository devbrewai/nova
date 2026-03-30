from chromadb import Collection, QueryResult
from openai import OpenAI

from app.services.embedding import embed_texts
from app.services.vector_store import search


def retrieve(
    query: str, client: OpenAI, collection: Collection, n_results: int = 3
) -> QueryResult:
    """Search user query in ChromaDB store and return results."""
    [query_vector] = embed_texts(texts=[query], client=client)
    results = search(collection, query_vector=query_vector, n_results=n_results)
    return results
