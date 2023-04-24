from bs4 import BeautifulSoup
from pydash import join
import pydash as _
import spacy


class Processor:
    def __init__(self):
        spacy.prefer_gpu()
        self.nlp = spacy.load("en_core_web_sm")
        self.parser = "html.parser"

    def html_to_text(self, html: str) -> str:
        soup = BeautifulSoup(html, self.parser)
        doc_text = soup.get_text()
        return doc_text

    def process(self, text: str) -> str:
        doc_text = join(
            [
                token.text
                for token in self.nlp(text)
                if not token.is_stop and not token.is_punct
            ],
            " ",
        )
        return doc_text
