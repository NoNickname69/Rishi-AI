import re

from app.data.chunking.base import BaseChunker
from app.models.domain.chunk import Chunk

class ChapterChunker(BaseChunker):
    """
    Chapter-aware chunking strategy.

    Splits documents based on detected chapter
    headings while preserving chapter boundaries.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        overlap: int = 200,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def find_chapters(
            self,
            text: str,
    ) -> list[tuple[int, str]]:
        """
        Finds all chapter headings in the document.

        Returns:
            A list of tuples containing:
            (character_position, chapter_heading)
        """
        
        chapters: list[tuple[int, str]] = []

        pattern = r"(?im)^chapter\s+\d+"

        for match in re.finditer(
            pattern,
            text,
        ):
            chapters.append(
                (
                    match.start(),
                    match.group(),
                )
            )

        return chapters

    def split_by_chapters(
            self,
            text: str
    ) -> list[str]:
        """
        Splits the document into chapter-sized text blocks.
        """

        chapters = self.find_chapters(text)

        text_chunks: list[str] = []

        if not chapters:

            return [text]
        
        if chapters[0][0] > 0:
            text_chunks.append(
                text[:chapters[0][0]].strip()
            )

        for index, (start, heading) in enumerate(chapters):

            if index < len(chapters) - 1:

                end = chapters[index + 1][0]

            else:

                end = len(text)

            chapter_text = text[start:end].strip()

            text_chunks.append(chapter_text)

        return text_chunks
    
    def chunk(
            self,
            text: str,
            document_id: str,
    ) -> list[Chunk]:
        
        """
        Splits a document using chapter chunking and
        converts the resulting text chunks into Chunk objects.
        """

        text_chunks = self.split_by_chapters(text)

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