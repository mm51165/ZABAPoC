from django.core.management.base import BaseCommand

from dataiq.adapters.chunk_repository import DjangoChunkRepository
from dataiq.adapters.text_processor import TransformerTextProcessor
from dataiq.adapters.web_page_parser import BeautifulSoupWebPageParser
from dataiq.application.interactors import (
    ChunkSaver,
    TextBlockExtractor,
    TextChunkProcessor,
    TextProcessingPipeline,
)


class Command(BaseCommand):
    """
    Django management command to extract, process, and store text chunks from a webpage.
    """

    help = "Extract, process, and store text chunks from a webpage"

    def handle(self, *args, **kwargs):
        """
        The main entry point for the command.
        """
        parser = BeautifulSoupWebPageParser()
        processor = TransformerTextProcessor(
            tokenizer_name="intfloat/multilingual-e5-large",
            model_name="intfloat/multilingual-e5-large",
            spacy_model="hr_core_news_sm",
        )
        repository = DjangoChunkRepository()

        extractor = TextBlockExtractor(parser)
        chunk_processor = TextChunkProcessor(processor)
        chunk_saver = ChunkSaver(repository)

        pipeline = TextProcessingPipeline(extractor, chunk_processor, chunk_saver)
        pipeline.run("https://www.zaba.hr/home/smart")
