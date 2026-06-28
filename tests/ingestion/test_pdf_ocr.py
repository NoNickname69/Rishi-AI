"""
from pathlib import Path

from app.data.ingestion.pdf_extractor import extract_pdf_text
from app.data.ocr.rapid import RapidOCRProcessor

import fitz  # PyMuPDF
import io

ocr = RapidOCRProcessor()

pdf_path = Path(
    r"C:\Rishi AI\storage\raw\commentaries\adi_shankaracharya\brahma_sutras\swami_vireswarananda_1936\document.pdf"
)

text = extract_pdf_text(
    pdf_path=pdf_path,
    document_id="ocr_test",
    ocr=ocr,
)

print("=" * 80)
print("OCR TEST")
print("=" * 80)

if text.strip():
    print("♥ Text extracted successfully.")
else:
    print("X No text extracted.")


print(text[:2000])

print("=" * 80)
print(f"Characters: {len(text)}")
print("=" * 80)
"""
from pathlib import Path
import io

import fitz
from PIL import Image

from app.data.ocr.rapid import RapidOCRProcessor


ocr = RapidOCRProcessor()

pdf_path = Path(
    r"C:\Rishi AI\storage\raw\commentaries\adi_shankaracharya\brahma_sutras\swami_vireswarananda_1936\document.pdf"
)

with fitz.open(pdf_path) as document:

    page_number = 10

    print(f"Processing page {page_number}...")

    # PyMuPDF uses zero-based indexing
    page = document.load_page(page_number - 1)

    print("Extracting embedded text...")

    text = page.get_text("text")

    if text.strip():

        print("Embedded text found!")

    else:

        print("No embedded text found.")

        print("Rendering page...")

        pixmap = page.get_pixmap()

        print("Converting to image...")

        image_bytes = pixmap.tobytes("png")

        image = Image.open(
            io.BytesIO(image_bytes)
        )

        image.load()

        print("Running OCR...")

        text = ocr.extract_text(image)

        print("OCR finished!")

print("\n" + "=" * 80)

print(text[:3000])

print("\n" + "=" * 80)

print(f"Characters: {len(text)}")