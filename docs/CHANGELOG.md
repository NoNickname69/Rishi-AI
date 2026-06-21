# Changelog

## v0.1.1 - Phase 1 Foundation

### Repository
- Established scalable project architecture.
- Organized modules into app/, scripts/, storage/, config/, tests/.

### Corpus
- Designed corpus folder hierarchy.
- Added metadata schema.
- Added corpus manifest generation.

### Ingestion
- Implemented PDF extraction using PyMuPDF.
- Added ingestion pipeline.
- Added document manifest validation.
- Added processed corpus generation.

### Cleaning
- Introduced CleaningPipeline.
- Added BaseCleaner abstraction.
- Added UnicodeNormalizer.
- Added WhitespaceCleaner.

### Chunking
- Introduced BaseChunker abstraction.
- Added Chunk model.
- Added FixedChunker.
- Added ChunkingPipeline.

### Embeddings
- Introduced embedding pipeline architecture.
- Added SentenceTransformerEmbedder.

### Vector Database
- Added ChromaDB integration scaffold.

### Misc
- Improved project package structure.
- Added domain models.
- Added unit tests for metadata, extraction, cleaning and chunking.