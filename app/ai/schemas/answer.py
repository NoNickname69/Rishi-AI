from dataclasses import dataclass

from app.models.domain.search_result import SearchResult

@dataclass(slots=True)
class Answer:
    """
    Final response produced by Rishi AI.
    """

    answer: str

    citations: list[str]

    confidence: float

    retrieved_results: list[SearchResult]