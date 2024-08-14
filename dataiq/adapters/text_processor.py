from typing import List

import spacy
import torch
from transformers import AutoModel, AutoTokenizer

from dataiq.domain.ports import TextProcessor
from dataiq.models import Chunk


class TransformerTextProcessor(TextProcessor):
    """
    A text processor class using transformer models to process text blocks.
    """

    def __init__(self, tokenizer_name: str, model_name: str, spacy_model: str):
        """
        Initializes the TransformerTextProcessor with a tokenizer, model, and spaCy model.

        Args:
            tokenizer_name (str): The name of the tokenizer model.
            model_name (str): The name of the transformer model.
            spacy_model (str): The name of the spaCy model.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.nlp = spacy.load(spacy_model)

    def process_text_blocks(self, text_blocks: List[str]) -> List[Chunk]:
        """
        Processes a list of text blocks into chunks.

        Args:
            text_blocks (List[str]): A list of text blocks.

        Returns:
            List[Chunk]: A list of processed Chunk objects.
        """
        chunks = []
        chunk_id = 1

        for text in text_blocks:
            doc = self.nlp(text)
            sentences = [sent.text for sent in doc.sents]

            current_chunk = ""
            current_chunk_tokens = 0

            for sentence in sentences:
                sentence_tokens = len(self.tokenizer(sentence)["input_ids"])
                if current_chunk_tokens + sentence_tokens > 512:
                    chunk = self.create_chunk(current_chunk.strip())
                    chunks.append(chunk)
                    chunk_id += 1

                    current_chunk = " ".join(
                        current_chunk.split()[-int(len(current_chunk.split()) * 0.1) :]
                    )
                    current_chunk_tokens = len(
                        self.tokenizer(current_chunk)["input_ids"]
                    )

                current_chunk += " " + sentence
                current_chunk_tokens += sentence_tokens

            if current_chunk.strip():
                chunk = self.create_chunk(current_chunk.strip())
                chunks.append(chunk)
                chunk_id += 1

        return chunks

    def create_chunk(self, text: str) -> Chunk:
        """
        Creates a Chunk object from the given text.

        Args:
            text (str): The text content for the chunk.

        Returns:
            Chunk: The created Chunk object.
        """
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True
        )
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state.mean(dim=1)
        embedding = embeddings.numpy().reshape(1, -1)

        keywords = self.extract_keywords(text)
        chunk = Chunk(
            text=text,
            embedding=embedding.tobytes(),
            url="https://www.zaba.hr/home/smart",
            keywords=keywords,
        )
        return chunk

    def extract_keywords(self, text: str) -> List[str]:
        """
        Extracts keywords from the text.

        Args:
            text (str): The text from which to extract keywords.

        Returns:
            List[str]: A list of extracted keywords.
        """
        tokens = [token.lower() for token in text.split() if token.isalpha()]
        keyword_freq = {}

        for token in tokens:
            if token in keyword_freq:
                keyword_freq[token] += 1
            else:
                keyword_freq[token] = 1

        sorted_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)
        top_keywords = [keyword for keyword, _ in sorted_keywords[:5]]

        return top_keywords
