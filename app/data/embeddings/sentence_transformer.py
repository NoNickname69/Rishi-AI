from sentence_transformers import SentenceTransformer

from app.data.embeddings.base import BaseEmbedder


class SentenceTransformerEmbedder(BaseEmbedder):

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5",
    ):

        self.model = SentenceTransformer(model_name)

    def embed(self, texts):

        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
        )