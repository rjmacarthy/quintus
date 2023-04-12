from pathlib import Path
from tqdm import tqdm
import json
import pydash as _
import torch
import os

from database.repository import Repository
from schema.document import Document
from utils.encoder import Encoder
from utils.processor import Processor
from utils.scraper import Scraper


class Store:
    def __init__(
        self,
        *,
        model_name=os.environ.get("EMBEDDING_MODEL")
        or "sentence-transformers/all-mpnet-base-v2",
        data_dir="data",
        parser="html.parser",
        db_name="embeddings",
        scrape=False,
    ):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.parser = parser
        self.data_dir = Path(data_dir)
        self.encoder = Encoder(model_name)
        self.processor = Processor()
        self.document_repository = Repository(Document, db_name)
        self.scraper = Scraper(self.data_dir)
        self.model_name = model_name
        if scrape:
            scrape()

    def scrape(self, url):
        self.scraper.scrape(url)

    def search(self, query):
        with torch.no_grad():
            return self.document_repository.search(self.encoder.encode(query))

    def index(self):
        json_files = sorted(list(self.data_dir.glob("*.json")))
        for _, file in enumerate(tqdm(json_files, desc="Processing JSON files")):
            with open(file) as f:
                doc = json.load(f)
                doc_text = self.processor.process(doc)
                embedding = self.encoder.encode(doc_text)
            self.document_repository.create(
                doc_id=doc["id"],
                doc_text=doc["body"],
                doc_title=doc["title"],
                doc_url=doc["url"],
                embedding=embedding,
            )
