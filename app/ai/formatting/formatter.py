from app.ai.schemas.answer import Answer
from app.corpus.source import Source



class ResponseFormatter:
    """
    Formats AI responses for different output targets.
    """

    def format(
            self,
            answer: Answer,
            style: str = "terminal",
    ) -> str:
        
        if style == "terminal":
            return self._terminal(answer)

        if style == "plain":
            return self._plain(answer)

        raise ValueError(
            f"Unknown formatting style: {style}"
        )
    
    def _terminal(
            self,
            answer: Answer,
    ) -> str:
        
        return f"""
{'═' * 60}

♥ Direct Answer:

{answer.direct_answer}

{'═' * 60}

☺ Explanation:

{answer.explanation}

{'═' * 60}


☻ Sources
{self._format_sources(answer.sources)}

{'═' * 60}

• Confidence

{answer.confidence:.2f}

{'═' * 60}

"""
    
    def _plain(
            self,
            answer: Answer,
    ) -> str:
        
        return f"{answer.direct_answer}\n\n{answer.explanation}"
    

    def _format_sources(
            self,
            sources: list[Source],
    ) -> str:
        
        if not sources:
            return "No sources available."
        
        unique = []
        seen = set()

        for source in sources:

            if source.document_id not in seen:

                seen.add(source.document_id)
                unique.append(source)
        
        return "\n".join(
        f" ♥ {source.title}"
        for source in unique
    )