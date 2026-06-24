"""
Combines dense semantic retrieval and sparse BM25 retrieval
using Reciprocal Rank Fusion (RRF).

This retriever orchestrates multiple retrieval strategies and
returns a single ranked list of search results.
"""

from app.models.domain.query import Query
from app.models.domain.search_result import SearchResult

from app.retrieval.search.fusion import ReciprocalRankFusion
from app.retrieval.search.bm25 import BM25Retriever
from app.retrieval.search.semantic import SemanticRetriever


class HybridRetriever:
    """
    Combines semantic and lexical (BM25) retrieval results via Reciprocal Rank Fusion.
    """
    def __init__(
            
            self,
            semantic_retriever: SemanticRetriever,
            bm25_retriever: BM25Retriever,
    ):
        self.semantic_retriever = semantic_retriever
        self.bm25_retriever = bm25_retriever

        self.fusion = ReciprocalRankFusion()

    def search(
            self,
            query:Query,
    ) -> list[SearchResult]:
        """
        Retrieve and fuse top results from both semantic and BM25 retrievers for a given query.


        note: why top_k=20 is hardcoded here instead of using query.top_k,
        this is the "over-fetch before fusion" pattern.
        This way both methods will fetch top 20 results.
        """

        retrieval_query = Query(
            text=query.text,
            top_k=20,
            document_id=query.document_id,
            chapter=query.chapter,
            section=query.section,
            verse_start=query.verse_start,
            verse_end=query.verse_end,
        )


        semantic_results = self.semantic_retriever.search(
            retrieval_query
        )

        bm25_results = self.bm25_retriever.search(
            retrieval_query
        )

        # Fusion is what trims results back down to the user-requested query.top_k
        fused_results = self.fusion.fuse(
            semantic_results,
            bm25_results,
            top_k=query.top_k,
        )

        return fused_results