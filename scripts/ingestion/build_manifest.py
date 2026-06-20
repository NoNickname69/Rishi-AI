from pathlib import Path
import json
from pathlib import Path
import hashlib

# Project root (two levels above this file)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "storage" / "raw" # Reads the entire content of storage raw (unprocessed)
OUTPUT_FILE = PROJECT_ROOT / "storage" / "corpus_manifest.json" # Output file is a directory of file location

# List of required fields 
REQUIRED_FIELDS = [
    "document_id",
    "title",
    "category",
    "document_kind"
]


def find_documents(root: Path):
    """
    Recursively find every document folder that contains both:
    document.pdf and metadata.json.
    """

    documents = [] # Initializing a list of documents

    for metadata_file in root.rglob("metadata.json"): # looping through rglob (returns all existing files)

        folder = metadata_file.parent
        pdf_file = folder / "document.pdf"


        if not pdf_file.exists():
            print(f"[WARNING] Missing PDF: {folder}")
            continue

        documents.append((pdf_file, metadata_file))

    return documents

def load_metadata(path: Path): 
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def calculate_sha256(file_path): 
    """
    computes a SHA-256 hash and file size for every PDF
    For implementing incremental ingestion (only reprocessing changed documents), if needed later.
    """
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()

def build_manifest():

    manifest = [] # initializing a list for storing manifested paths

    docs = find_documents(RAW_DIR) # list of all PDFs returned from find_documents()

    seen = set() # Only keeps unique elements

    stats = {} # For keeping stats

    print(f"Found {len(docs)} documents.\n")

    for pdf_path, metadata_path in docs: # Looping through paths for each path in docs

        metadata = load_metadata(metadata_path)  #loading metadata.json for each path

        # checks for any missing fieldd
        missing = [
            field for field in REQUIRED_FIELDS
            if field not in metadata
        ]

        if missing:
            print(f"[ERROR] {metadata_path} missing fields: {missing}")
            continue

        if metadata["document_id"] in seen:
            raise ValueError(
                f"Duplicate document_id: {metadata['document_id']}"
            )

        seen.add(metadata["document_id"])

        file_size = pdf_path.stat().st_size # calculating file size
        sha256 = calculate_sha256(pdf_path)

        # appending for storing manifested paths
        manifest.append({ 

            "document_id": metadata["document_id"],

            "title": metadata["title"],

            "category": metadata.get("category"),

            "document_kind": metadata.get("document_kind"),

            "quality_score": metadata.get("quality_score"),

            "pdf_path": str(pdf_path),

            "metadata_path": str(metadata_path),

            "file_size": file_size,

            "sha256": sha256,

        })

        # For stats
        category = metadata["category"]

        stats[category] = stats.get(category, 0) + 1


    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True) # Making a directory for output file

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

        json.dump(manifest, f, indent=4, ensure_ascii=False) # Updating .json file

    print(f"Manifest written to {OUTPUT_FILE}")

    # Looks very professional
    print("\n========== Manifest Summary ==========")
    print(f"Documents : {len(manifest)}")

    for category, count in sorted(stats.items()):
        print(f"{category:<15}: {count}")

    print("======================================")

if __name__ == "__main__": # Running build_manifest()
    build_manifest()