from app.data.ocr.base import BaseOCR


from pathlib import Path
from PIL import Image
import fitz  # PyMuPDF
import io


def extract_pdf_text(
        pdf_path: Path,
        document_id: str,
        ocr: BaseOCR | None = None,
        ) -> str:
    """
    Extract text from a PDF while preserving page order.

    If a page contains no embedded text and an OCR engine
    is provided, the page is rendered as an image and
    processed using OCR.
    """

    with fitz.open(pdf_path) as document:

        pages: list[str] = []

        for page_number, page in enumerate(document, start=1): # looping through pages in the document
            
            # Try extracting embedded text before falling back to OCR.
            text = page.get_text("text") 

            source = pdf_path.parent.name
            
            # Render scanned pages as images and extract text using OCR.
            if not text.strip() and ocr is not None:

                # Render the scanned PDF page into an image.
                pixmap = page.get_pixmap()

                # Convert the rendered page into PNG bytes.
                image_bytes = pixmap.tobytes("png")

                # Load the rendered page as a Pillow image.
                image = Image.open(
                    io.BytesIO(image_bytes)
                )
                
                image.load()

                # Extract text from the rendered page using OCR.
                text = ocr.extract_text(image)




            pages.append(
                f"<<<PAGE\n"
                f"page: {page_number}\n"
                f"source: {source}\n"
                f">>>\n\n"
                f"{text}\n"
            )

    return "\n".join(pages)