from typing import List

from dataiq.domain.ports import ChunkRepository, TextProcessor, WebPageParser


class TextBlockExtractor:
    """
    Extracts text blocks from a web page using a WebPageParser.
    """

    def __init__(self, parser: WebPageParser):
        """
        Initializes the TextBlockExtractor with a parser.

        Args:
            parser (WebPageParser): The parser to use for extracting text blocks.
        """
        self.parser = parser

    def extract(self, url: str) -> List[str]:
        """
        Extracts text blocks from a given URL.

        Args:
            url (str): The URL of the web page to extract text from.

        Returns:
            List[str]: A list of extracted text blocks.
        """
        return self.parser.extract_text_blocks(url)


class TextChunkProcessor:
    """
    Processes text blocks into Chunks using a TextProcessor.
    """

    def __init__(self, processor: TextProcessor):
        """
        Initializes the TextChunkProcessor with a text processor.

        Args:
            processor (TextProcessor): The processor to use for processing text blocks.
        """
        self.processor = processor

    def process(self, text_blocks: List[str]) -> List["Chunk"]:
        """
        Processes a list of text blocks into chunks.

        Args:
            text_blocks (List[str]): A list of text blocks.

        Returns:
            List[Chunk]: A list of processed Chunk objects.
        """
        return self.processor.process_text_blocks(text_blocks)


class ChunkSaver:
    """
    Saves chunks using a ChunkRepository.
    """

    def __init__(self, repository: ChunkRepository):
        """
        Initializes the ChunkSaver with a repository.

        Args:
            repository (ChunkRepository): The repository to use for saving chunks.
        """
        self.repository = repository

    def save(self, chunks: List["Chunk"]):
        """
        Saves a list of chunks to the repository.

        Args:
            chunks (List[Chunk]): List of Chunk objects to be saved.
        """
        self.repository.save_chunks(chunks)


class TextProcessingPipeline:
    """
    A pipeline that extracts, processes, and saves text chunks from a web page.
    """

    def __init__(
        self,
        extractor: TextBlockExtractor,
        processor: TextChunkProcessor,
        saver: ChunkSaver,
    ):
        """
        Initializes the TextProcessingPipeline with extractor, processor, and saver.

        Args:
            extractor (TextBlockExtractor): The extractor to use.
            processor (TextChunkProcessor): The processor to use.
            saver (ChunkSaver): The saver to use.
        """
        self.extractor = extractor
        self.processor = processor
        self.saver = saver

    def run(self, url: str):
        """
        Runs the text processing pipeline on a given URL.

        Args:
            url (str): The URL of the web page to process.
        """
        text_blocks = self.extractor.extract(url)
        chunks = self.processor.process(text_blocks)
        self.saver.save(chunks)
