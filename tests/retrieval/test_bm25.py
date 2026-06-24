"""
Manual smoke test for BM25Retriever.

This script performs a sample lexical search and prints the
top-ranked results for manual inspection.
"""

from app.models.domain.query import Query
from app.retrieval.search.bm25 import BM25Retriever

bm25 = BM25Retriever()

results = bm25.search(
    Query(
        text="What is Brahman?",
        top_k=5,
    )
)

# Print the retrieved results in ranked order.

for result in results:
    print("=" * 80)
    print(result.score)
    print(result.document_id)
    print(result.text[:300])