from app.ai.schemas.answer import Answer


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

Answer

{answer.answer}

{'═' * 60}

Sources

{self._format_sources(answer.sources)}

{'═' * 60}

Confidence

{answer.confidence:.2f}

{'═' * 60}

"""
    
    def _plain(
            self,
            answer: Answer,
    ) -> str:
        
        return answer.answer
    

    def _format_sources(
            self,
            sources: list[str],
    ) -> str:
        
        if not sources:
            return "No sources available."
        
        return "\n".join(
        f" ♥ {source.title}"
        for source in sources
    )