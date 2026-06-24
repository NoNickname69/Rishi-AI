from collections import defaultdict

from app.models.domain.search_result import SearchResult


class ReciprocalRankFusion:
    """
    Fuses multiple ranked result lists into one using Reciprocal Rank Fusion (RRF).
    """
    def __init__(
        self,
        k: int = 60,
    ):
        self.k = k

    def fuse(
        self,
        *result_lists: list[SearchResult],
        top_k: int = 5,
    ) -> list[SearchResult]:
        """
        Combine multiple ranked result lists by RRF score and return the top-k fused results.
        """
        scores = defaultdict(float)

        best_results = {}

        for results in result_lists:

            for rank, result in enumerate(results):

                # Reciprocal Rank Fusion (RRF):
                # Higher-ranked results contribute more to the final score.
                # If a chunk appears in multiple retrievers, their
                # contributions accumulate, boosting its overall ranking.

                scores[result.chunk_id] += (
                    1 / (self.k + rank + 1)
                )

                #_Note_: This keeps the most recently seen SearchResult object for a given chunk_id
                # (used later to reconstruct text/metadata in fused output)

                best_results[result.chunk_id] = result

        # _Note_: This sorts fused chunk_id→score pairs descending by combined RRF score.

        ranked = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        fused_results = []

        for chunk_id, fused_score in ranked[:top_k]:

            original = best_results[chunk_id]

            fused_results.append(
                SearchResult(
                    chunk_id=original.chunk_id,
                    document_id=original.document_id,
                    text=original.text,
                    score=fused_score,
                    metadata=original.metadata,
                )
            )

        return fused_results