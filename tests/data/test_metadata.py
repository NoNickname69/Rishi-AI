from pathlib import Path

from app.models.domain.metadata import Metadata

metadata = Metadata.from_json(
    Path("storage/raw/scriptures/gita/sivananda/metadata.json")
)

print(metadata)