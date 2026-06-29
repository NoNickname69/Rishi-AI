from app.data.embeddings.base import BaseEmbedder
from app.models.domain.query import Query
from app.models.domain.search_result import SearchResult
from app.retrieval.vectorstores.base import BaseVectorStore
from app.retrieval.base import BaseRetriever

class SemanticRetriever(BaseRetriever):
    """
    Retrieves chunks by embedding the query and performing vector similarity search.
    """
    def __init__(
            self,
            embedder: BaseEmbedder,
            vector_store: BaseVectorStore
            ):
        
        self.embedder = embedder
        self.vector_store = vector_store

    def search(
        self,
        query: Query,
    ) -> list[SearchResult]:
        """
        Embed the query text and delegate to the vector store for similarity search.
        """

        # _Note_ : That embed takes a batch (list) and only the first result is used.
        
        query_embedding = self.embedder.embed(
            [query.text]
        )[0]

        return self.vector_store.search(
            query = query,
            query_embedding=query_embedding.tolist(),
        )