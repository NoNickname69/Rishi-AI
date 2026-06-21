"""
Defines the abstract interface for all text cleaners.

Every cleaner in Rishi AI should inherit from this class.
This guarantees that every cleaner behaves consistently and
can be inserted into the cleaning pipeline.
"""

# Abstract Base Classes allow us to define an interface.
# Any subclass MUST implement the required methods.

from abc import ABC, abstractmethod

class BaseCleaner(ABC):
    """
    Base class for every cleaning step.
    Every cleaner receives a string,
    and returns a cleaned string.
    """

    @abstractmethod
    def clean(self, text: str) -> str:
        """
        Clean the supplied text.

        Parameters:
        text : str # Raw input

        Returns:
        str: Cleaned text
        """