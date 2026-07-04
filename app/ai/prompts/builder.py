from app.ai.prompts.templates import SYSTEM_PROMPT
from app.models.domain.search_result import SearchResult

class PromptBuilder:
    """Builds prompt for the Large Language Model."""
    def build(
        self,
        query: str,
        results: list[SearchResult],
    ) -> str:
        """
        Build a complete prompt from the user query and retrieved context.
        """

        context = self._build_context(results)

        return f"""{SYSTEM_PROMPT}

========================
CONTEXT
========================

{context}

========================
USER QUESTION
========================

{query}

========================
INSTRUCTION
========================

Answer using ONLY provided context.

If the answer cannot be found in the provided context,
Say you don't know.

At the end, mention which sources were used.
"""
    

    def _build_context(
            self,
            results: list[SearchResult],
    ) -> str:
        """Convert retireval resutls into prompt context."""

        sections = []

        for i, result in enumerate(results, start=1):
            
            title = result.metadata.get(
                "title",
                result.document_id,
            )

            sections.append(
                f"""
                Source: {i}
                Document: {title}
                Score: {result.score:.3f}

                {result.text}
                """
            )

        return "\n\n".join(sections)