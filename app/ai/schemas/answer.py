from dataclasses import dataclass

from app.models.domain.search_result import SearchResult
from app.corpus.source import Source

@dataclass(slots=True)
class Answer:
    """
    Final response produced by Rishi AI.
    """

    answer: str

    sources: list[Source]

    confidence: float

    retrieved_results: list[SearchResult]