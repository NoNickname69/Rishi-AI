from app.data.embeddings.pipeline import EmbeddingPipeline
from app.data.embeddings.sentence_transformer import SentenceTransformerEmbedder

pipeline = EmbeddingPipeline(
    SentenceTransformerEmbedder()
)

vectors = pipeline.embed([
    "Krishna teaches karma yoga.",
    "Atman is eternal.",
])

print(vectors.shape)