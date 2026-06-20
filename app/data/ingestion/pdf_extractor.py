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
            f"""<<<PAGE
        page: {page_number}
        source: {source}
        >>>

        {text.strip()}

        """
        )
    
    document.close()
    
    document_header = f"""---
    document_id: {document_id}
    ---

    """

    return document_header + "\n".join(pages)
