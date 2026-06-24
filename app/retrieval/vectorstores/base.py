from abc import ABC, abstractmethod

from app.models.domain.query import Query
from app.models.domain.search_result import SearchResult

class BaseVectorStore(ABC):
    """
    Abstract interface for vector store backends supporting add, search, and delete operations.
    """
    @abstractmethod
    def add(
        self, *args, **kwargs
        ):
        """
        Store chunk embeddings in the vector store.
        """
        raise NotImplementedError(
        "Add operation is not implemented yet."
        )
    
    @abstractmethod
    def search(
        self,
        query: Query,
        query_embedding: list[float],
        ) -> list[SearchResult]:
        """
        Return the most similar chunks to a query embedding.
        """
        raise NotImplementedError
    
    @abstractmethod
    def delete(
        self,
        ids: list[str],
    ):
        """
        Delete vectors by ID from the store.
        """
        raise NotImplementedError(
        "Delete operation is not implemented yet."
        )