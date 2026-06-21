"""
Chunking pipeline.

Coordinates one chunking strategy.

The pipeline itself does NOT know how to split text.
That responsibility belongs to the selected strategy.
"""

from app.data.chunking.base import BaseChunker
from app.models.domain.chunk import Chunk

class ChunkingPipeline:
    """
    Coordinates documents for chunking.
    """

    def __init__(self, chunker: BaseChunker):
        """
        Parameters:

        chunker: chunking stratergy
        """

        self.chunker = chunker

    def chunk(
            self,
            text: str,
            document_id: str,
    ) -> list[Chunk]:
        """
        Delegate chunking to the configured strategy.
        """

        return self.chunker.chunk(
            text=text,
            document_id=document_id,
        )