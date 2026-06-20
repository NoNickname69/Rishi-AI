from app.data.ingestion.pdf_extractor import extract_pdf_text
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

pdf = (
    PROJECT_ROOT
    / "storage"
    / "raw"
    / "scriptures"
    / "gita"
    / "sivananda"
    / "document.pdf"
)

text = extract_pdf_text(
    pdf,
    "bhagavad_gita.sivananda.en"
)

print(text[:3000])