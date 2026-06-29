from app.retrieval.base import BaseRetriever
from app.models.domain.query import Query
from app.evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)
from app.evaluation.models import (
    EvaluationExample,
    EvaluationResult
)

class Evaluator:

    """
    Evaluates retrieval performance using a collection
    of standard information retrieval metrics.
    """
    def __init__(
    self,
    retriever: BaseRetriever,   
    ):
        """
        Parameters
        ----------
        retriever:
            Retrieval strategy to evaluate.
        """
        self.retriever = retriever

    def evaluate(
            
            self,
            example: EvaluationExample,
            k: int = 5,
    ) -> EvaluationResult:
        
        """
        Evaluate retrieval performance for a single query.

        The retriever is executed on the query contained in the
        evaluation example, after which retrieval metrics are
        computed and returned as an EvaluationResult.
        """

        query = Query(

            text=example.query,
            top_k=k,

        )

        retrieved_results = self.retriever.search(
            query
        )

        precision = precision_at_k(
            example,
            retrieved_results,
            k,
        )

        recall = recall_at_k(
            example,
            retrieved_results,
            k,
        )

        reciprocal = reciprocal_rank(
            example,
            retrieved_results,
        )

        return EvaluationResult(
            example=example,
            retrieved_results=retrieved_results,
            precision_at_k=precision,
            recall_at_k=recall,
            mrr=reciprocal,
        )