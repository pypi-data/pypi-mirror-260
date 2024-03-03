"""Ranker Resource Module."""

from typing import List

from ..dataclasses.embed import EmbeddingMeta
from .base import AsyncResource, SyncResource


class SyncEmbeddingResource(SyncResource):
    """Synchronous Embedding Resource Class."""

    def embed(
        self,
        texts: List[str],
    ) -> List[EmbeddingMeta]:
        """Embed all texts."""
        output = self._post(
            data={
                "input_data": {"texts": texts},
                "task": "embedding",
            },
        )
        output.raise_for_status()
        return [
            EmbeddingMeta(
                embedding=emb["embedding"],
                text=emb["text"],
            )
            for emb in output.json()["output"]
        ]


class AsyncEmbeddingResource(AsyncResource):
    """Asynchronous Embedding Resource Class."""

    async def embed(
        self,
        texts: List[str],
        read_timeout: float = 10.0,
        timeout: float = 180.0,
    ) -> List[EmbeddingMeta]:
        """Asynchronously embed all texts."""
        response = await self._post(
            data={
                "input_data": {"texts": texts},
                "task": "embedding",
            },
            read_timeout=read_timeout,
            timeout=timeout,
        )
        response.raise_for_status()  # Ensure proper exception handling in your async context.
        return [
            EmbeddingMeta(
                embedding=emb["embedding"],
                text=emb["text"],
            )
            for emb in response.json()["output"]
        ]
