from typing import TypedDict


class Chunk(TypedDict):
    id: str
    text: str
    source: str
    category: str
    chunk_index: int