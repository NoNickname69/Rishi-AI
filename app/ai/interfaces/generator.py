from abc import ABC, abstractmethod

class Generator(ABC):
    """Abstract interface for all LLM generators."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        
        """
        Generate an answer from the given prompt.

        Args:
            Prompt: Fully constructed prompt.
        
        Returns:
            Generated response.
        """

        pass