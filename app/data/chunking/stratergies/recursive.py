"""
Recursive chunking strategy.

Recursively splits oversized text using progressively
smaller separators while preserving as much semantic
structure as possible.
"""

from app.data.chunking.base import BaseChunker
from app.models.domain.chunk import Chunk

class RecursiveChunker(BaseChunker):
    """
    Initializes the recursive chunker.

    Parameters:
        chunk_size: Maximum number of characters per chunk.
        overlap: Number of overlapping characters between chunks.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        overlap: int = 200,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

        self.separators = [
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ]
                
    def split_text(
        self,
        text: str,
        separator: str,
    ) -> list[str]:
        """
        Splits text using the given separator while
        removing empty pieces.
        """

        if separator == "":
            return list(text)

        return [
            part.strip()
            for part in text.split(separator)
            if part.strip()
        ]

    def merged_parts(
        self,
        parts: list[str],
        separator: str,
    ) -> list[str]:
        """
        Greedily merges neighbouring text parts into
        chunks without exceeding chunk_size.
        """

        current_chunk: list[str] = []

        merged_chunks: list[str] = []

        for part in parts:
            candidate = separator.join(
                current_chunk + [part]
            )

            if len(candidate) <= self.chunk_size:
                current_chunk.append(part)
            
            else:

                if current_chunk:
                    merged_chunks.append(
                        separator.join(current_chunk)
                    )
            
                current_chunk = [part]

        if current_chunk:
            merged_chunks.append(
                separator.join(current_chunk)
                )

        return merged_chunks

    def split_recursively(
        self,
        text: str,
        separator_index: int,
    ) -> list[str]:
        """
        Recursively splits oversized text using progressively
        smaller separators until each chunk fits within the
        configured chunk size.
        """

        # Base case


        # If we've exhausted all separators, fall back to
        # fixed-size chunking.

        if separator_index >= len(self.separators):

            return [
                text[i:i + self.chunk_size]
                for i in range(
                    0,
                    len(text),
                    self.chunk_size - self.overlap,
                )
            ]
        # Get the current separator

        separator = self.separators[separator_index]

        # Split the text

        parts = self.split_text(
            text = text,
            separator = separator,
        )

        # Merge neighbouring parts

        merged_parts = self.merged_parts(
            parts,
            separator,
        )

        # Collect the final chunks

        final_chunks: list[str] = []

        # Check if each merged chunk is too large

        for chunk in merged_parts:

        # Small enough?
            if len(chunk) <= self.chunk_size:

                final_chunks.append(chunk)

            # Still too large?
            else:

                final_chunks.extend(

                    self.split_recursively(

                        text=chunk,

                        separator_index=separator_index + 1,

                    )

                )

        # Return the final chunks
        
        return final_chunks

    def chunk(
        self,
        text: str,
        document_id: str,
    ) -> list[Chunk]:
        """
        Splits a document using recursive chunking and
        converts the resulting text chunks into Chunk objects.
        """

        text_chunks = self.split_recursively(
            text=text,
            separator_index=0,
        )

        chunks: list[Chunk] = []

        for chunk_index, chunk_text in enumerate(text_chunks):

            chunks.append(

                Chunk(

                    chunk_id=f"{document_id}_{chunk_index}",

                    document_id=document_id,

                    text=chunk_text,

                    chunk_index=chunk_index,

                    character_count=len(chunk_text),

                    word_count=len(chunk_text.split()),

                )

            )

        return chunks