from abc import ABC, abstractmethod

from app.models.domain.query import Query
from app.models.domain.search_result import SearchResult

class BaseReranker(ABC):
    """
    Abstract interface for retrieval rerankers.

    A reranker receives an initial list of retrieved search
    results and reorders them based on a more accurate
    relevance model.
    """

    @abstractmethod
    def rerank(
        self,
        query: Query,
        results: list[SearchResult],
    ) -> list[SearchResult]:
        """
        Rerank retrieved search results for a given query.
        """

        raise NotImplementedError