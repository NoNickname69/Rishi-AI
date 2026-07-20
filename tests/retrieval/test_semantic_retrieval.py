from app.data.embeddings.sentence_transformer import SentenceTransformerEmbedder
from app.models.domain.query import Query
from app.retrieval.search.semantic import SemanticRetriever
from app.retrieval.vectorstores.chroma import ChromaVectorStore

def test_semantic_retrieval():
    embedder = SentenceTransformerEmbedder()
    vector_store = ChromaVectorStore()

    retriever = SemanticRetriever(
        embedder=embedder,
        vector_store=vector_store,
    )

    query = Query(
        text="What is Brahman?",
        top_k=5,
    )

    results = retriever.search(query)

    print(f"\nRetrieved {len(results)} results\n")

    for i, result in enumerate(results, start=1):
        print(f"{i}. Score: {result.score:.4f}")
        print(f"Document: {result.document_id}")
        print(result.text[:250])
        print("-" * 80)

    assert len(results) > 0

test_semantic_retrieval()