from app.ai.schemas.answer import Answer
from app.ai.prompts.builder import PromptBuilder
from app.ai.interfaces.generator import Generator
from app.models.domain.query import Query
from app.ai.generation.exception import InvalidLLMResponseError

import json

class RAGPipeline:
    """
    End-to-end RAG pipeline.
    """

    def __init__(
            self,
            retriever,
            generator: Generator,
            prompt_builder: PromptBuilder,
            corpus_registry = None,
    ):

        self.retriever = retriever
        self.generator = generator
        self.prompt_builder = prompt_builder
        self.corpus_registry = corpus_registry

    def answer(
            self,
            question: str,
            top_k: int = 5, 
    ) -> Answer:
        
        query = Query(
            text=question,
            top_k=top_k,
        )

        results = self.retriever.search(query)

        prompt = self.prompt_builder.build(
            query=question,
            results=results,
        )

        response = self.generator.generate(
            prompt=prompt,
            )
        
        try:

            parsed = json.loads(response)
        
        except json.JSONDecodeError as e:

            raise InvalidLLMResponseError(
                "LLM returned invalid JSON."
            ) from e

        required_fields = {
                "direct_answer",
                "explanation",
            }

        if not required_fields.issubset(parsed):

            missing = required_fields - parsed.keys()

            raise InvalidLLMResponseError(
                f"Missing required fields: {', '.join(sorted(missing))}"
            )

        if self.corpus_registry is not None:
            sources  = [
                self.corpus_registry.get(
                    result.document_id
                )
                for result in results
            ]
        
        else:
            
            sources = []

        confidence = (
            sum(r.score for r in results) / len(results)
            if results
            else 0.0
        )

        return Answer(
            direct_answer=parsed["direct_answer"],
            explanation=parsed["explanation"],
            sources=sources,
            confidence=confidence,
            retrieved_results=results,
        )
