from app.data.chunking.stratergies.semantic import SemanticChunker
from app.data.embeddings.sentence_transformer import (
    SentenceTransformerEmbedder,
)

embedder = SentenceTransformerEmbedder()

chunker = SemanticChunker(
    embedder=embedder,
    similarity_threshold=0.60,
)

text = """
Brahman is the ultimate reality.

It is eternal and infinite.

The Atman is identical to Brahman.

Meditation calms the mind.

Concentration naturally follows meditation.

Karma binds beings to the cycle of rebirth.

Liberation comes through Self-knowledge.
"""

chunks = chunker.chunk(
    text=text,
    document_id="smoke_test",
)

print("=" * 80)
print("SEMANTIC CHUNKS")
print("=" * 80)

for chunk in chunks:

    print(f"\nChunk {chunk.chunk_index}")
    print("-" * 40)

    print(chunk.text)

    print()

sentences = chunker._split_sentences(text)

print("=" * 80)
print("SENTENCES")
print("=" * 80)

for i, sentence in enumerate(sentences):
    print(f"{i}: {sentence}")

embeddings = chunker._embed_sentences(sentences)

similarities = chunker._compute_similarities(embeddings)

print("=" * 80)
print("SIMILARITIES")
print("=" * 80)

for i, similarity in enumerate(similarities):
    print(
        f"{i} -> {i+1}: {similarity:.4f}"
    )

boundaries = chunker._find_boundaries(similarities)

print("=" * 80)
print("BOUNDARIES")
print("=" * 80)

for i, boundary in enumerate(boundaries):

    print(
        f"{i} -> {i+1}: {boundary}"
    )