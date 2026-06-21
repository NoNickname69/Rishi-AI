from app.data.embeddings.base import BaseEmbedder


class EmbeddingPipeline:

    def __init__(self, embedder: BaseEmbedder):

        self.embedder = embedder

    def embed(self, texts):

        return self.embedder.embed(texts)