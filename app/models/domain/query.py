from dataclasses import dataclass

"""
Represents a user's retrieval request.

A query contains the search text along with optional metadata
filters that can restrict retrieval to specific documents,
chapters, sections, or verses.
"""
@dataclass(slots=True)
class Query:
    text: str
    top_k: int = 5

    # Optional filters

    document_id: str | None = None
    chapter: str | None = None
    section: str | None = None

    # Future filters (Planned)

    verse_start: int | None = None
    verse_end: int | None = None