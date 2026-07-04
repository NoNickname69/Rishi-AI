from app.ai.generation.pipeline import RAGPipeline
from app.ai.generation.groq import GroqGenerator
from app.ai.prompts.builder import PromptBuilder

from app.data.embeddings.sentence_transformer import (
    SentenceTransformerEmbedder,
)

from app.retrieval.vectorstores.chroma import ChromaVectorStore

from app.retrieval.search.semantic import SemanticRetriever
from app.retrieval.search.bm25 import BM25Retriever
from app.retrieval.search.hybrid import HybridRetriever

from app.retrieval.rerankers.cross_encoder import (
    CrossEncoderReranker,
)
embedder = SentenceTransformerEmbedder()

vector_store = ChromaVectorStore()

semantic = SemanticRetriever(
    embedder=embedder,
    vector_store=vector_store,
)

bm25 = BM25Retriever()

reranker = CrossEncoderReranker()

retriever = HybridRetriever(
    semantic_retriever=semantic,
    bm25_retriever=bm25,
    reranker=reranker,
)

generator = GroqGenerator()

builder = PromptBuilder()

pipeline = RAGPipeline(
    retriever=retriever,
    generator=generator,
    prompt_builder=builder,
)

answer = pipeline.answer(
    "What is Brahman?"
)

print("=" * 80)

print(answer.answer)

print()

print("Confidence")
print(answer.confidence)

print()

print("Sources")

for source in answer.citations:
    print("-", source)