from abc import ABC, abstractmethod

from app.models.domain.query import Query
from app.models.domain.search_result import SearchResult

class BaseRetriever(ABC):
    """
    Abstract interface for retrieval strategies.
    """

    @abstractmethod
    def search(
        self,
        query: Query,
    ) -> list[SearchResult]:
        """
        Retrieve the most relevant search results for a query.
        """

        raise NotImplementedError