"""
Unicode normalization.

This module converts visually identical Unicode characters
into a single canonical representation.

Without normalization, PDFs extracted from different sources
may contain different Unicode code points for the same text.
"""

# Python's built-in Unicode library.

# It knows how to normalize thousands of Unicode characters.

import unicodedata

# Import the common cleaner interface

from app.data.cleaning.base import BaseCleaner

class UnicodeNormalizer(BaseCleaner):
    """
    Normalize Unicode characters.

    Uses Unicode NFKC normalization.

    NFKC = Compatibility Composition

    This is generally the safest choice for
    search engines, NLP and RAG systems.
    """

    def clean(self, text: str) -> str:
        """
        Normalize Unicode.
        """

        return unicodedata.normalize(
            "NFKC",
            text,
        )