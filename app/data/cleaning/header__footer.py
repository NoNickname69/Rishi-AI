"""
Header and footer detection.

Version 1.

Detects repeated page headers and footers using frequency.

The cleaner intentionally errs on the side of caution.

False negatives are acceptable.

False positives are not.
"""

from collections import Counter

from app.data.cleaning.base import BaseCleaner

class HeaderFooterCleaner(BaseCleaner):
    """
    Removes repeated page headers and footers.
    """

    def __init__(self):
        
        # Percentage of pages a line must appear on, before it is considered a header/footer.

        self.threshold = 0.80

    def clean(self, text: str) -> str:

        # Split into individual pages.

        pages = text.split("<<<PAGE")

        if len(pages) <= 1:
            return text
        
        # Count candidate header/footer lines

        counter = Counter()

        processed_pages = []

        for page in pages:

            lines = page.splitlines()
        
            if len(lines) < 8:
                processed_pages.append(lines)
                continue

            # First three lines after metadata.
            header = lines[:3]

            # Last three lines.
            footer = lines[-3:]

            for line in header + footer:

                candidate = line.strip()

                if candidate:
                    counter[candidate] += 1

            processed_pages.append(lines)

        # Determine repeated lines

        minimum = int(len(processed_pages) * self.threshold)

        repeated = {

            line

            for line, count in counter.items()

            if count >= minimum

        }


        # Remove repeated lines.

        cleaned_pages = []

        for lines in processed_pages:

            new_lines = []

            for line in lines:

                if line.strip() in repeated:

                    continue

                new_lines.append(line)

            cleaned_pages.append("\n".join(new_lines))

        return"<<<PAGE".join(cleaned_pages)