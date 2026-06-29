from app.evaluation.models import EvaluationExample
from app.evaluation.evaluator import Evaluator
from app.evaluation.benchmark import Benchmark

from app.retrieval.search.semantic import SemanticRetriever
from app.retrieval.vectorstores.chroma import ChromaVectorStore
from app.data.embeddings.sentence_transformer import (
    SentenceTransformerEmbedder,
)


embedder = SentenceTransformerEmbedder()

vector_store = ChromaVectorStore()

retriever = SemanticRetriever(
    embedder=embedder,
    vector_store=vector_store,
)

evaluator = Evaluator(retriever)

benchmark = Benchmark(evaluator)

examples = [

    EvaluationExample(
        query="What is Brahman?",
        relevant_document_ids=[
            "mundaka_upanishad.gurubhaktananda.en.2019",
            "chandogya_upanishad",
        ],
    ),

    EvaluationExample(
        query="Who is Nachiketas?",
        relevant_document_ids=[
            "katha_upanishad.gurubhaktananda.en.2018",
        ],
    ),

    EvaluationExample(
        query="What is Atman?",
        relevant_document_ids=[
            "brihadaranyaka_upanishad",
            "chandogya_upanishad",
        ],
    ),

]

result = benchmark.run(examples)

print("=" * 80)
print("BENCHMARK RESULTS")
print("=" * 80)

print(f"Examples             : {result.num_examples}")
print(f"Average Precision@5  : {result.average_precision_at_k:.3f}")
print(f"Average Recall@5     : {result.average_recall_at_k:.3f}")
print(f"Average MRR          : {result.average_mrr:.3f}")