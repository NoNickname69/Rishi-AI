import chromadb

from app.models.domain.search_result import SearchResult
from app.retrieval.vectorstores.base import BaseVectorStore
from app.models.domain.query import Query

class ChromaVectorStore(BaseVectorStore):
    """
    Vector store backend backed by a persistent ChromaDB collection.
    """
    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="storage/vectordb"
        )

        self.collection = self.client.get_or_create_collection(
            "rishi_ai"
        )
    


    def search(
            self,
            query: Query,
            query_embedding: list[float],
            ) -> list[SearchResult]:
        
        """
        Search the Chroma collection for the most similar chunks to a query embedding, optionally filtered by document/chapter/section metadata.
        
        """

        # note this builds a Chroma `where` metadata filter dynamically, only including filters the caller actually specified

        where = {}

        if query.document_id is not None:
            where["document_id"] = query.document_id

        if query.chapter is not None:
            where["chapter"] = query.chapter

        if query.section is not None:
            where["section"] = query.section

        query_args = {
            "query_embeddings": [query_embedding],
            "n_results": query.top_k,
            "include": [
                "documents",
                "metadatas",
                "distances",
            ],
        }

        # Only include the "where" clause when at least one filter is present.
        # Passing where={} to Chroma is not equivalent to omitting it and may
        # result in different behavior or validation errors.

        if where:
            query_args["where"] = where
            
        results = self.collection.query(**query_args)

        if not results["ids"]:
            return []
        
        ids = results["ids"][0]
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        search_results = []

        for chunk_id, document, metadata, distance in zip(
            ids,
            documents,
            metadatas,
            distances,
        ):
            search_results.append(
                SearchResult(
                    chunk_id=chunk_id,
                    document_id=metadata["document_id"],
                    text=document,
                    score=1 - distance,
                    metadata=metadata,
                )
            )
        
        return search_results





    def add(
                self,
                chunks,
                embeddings,
            ):
        
        """
        Embed and index a batch of chunks into the Chroma collection, batching writes to stay under Chroma's per-call limits.
        """

        ids = [chunk.chunk_id for chunk in chunks]

        documents = [chunk.text for chunk in chunks]

        embedding_list = embeddings.tolist()

        metadatas = []

        for chunk in chunks:

            metadata = {
                "document_id": str(chunk.document_id),
                "chunk_index": int(chunk.chunk_index),
            }

            if chunk.chapter is not None:
                metadata["chapter"] = str(chunk.chapter)

            if chunk.section is not None:
                metadata["section"] = str(chunk.section)

            if chunk.verse_start is not None:
                metadata["verse_start"] = str(chunk.verse_start)

            if chunk.verse_end is not None:
                metadata["verse_end"] = str(chunk.verse_end)

            if chunk.page_start is not None:
                metadata["page_start"] = int(chunk.page_start)

            if chunk.page_end is not None:
                metadata["page_end"] = int(chunk.page_end)

            metadatas.append(metadata)
        
        # Chroma limits the maximum insert batch size,
        # so large indexing jobs are split into smaller batches.

        BATCH_SIZE = 5000

        total = len(chunks)

        for start in range(0, total, BATCH_SIZE):

            end = min(start + BATCH_SIZE, total)

            self.collection.add(
                ids=ids[start:end],
                documents=documents[start:end],
                embeddings=embedding_list[start:end],
                metadatas=metadatas[start:end],
            )

    def delete(
        self,
        ids: list[str],
        ):
        
        """
        Delete vectors by ID (not yet implemented).
        """
        
        raise NotImplementedError(
            "Delete is not implemented yet."
        )