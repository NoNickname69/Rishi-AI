from app.evaluation.models import EvaluationExample

from app.models.domain.search_result import SearchResult

def precision_at_k(
        
        example: EvaluationExample,
        retrieved_results: list[SearchResult],
        k: int,

) -> float:
    """
    Compute precision@k for a retrieval result.

    Precision@K measures the proportion of the top-K
    retrieved results that are relevant.
    """

    if k <= 0:
        return 0.0
    
    if not retrieved_results:
        return 0.0
    
    relevant_count = 0 

    for result in retrieved_results[:k]:

        if result.document_id in example.relevant_document_ids:

            relevant_count += 1

    return relevant_count/k

def recall_at_k(
        
        example: EvaluationExample,
        retrieved_results: list[SearchResult],
        k: int,

) -> float:
    
    """
    Compute Recall@K for a retrieval result.

    Recall@K measures the proportion of all relevant
    documents that appear within the top-K retrieved
    results.
    """

    if k <= 0:
        return 0.0
    
    if not retrieved_results:
        return 0.0
    
    if not example.relevant_document_ids:
        return 0.0
    
    relevant_count = 0

    found_documents = set()

    for result in retrieved_results[:k]:

        if result.document_id in example.relevant_document_ids:

            if result.document_id not in found_documents:

                relevant_count += 1

                found_documents.add(result.document_id)

    return relevant_count/len(example.relevant_document_ids)


def reciprocal_rank(
        
        example: EvaluationExample,
        retrieved_results: list[SearchResult],

) -> float:
    
    """
    Compute the Reciprocal Rank for a retrieval result.

    The reciprocal rank is the inverse of the rank of
    the first relevant retrieved result. If no relevant
    result is retrieved, returns 0.0.
    """

    if not retrieved_results:
        return 0.0
    
    for rank, result in enumerate(retrieved_results, start=1):
        
        if result.document_id in example.relevant_document_ids:
        
            return 1 / rank

    return 0.0