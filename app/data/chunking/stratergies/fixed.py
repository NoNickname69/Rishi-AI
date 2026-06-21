"""
Fixed-size chunking strategy.

Splits text into equally sized character chunks.

This strategy is mainly used for testing and benchmarking.
"""

from app.data.chunking.base import BaseChunker
from app.models.domain.chunk import Chunk

class FixedChunker(BaseChunker):

    def __init__(
        self,
        chunk_size: int = 1000,
        overlap: int = 200,
    ):
        """
        Parameters:
        chunk_size: Maximum number of characters per chunk.

        overlap: Number of overlapping characters between chunks.
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk(self,
            text:str, 
            document_id:str,
            ) -> list[Chunk]:
        chunks = []

        start = 0
        chunk_index = 0

        while start < len(text): 
            
            end = min(
                start + self.chunk_size,
                len(text),
            )
            
            chunk_text = text[start:end]

            chunks.append(
                Chunk(
                    chunk_id = f"{document_id}_{chunk_index}",
                    document_id = document_id,
                    text = chunk_text,
                    chunk_index = chunk_index,
                    character_count = len(chunk_text),
                    word_count = len(chunk_text.split()),
                )
            )

            chunk_index += 1

            start += self.chunk_size - self.overlap

            return chunks
         