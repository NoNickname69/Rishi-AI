from app.corpus.registry import CorpusRegistry

registry = CorpusRegistry(
    "storage/corpus_manifest.json"
)

source = registry.get(
    "isha_upanishad.aurobindo.en.2003"
)

print(source)

print(source.title)
print(source.category)
print(source.document_kind)

print(
    registry.exists(
        "mahabharata.ganguli.en"
    )
)

print(
    registry.exists(
        "this_do_not_exist"
    )
)

sources = registry.all()

print(len(sources))

print(sources[0])