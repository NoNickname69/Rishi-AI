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

{self._format_sources(answer.citations)}

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
            citations: list[str],
    ) -> str:
        
        if not citations:
            return "No sources available."
        
        unique = []
        seen = set()

        for citation in citations:
            
            pretty = self._prettify_document(citation)

            if pretty not in seen:

                seen.add(pretty)
                unique.append(pretty)


        return "\n".join(
        f"{source}"
        for source in unique
    )

    def _prettify_document(
            self,
            document: str,
    ) -> str:

        document = document.split(".")[0]
        document = document.replace("_", " ")

        return document.title()