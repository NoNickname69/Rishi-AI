import json
from pathlib import Path

from rank_bm25 import BM25Okapi

from app.models.domain.query import Query
from app.models.domain.search_result import SearchResult
from app.models.domain.chunk import Chunk
from app.retrieval.search.preprocess import preprocess_query
from app.retrieval.base import BaseRetriever

class BM25Retriever(BaseRetriever):
    """
    Lexical retriever using BM25 ranking over chunks loaded from disk.
    """
    def __init__(self):

        self.chunks = []
        self.documents = []
        self.bm25 = None

        self._load_chunks()

    def _load_chunks(self):
        """
        Load all chunk JSON files from storage, build the BM25 index over their tokenized text.
        """
        chunk_dir = Path("storage/chunks")

        for file in chunk_dir.glob("*.json"):

            with open(file, "r", encoding="utf-8") as f:

                data = json.load(f)

            for item in data:

                chunk = Chunk.model_validate(item)
                
                self.chunks.append(chunk)

                # note that BM25Okapi expects pre-tokenized documents (list of word lists), and this uses a naive .split() rather than the same preprocessing as the query.

                self.documents.append(
                    chunk.text.split()
                )

        self.bm25 = BM25Okapi(self.documents)

        print(
            f"Loaded {len(self.chunks)} chunks into BM25."
        )
    def search(
        self,
        query: Query,
    ) -> list[SearchResult]:
        """
        Tokenize the query and return the top-k highest-scoring chunks by BM25 score.
        """
        tokenized_query = preprocess_query(
            query.text
        )

        scores = self.bm25.get_scores(tokenized_query)

        # _Note_: This sorts (index, score) pairs by score descending to rank chunks.

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True,
        )

        results = []

        for index, score in ranked[: query.top_k]:
            
            # _Note_: That BM25 can return zero/negative-ish scores for non-matching documents, so this filters out irrelevant results before truncation.

            if score <= 0:
                continue

            chunk = self.chunks[index]

            results.append(
                SearchResult(
                    chunk_id=chunk.chunk_id,
                    document_id=chunk.document_id,
                    text=chunk.text,
                    score=float(score),
                    metadata={
                        "document_id": chunk.document_id,
                        "chunk_index": chunk.chunk_index,
                    },
                )
            )

        return results
