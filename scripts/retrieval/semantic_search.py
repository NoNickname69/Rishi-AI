from app.data.embeddings.sentence_transformer import (
    SentenceTransformerEmbedder,
)
from app.models.domain.query import Query
from app.retrieval.search.semantic import SemanticRetriever
from app.retrieval.vectorstores.chroma import ChromaVectorStore

embedder = SentenceTransformerEmbedder()

vector_store = ChromaVectorStore()

retriever = SemanticRetriever(
    embedder=embedder,
    vector_store=vector_store,
)

query = Query(

    text = "what is Brahman?",
    top_k = 5

)

results = retriever.search(query)
print(results)
print(len(results))

print("Collection count:", vector_store.collection.count())

for result in results:
    print("=" * 80)
    print(result.score)
    print(result.document_id)
    print(result.text)