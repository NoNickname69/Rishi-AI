from pathlib import Path
import json
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.models.domain.enums import (
    Category,
    DocumentKind,
    DocumentFormat,
    Language,
)

class Metadata(BaseModel):
    """
    Metadata describing a single document in the corpus.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        str_strip_whitespace=True,
    )

    # Identity

    document_id: str = Field(
        description="Globally unique document identifier."
    )

    title: str = Field(
        description="Canonical title."
    )

    canonical_source: Optional[str] = Field(
        default=None,
        description="Underlying work this document belongs to."
    )

    # Classification, calling from enums.py

    category: Category 

    document_kind: DocumentKind 

    # Authorship

    author: Optional[str] = None

    translator: Optional[str] = None

    commentator: Optional[str] = None

    editor: Optional[str] = None

    # Language

    language: Language

    original_language: Optional[Language] = None

    # Publication

    publication_year: Optional[int] = Field(
        default=None,
        ge=1
    )

    # Source

    source_url: Optional[HttpUrl] = None

    document_format: DocumentFormat = DocumentFormat.PDF

    # Quality

    verified: bool = False

    quality_score: float = Field(
        default=3.0,
        ge=0.0,
        le=5.0
    )

    # Tags

    tags: list[str] = Field(default_factory=list)

    # Serialization

    @classmethod
    def from_json(cls, path: Path) -> "Metadata":
        with open(path, "r", encoding="utf-8") as f:
            return cls.model_validate(json.load(f))

    def to_json(self, path: Path) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                self.model_dump(mode="json"),
                f,
                indent=4,
                ensure_ascii=False,
            )