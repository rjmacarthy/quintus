from bs4 import BeautifulSoup
from pydash import join
import pydash as _
import spacy


class Processor:
    def __init__(self):
        spacy.prefer_gpu()
        self.nlp = spacy.load("en_core_web_sm")
        self.parser = "html.parser"

    def to_text(self, doc):
        html = doc["body"]
        soup = BeautifulSoup(html, self.parser)
        doc_text = soup.get_text()
        return doc_text

    def process(self, doc):
        html = doc["body"]
        soup = BeautifulSoup(html, self.parser)
        doc_text = soup.get_text()
        doc_nlp = self.nlp(doc_text)
        doc_filtered = [
            token.text for token in doc_nlp if not token.is_stop and not token.is_punct
        ]
        doc_text = join(doc_filtered, " ")
        return doc_text
