from dataclasses import dataclass
from typing import Any

"""
Represents a single retrieval result.

A SearchResult contains the retrieved chunk, its relevance score,
and metadata required for citations and downstream processing.
"""

@dataclass(slots=True)
class SearchResult:
    chunk_id: str
    document_id: str
    text: str
    score: float
    metadata: dict[str, Any]