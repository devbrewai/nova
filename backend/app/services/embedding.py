from openai import OpenAI


def get_openai_client() -> OpenAI:
    """Initialize the OpenAI client and return it."""
    return OpenAI()


def embed_texts(texts: list[str], client: OpenAI) -> list[list[float]]:
    """Embed text using OpenAI embedding API and return vectors."""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts,
    )
    vectors = [item.embedding for item in response.data]
    return vectors


def embed_chunks(chunks: list[dict[str, object]], client: OpenAI) -> list[list[float]]:
    """Embed a list of chunks text."""
    texts = [str(chunk["text"] for chunk in chunks)]
    vectors = embed_texts(texts, client)
    return vectors
