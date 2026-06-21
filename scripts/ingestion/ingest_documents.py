from pathlib import Path
import json
import shutil

from app.data.ingestion.pdf_extractor import extract_pdf_text

# Paths, later to be shifted to \app\core\paths.py

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MANIFEST_PATH = PROJECT_ROOT / "storage" / "corpus_manifest.json"

RAW_DIR = PROJECT_ROOT / "storage" / "raw"

PROCESSED_DIR = PROJECT_ROOT / "storage" / "processed"

def load_manifest():
    """To load .json"""

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:

        return json.load(f)
    
def get_output_directory(pdf_path: Path):
    """Returns output directory."""

    relative = pdf_path.parent.relative_to(RAW_DIR)

    output = PROCESSED_DIR / relative

    output.mkdir(parents=True, exist_ok=True)

    return output

def process_document(entry):

    try:
        pdf_path = Path(entry["pdf_path"])

        metadata_path = Path(entry["metadata_path"])

        output_dir = get_output_directory(pdf_path)

        print(f"Processing: {entry['document_id']}")

        # Extract PDF

        text = extract_pdf_text(
        pdf_path,
        entry["document_id"],
        )

        # Save Text.md

        text_path = output_dir / "text.md"

        text_path.write_text(
        text,
        encoding="utf-8"
        )

        # Copy metadata

        shutil.copy2(
            metadata_path,
            output_dir / "metadata.json",
        )

        print(f"✓ {entry['document_id']}")
    
    except Exception as e:

        print(f"✗ {entry['document_id']}")
        print(e)


def main():
    
    manifest = load_manifest()

    print(f"Found {len(manifest)} documents.\n")
    
    for entry in manifest:

        process_document(entry)

    print("\nIngestion complete.")

if __name__ == "__main__":

    main()