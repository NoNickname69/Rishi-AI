import json
from pathlib import Path

from app.data.cleaning.pipeline import CleaningPipeline
from app.data.chunking.pipeline import ChunkingPipeline
from app.data.chunking.stratergies.fixed import FixedChunker

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DIR = PROJECT_ROOT / "storage" / "processed"

CHUNK_DIR = PROJECT_ROOT / "storage" / "chunks"

CHUNK_DIR.mkdir(
    parents=True,
    exist_ok=True,
)
def main():
    text_files = list(
        PROCESSED_DIR.rglob("text.md")
    )

    print(
        f"Found {len(text_files)} processed documents.\n"
    )

    cleaning_pipeline = CleaningPipeline(
                                            cleaners=[]
                                        )
    chunking_pipeline = ChunkingPipeline(
                                        FixedChunker(
                                            chunk_size=1000,
                                            overlap=200,
                                            )
                                        )
    for text_file in text_files:
        metadata_file = (
            text_file.parent / "metadata.json"
        )

        with open(
            metadata_file,
            "r",
            encoding="utf-8",
        ) as f:

            metadata = json.load(f)
        
        text = text_file.read_text(
            encoding="utf-8"
        )
        cleaned_text = cleaning_pipeline.clean(text)

        document_id = metadata["document_id"]

        chunks = chunking_pipeline.chunk(
                                        text=cleaned_text,
                                        document_id=document_id,
                                        )
        

        output_file = CHUNK_DIR / f"{document_id}.json"

        with open(
                    output_file,
                    "w",
                    encoding="utf-8",
                ) as f:
            json.dump(
        [
            chunk.model_dump()
            for chunk in chunks
        ],
        f,
        indent=4,
        ensure_ascii=False,
            )

        print(f"✓ {document_id}: {len(chunks)} chunks")
if __name__ == "__main__":
    main()