from app.evaluation.models import (
    EvaluationExample,
    BenchmarkResult,
)

from app.evaluation.evaluator import (
    Evaluator
)


class Benchmark:


    def __init__(
            self,
            evaluator: Evaluator,
    ):
        """
        Parameters:
        ----------
        evaluator:
            Evaluator used to score each example.
        """
        self.evaluator = evaluator

    def run(
    self,
    examples: list[EvaluationExample],
    k: int = 5,
    ) -> BenchmarkResult: 
           

            if not examples:
                return BenchmarkResult(
                average_precision_at_k=0.0,
                average_recall_at_k=0.0,
                average_mrr=0.0,
                num_examples=0,
                )
            

            precision_sum = 0.0

            recall_sum = 0.0

            mrr_sum = 0.0

            for example in examples:
                 
                result = self.evaluator.evaluate(
                      example,
                      k,
                )

                precision_sum += result.precision_at_k

                recall_sum += result.recall_at_k

                mrr_sum += result.mrr

            
            num_examples = len(examples)

            average_precision = precision_sum / num_examples

            average_recall = recall_sum / num_examples

            average_mrr = mrr_sum / num_examples

            return BenchmarkResult(
                    average_precision_at_k=average_precision,
                    average_recall_at_k=average_recall,
                    average_mrr=average_mrr,
                    num_examples=num_examples,
                )