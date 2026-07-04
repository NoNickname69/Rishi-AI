import os

from dotenv import load_dotenv
from groq import Groq

from app.ai.interfaces.generator import Generator

# Load environment variables from .env
load_dotenv()

class GroqGenerator(Generator):
    """LLM Generator backed by groq API."""

    def __init__(
            
            self,
            api_key: str | None = None,
            model: str = "llama-3.3-70b-versatile",

    ):
        self.client = Groq(
            api_key=api_key or os.getenv("GROQ_API_KEY")
        )

        self.model = model

    
    def generate(
            self,
            prompt: str,
    ) -> str:
        """Generate a response from the language model."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                    {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content.strip()