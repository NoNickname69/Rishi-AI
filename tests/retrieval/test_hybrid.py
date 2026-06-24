"""
Manual smoke test for HybridRetriever.

This script executes a hybrid search using Semantic Search,
BM25, and Reciprocal Rank Fusion (RRF), then prints the
ranked retrieval results.
"""

from app.data.embeddings.sentence_transformer import SentenceTransformerEmbedder

from app.models.domain.query import Query
from app.retrieval.search.bm25 import BM25Retriever
from app.retrieval.search.hybrid import HybridRetriever
from app.retrieval.search.semantic import SemanticRetriever
from app.retrieval.vectorstores.chroma import ChromaVectorStore

# Initialize all retrieval components.

embedder = SentenceTransformerEmbedder()


vector_store = ChromaVectorStore()

semantic_retriever = SemanticRetriever(
    embedder=embedder,
    vector_store=vector_store,
)

bm25_retriever = BM25Retriever()

hybrid_retriever = HybridRetriever(
    semantic_retriever=semantic_retriever,
    bm25_retriever=bm25_retriever,
)

query = Query(
    text="What is Brahman?",
    top_k=5,
)

# Execute a sample hybrid retrieval query.

results = hybrid_retriever.search(query)

print("\nHYBRID SEARCH RESULTS\n")

# Display the ranked retrieval results.

for i, result in enumerate(results, start=1):

    print("=" * 80)

    print(f"Rank: {i}")
    print(f"Score: {result.score:.4f}")
    print(f"Document: {result.document_id}")

    print(result.text[:500])

    print()