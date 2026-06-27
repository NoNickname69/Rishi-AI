from app.data.embeddings.sentence_transformer import SentenceTransformerEmbedder

from app.models.domain.query import Query

from app.retrieval.search.semantic import SemanticRetriever
from app.retrieval.search.bm25 import BM25Retriever
from app.retrieval.search.hybrid import HybridRetriever

from app.retrieval.rerankers.cross_encoder import CrossEncoderReranker

from app.retrieval.vectorstores.chroma import ChromaVectorStore


embedder = SentenceTransformerEmbedder()

vector_store = ChromaVectorStore()

semantic_retriever = SemanticRetriever(
    embedder=embedder,
    vector_store=vector_store,
)

bm25_retriever = BM25Retriever()

reranker = CrossEncoderReranker()

hybrid_retriever = HybridRetriever(
    semantic_retriever=semantic_retriever,
    bm25_retriever=bm25_retriever,
    reranker=reranker,
)


query = Query(
    text="What is Brahman according to the Upanishads?",
    top_k=5,
)

hybrid_without = HybridRetriever(
    semantic_retriever=semantic_retriever,
    bm25_retriever=bm25_retriever,
)

results = hybrid_without.search(query)

print("\nRESULTS\n")

for rank, result in enumerate(results, start=1):

    print("=" * 80)

    #print(f"Rank: {rank}")
    #print(f"Score: {result.score:.4f}")
    print(f"Document: {result.document_id}\n")

    print(result.text[:700])

hybrid_with = HybridRetriever(
    semantic_retriever=semantic_retriever,
    bm25_retriever=bm25_retriever,
    reranker=reranker,
)

results = hybrid_with.search(query)

print("\nRERANKED RESULTS\n")

for rank, result in enumerate(results, start=1):

    print("=" * 80)

    print(f"Rank: {rank}")
    print(f"Score: {result.score:.4f}")
    print(f"Document: {result.document_id}\n")

    print(result.text[:700])