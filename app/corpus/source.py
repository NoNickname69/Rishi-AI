from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Source:
    """
    Represents a document available in the Rishi AI corpus.
    """

    document_id: str

    title: str

    category: str

    document_kind: str

    quality_score: float | None