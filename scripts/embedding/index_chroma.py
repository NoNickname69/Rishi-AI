import json
import numpy as np
from pathlib import Path


from app.data.embeddings.sentence_transformer import (
    SentenceTransformerEmbedder,
)

from app.models.domain.chunk import Chunk
from app.retrieval.vectorstores.chroma import ChromaVectorStore

chunks = []

print("Loading chunks...")

chunk_directory = Path("storage/chunks")

for file in chunk_directory.glob("*.json"):

    print(f"Loading {file.name}")

    with open(file, "r", encoding="utf-8") as f:

        data = json.load(f)

        chunks.extend(
            Chunk.model_validate(item)
            for item in data
        )

    print(f"\nLoaded {len(chunks)} chunks.")

embedder = SentenceTransformerEmbedder()

texts = [
    chunk.text
    for chunk in chunks
]

print(f"Embedding {len(texts)} chunks...")

embedding_file = Path("storage/embeddings.npy")

# earliar I saved the embeddings using np.save("storage/embeddings.nyp", embeddings)
if embedding_file.exists():
    print("Loading cached embeddings...")
    embeddings = np.load(embedding_file)
else: 
    print(f"Embedding {len(texts)} chunks...")
    embeddings = embedder.embed(texts)
    np.save(embedding_file, embeddings)


print(embeddings.shape)

vector_store = ChromaVectorStore()

print(f"Indexing {len(chunks)} chunks...")

"""
Safety net for deletion of the collection
"""
try:
    vector_store.client.delete_collection("rishi_ai")
except Exception:
    pass


vector_store.collection = (
    vector_store.client.get_or_create_collection(
        "rishi_ai"
    )
)

vector_store.add(
    chunks,
    embeddings,
)
print("Texts:", len(texts))


print(
    "Collection count:",
    vector_store.collection.count()
)