from app.models.domain.search_result import SearchResult

from dataclasses import dataclass

@dataclass
class EvaluationExample:
    """

    Represents a single evaluation example used to
    benchmark retrieval quality.

    Each example consists of a natural-language query
    and the documents or chunks that should ideally
    be retrieved for that query.

    """

    query: str

    relevant_document_ids: list[str]

    relevant_chunk_ids: list[str] | None = None

    metadata: dict[str, str] | None = None


@dataclass
class EvaluationResult:

    """
    Stores the evaluation metrics produced for a 
    single retrieval query.

    Each result links an evaluation example with the
    retrieved search results and the computed metrics.
    """

    example: EvaluationExample

    retrieved_results: list[SearchResult]

    precision_at_k: float

    recall_at_k: float

    mrr: float

@dataclass
class BenchmarkResult:

    """
    Stores the aggregate metrics produced from evaluating
    a collection of retrieval queries.
    """

    average_precision_at_k: float

    average_recall_at_k: float

    average_mrr: float

    num_examples: int