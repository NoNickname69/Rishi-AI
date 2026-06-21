"""
Whitespace normalization.

Responsible for normalizing whitespace while preserving
the logical structure of the document.
"""

import re

from app.data.cleaning.base import BaseCleaner

class WhitespaceCleaner(BaseCleaner):
    """
    Normalize whitespace without destroying paragraphs.
    """

    def clean(self, text: str) -> str:
        """
        Replace tabs with spaces.
        """

        text = text.replace("\t", "    ")
        cleaned_lines = []

        # Process each line individually.
        for line in text.splitlines():

            line = line.rstrip() # Remove spaces at the end of the line.

            if line.strip() == "": # Convert whitespace-only lines to empty lines.
                line = ""

            cleaned_lines.append(line)
        
        # Join the cleaned lines.
        text = "\n".join(cleaned_lines)

        text = re.sub(r"\n{3,}", "\n\n", text) # Collapse 3+ blank lines into 2.

        # Remove blank space at the beginning/end of document.
        text = text.strip()

        return text