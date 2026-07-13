from __future__ import annotations

import json
from pathlib import Path

from app.corpus.source import Source



class CorpusRegistry:

    def __init__(
            self,
            manifest_path: str | Path,
    ) -> None:
        
        self._manifest_path = Path(manifest_path)

        self._sources: dict[str, Source] = {}

        self._load()

    def _load(
        self,
    ) -> None:
        with self._manifest_path.open(
            "r",
            encoding= "utf-8"
        ) as file:

            manifest = json.load(file)

        for item in manifest:

            source = Source(
                document_id=item["document_id"],
                title=item["title"],
                category=item["category"],
                document_kind=item["document_kind"],
                quality_score=item["quality_score"],
                )

            self._sources[source.document_id] = source

    def get(
        self,
        document_id: str,
    ) -> Source:
        
        return self._sources[document_id]

    def exists(
        self,
        document_id: str,
    ) -> bool:
        
        return document_id in self._sources

    def all(
        self,
    ) -> list[Source]:
        
        return list(self._sources.values())