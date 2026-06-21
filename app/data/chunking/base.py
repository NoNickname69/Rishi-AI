from abc import ABC, abstractmethod

from app.models.domain.chunk import Chunk

class BaseChunker(ABC):
    """
    Abstract interface for all chunking strategies.
    """
    
    @abstractmethod
    def chunk(
        self,
        text: str,
        document_id: str,
    ) -> list[Chunk]:
        """
        Split the supplied document into chunks.
        """

        raise NotImplementedError