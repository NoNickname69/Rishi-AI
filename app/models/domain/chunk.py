from pydantic import BaseModel, ConfigDict, Field

from typing import Optional

class Chunk(BaseModel):
    """
    Represents a single chunk of text.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )

    # Identity

    chunk_id: str

    document_id: str

    # Content

    text : str

    # Position

    chunk_index: int

    page_start: Optional[int] = None

    page_end: Optional[int] = None
    
    # Structure

    chapter: Optional[str] = None

    section: Optional[str] = None

    verse_start: Optional[str] = None

    verse_end: Optional[str] = None

    # Statistics

    character_count: int = Field(ge=0)

    word_count: int = Field(ge=0)

    token_count: Optional[int] = None

    # Relationships

    previous_chunk: Optional[str] = None

    next_chunk: Optional[str] = None