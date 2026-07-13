from app.ai.schemas.answer import Answer
from app.ai.prompts.builder import PromptBuilder
from app.ai.interfaces.generator import Generator
from app.models.domain.search_result import SearchResult
from app.models.domain.query import Query

class RAGPipeline:
    """
    End-to-end RAG pipeline.
    """

    def __init__(
            self,
            retriever,
            generator: Generator,
            prompt_builder: PromptBuilder,
            corpus_registry,
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
        
        sources  = [
            self.corpus_registry.get(
                result.document_id
            )
            for result in results
        ]

        confidence = (
            sum(r.score for r in results) / len(results)
            if results
            else 0.0
        )

        return Answer(
            answer=response,
            sources=sources,
            confidence=confidence,
            retrieved_results=results,
        )
