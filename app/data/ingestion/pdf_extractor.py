from pathlib import Path
import fitz  # PyMuPDF

def extract_pdf_text(pdf_path: Path, document_id: str) -> str:
    """
    Extract text from a PDF while preserving page order.
    """

    document = fitz.open(pdf_path)

    pages = [] # a list of pages

    for page_number, page in enumerate(document, start=1): # looping through pages in the document
        
        text = page.get_text("text") # get all text from the page

        source = pdf_path.parent.name

        pages.append(
            f"<<<PAGE\n"
            f"page: {page_num}\n"
            f"source: {source}\n"
            f">>>\n\n"
            f"{text}\n"
        )
    
    document.close()

    return "\n".join(pages)
