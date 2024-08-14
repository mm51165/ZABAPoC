from abc import ABC, abstractmethod
from typing import List


class WebPageParser(ABC):
    """
    Abstract base class for web page parsers.
    """

    @abstractmethod
    def extract_text_blocks(self, url: str) -> List[str]:
        """
        Extracts text blocks from a given URL.

        Args:
            url (str): The URL of the web page to extract text from.

        Returns:
            List[str]: A list of extracted text blocks.
        """
        pass


class TextProcessor(ABC):
    """
    Abstract base class for text processors.
    """

    @abstractmethod
    def process_text_blocks(self, text_blocks: List[str]) -> List["Chunk"]:
        """
        Processes text blocks into chunks.

        Args:
            text_blocks (List[str]): A list of text blocks.

        Returns:
            List[Chunk]: A list of processed Chunk objects.
        """
        pass


class ChunkRepository(ABC):
    """
    Abstract base class for chunk repositories.
    """

    @abstractmethod
    def save_chunks(self, chunks: List["Chunk"]):
        """
        Saves chunks to the repository.

        Args:
            chunks (List[Chunk]): List of Chunk objects to be saved.
        """
        pass
