from sentence_transformers import CrossEncoder

from app.models.domain.query import Query
from app.models.domain.search_result import SearchResult

from app.retrieval.rerankers.base import BaseReranker

class CrossEncoderReranker(BaseReranker):
    """
    
    Reranks retrieved search results using a Cross Encoder model.

    Unlike embedding models, a Cross Encoder jointly processes the
    query and each retrieved chunk to produce a more accurate
    relevance score.
    
    """

    def __init__(
            self,
            model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
    ):
        self.model = CrossEncoder(model_name)

    
    def rerank(
            self,
            query: Query,
            results: list[SearchResult],
            #top_k=None, # For future improvements
    ) -> list[SearchResult]:
        
        if not results:
            return []
        
        pairs: list[tuple[str, str]] = [
            (query.text, result.text)
            for result in results
        ]

        scores = self.model.predict(pairs)

        for result, score in zip(results, scores):
            result.score = float(score) # Convert NumPy scalar to native Python float.s

        return sorted(
            results,
            key=lambda result: result.score,
            reverse=True,
        )