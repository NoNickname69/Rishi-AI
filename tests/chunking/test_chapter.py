from app.data.chunking.stratergies.chapter import ChapterChunker

chunker = ChapterChunker()

# First test

text = """
Introduction

Some intro.

CHAPTER 1

Hello.

CHAPTER 2

World.
"""

chunks = chunker.chunk(
    text=text,
    document_id="test_doc",
)

print("=" * 80)
print("Test 1")

for chunk in chunks:
    print(chunk.chunk_index)
    print(
    f"{chunk.chunk_index} | "
    f"{len(chunk.text)} chars | "
    f"{chunk.word_count} words"
    )