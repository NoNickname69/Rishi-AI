from app.data.chunking.stratergies.recursive import RecursiveChunker

chunker = RecursiveChunker()

# Test Small Text

text = (
    "This is a small document. "
    "It should fit into one chunk."
)

chunks = chunker.chunk(
    text=text,
    document_id="test_doc",
)

print("=" * 80)
print("TEST 1, Small Text")

for chunk in chunks:
    print(chunk.chunk_index)
    print(
    f"{chunk.chunk_index} | "
    f"{len(chunk.text)} chars | "
    f"{chunk.word_count} words"
    )

# Test Multiple Paragraphs

text = """

Paragraph One.

Paragraph Two.

Paragraph Three.

"""


chunks = chunker.chunk(
    text=text,
    document_id="test_doc",
)

print("=" * 80)
print("TEST 2, Multiple Paragraphs")

for chunk in chunks:
    print(chunk.chunk_index)
    print(
    f"{chunk.chunk_index} | "
    f"{len(chunk.text)} chars | "
    f"{chunk.word_count} words"
    )
# Test Giant Paragraph

text = "Brahman " * 500

chunks = chunker.chunk(
    text=text,
    document_id="test_doc",
)

print("=" * 80)
print("TEST 3, Giant Paragraph")

for chunk in chunks:
    print(chunk.chunk_index)
    print(
    f"{chunk.chunk_index} | "
    f"{len(chunk.text)} chars | "
    f"{chunk.word_count} words"
    )

# Test No Spaces

text = "A" * 6000

chunks = chunker.chunk(
    text=text,
    document_id="test_doc",
)

print("=" * 80)
print("TEST 4, No Spaces")

for chunk in chunks:
    print(chunk.chunk_index)
    print(
    f"{chunk.chunk_index} | "
    f"{len(chunk.text)} chars | "
    f"{chunk.word_count} words"
    )

#Test Empty String

text = ""

chunks = chunker.chunk(
    text=text,
    document_id="test_doc",
)

print("=" * 80)
print("TEST 5, Empty String")

for chunk in chunks:
    print(chunk.chunk_index)
    print(
    f"{chunk.chunk_index} | "
    f"{len(chunk.text)} chars | "
    f"{chunk.word_count} words"
    )

# This one tests the actual recursive behavior.

text = (
    ("Paragraph One.\n\n") * 30
    +
    ("A" * 5000)
    +
    ("\n\nParagraph Three.")
)

chunks = chunker.chunk(
    text=text,
    document_id="test_doc",
)

print("=" * 80)
print("TEST 6, overall")

for chunk in chunks:
    print(chunk.chunk_index)
    print(
    f"{chunk.chunk_index} | ",
    f"{len(chunk.text)} chars | ",
    f"{chunk.word_count} words",
    repr(chunk.text[:40]),
    )