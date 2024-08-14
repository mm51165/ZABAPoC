from typing import List

import requests
from bs4 import BeautifulSoup

from dataiq.domain.ports import WebPageParser


class BeautifulSoupWebPageParser(WebPageParser):
    """
    A web page parser using BeautifulSoup to extract text blocks.
    """

    def extract_text_blocks(self, url: str) -> List[str]:
        """
        Extracts text blocks from a given URL.

        Args:
            url (str): The URL of the web page to extract text from.

        Returns:
            List[str]: A list of extracted text blocks.
        """
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        text_blocks = []

        rich_copy_sections = soup.find_all("section", class_="rich-copy")
        for section in rich_copy_sections:
            text_blocks.extend(self.parse_rich_copy_section(section))

        faq = self.parse_faq(soup)
        text_blocks.extend(faq)

        return text_blocks

    def parse_rich_copy_section(self, section):
        """
        Parses a rich copy section into text blocks.

        Args:
            section (BeautifulSoup): The section to parse.

        Returns:
            List[str]: A list of text blocks extracted from the section.
        """
        chunks = []
        current_chunk = ""
        previous_tag_was_h3 = False

        for element in section.children:
            if element.name == "h3":
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = element.get_text(strip=True) + "\n"
                previous_tag_was_h3 = True
            elif element.name == "p":
                current_chunk += element.get_text(separator=" ", strip=True) + "\n"
                previous_tag_was_h3 = False
            elif element.name in ["ul", "ol"]:
                list_items = ""
                for li in element.find_all("li"):
                    list_items += " - " + li.get_text(separator=" ", strip=True) + "\n"
                current_chunk += list_items
                previous_tag_was_h3 = False
            elif element.name and not previous_tag_was_h3:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = element.get_text(strip=True) + "\n"

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def parse_faq(self, soup):
        """
        Parses FAQ sections from the web page.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the web page.

        Returns:
            List[str]: A list of FAQ text blocks.
        """
        faq_blocks = []
        for faq_section in soup.select("article.accordion-container"):
            question = faq_section.find("h2", class_="accordion-toggle").get_text(
                strip=True
            )
            answer = faq_section.find("div", class_="accordion-content").get_text(
                separator="\n", strip=True
            )
            faq_blocks.append(f"Q: {question}\nA: {answer}")
        return faq_blocks
