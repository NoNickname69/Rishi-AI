from pathlib import Path

from app.data.chunking.pipeline import ChunkingPipeline
from app.data.chunking.stratergies.fixed import FixedChunker

text = Path(
    "storage/processed/scriptures/gita/sivananda/text.md"
).read_text(encoding="utf-8")

pipeline = ChunkingPipeline(
    FixedChunker(
        chunk_size=1000,
        overlap=200,
    )
)

chunks = pipeline.chunk(
    text=text,
    document_id="bhagavad_gita.sivananda",
)

print(f"Generated {len(chunks)} chunks\n")

print(chunks[0].model_dump())