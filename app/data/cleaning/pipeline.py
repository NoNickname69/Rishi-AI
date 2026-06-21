"""
Cleaning pipeline.

Responsible for applying every cleaner
in sequence.

The pipeline itself contains NO cleaning logic.

Its only job is orchestration.
"""

# Type hints

from typing import Iterable

# Import the common cleaner interface.

from app.data.cleaning.base import BaseCleaner

class CleaningPipeline:
    """
    Sequentially applies every cleaner.
    """
    def __init__(self, cleaners: Iterable[BaseCleaner]):
        """
        Parameters
        ----------
        cleaners

            Ordered list of cleaners.

            The order matters.

            Unicode should usually happen before
            whitespace normalization.
        """

        # Convert to a list so that
        # we can iterate multiple times if needed.
        self.cleaners = list(cleaners)
        
    def clean(self, text: str) -> str:
        """
        Apply every cleaner.

        The output of one cleaner becomes
        the input of the next cleaner.
        """

        # Start with the original text.
        cleaned = text

        # Execute every cleaner.
        for cleaner in self.cleaners:

            cleaned = cleaner.clean(cleaned)

        return cleaned