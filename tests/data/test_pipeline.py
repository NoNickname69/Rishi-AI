from pathlib import Path

from app.data.cleaning.pipeline import CleaningPipeline
from app.data.cleaning.unicode import UnicodeNormalizer
from app.data.cleaning.whitespace import WhitespaceCleaner
from app.data.cleaning.header__footer import HeaderFooterCleaner

pipeline = CleaningPipeline([
    UnicodeNormalizer(),
    WhitespaceCleaner(),
    HeaderFooterCleaner(),
])

text = Path(
    "storage/processed/scriptures/gita/sivananda/text.md"
).read_text(encoding="utf-8")

cleaned = pipeline.clean(text)

print(cleaned[:1000])