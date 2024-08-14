from typing import List

import numpy as np

from dataiq.domain.ports import ChunkRepository
from dataiq.models import Chunk
from dataiq.models import Chunk as ChunkModel


class DjangoChunkRepository(ChunkRepository):
    """
    A repository class for saving chunks using Django ORM.
    """

    def save_chunks(self, chunks: List[Chunk]) -> None:
        """
        Saves a list of chunks to the database.

        Args:
            chunks (List[Chunk]): List of Chunk objects to be saved.
        """
        for chunk in chunks:
            chunk_instance = ChunkModel(
                text=chunk.text,
                url=chunk.url,
                keywords=chunk.keywords,
            )
            embedding = np.frombuffer(chunk.embedding, dtype=np.float32)
            self.store_chunk_embedding(chunk_instance, embedding)

    def store_chunk_embedding(
        self, chunk_instance: ChunkModel, embedding: np.ndarray
    ) -> None:
        """
        Stores the embedding for a chunk in the database.

        Args:
            chunk_instance (ChunkModel): The Chunk model instance.
            embedding (np.ndarray): The embedding as a numpy array.

        Raises:
            ValueError: If embedding dimensions are not as expected.
        """
        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)

        if embedding.ndim != 2 or embedding.shape[0] != 1:
            raise ValueError("Embedding dimensions are not in the expected shape.")

        embedding_bytes = embedding.astype(np.float32).tobytes()
        chunk_instance.embedding = embedding_bytes
        chunk_instance.save()
