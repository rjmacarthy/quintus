from pathlib import Path
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import json
import pydash as _
import torch

from database.repository import Repository
from schema.document import Document
from utils.encoder import Encoder
from utils.processor import Processor
from utils.scraper import Scraper


class Store:
    def __init__(
        self, 
        model_name, *, 
        data_dir="data", 
        parser="html.parser", 
        db_name="embeddings",
    ):
        self.model = SentenceTransformer(model_name)
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.parser = parser
        self.data_dir = Path(data_dir)
        self.encoder = Encoder(model_name)
        self.processor = Processor()
        self.document_repository = Repository(Document, db_name)
        self.scraper = Scraper(self.data_dir)

    def scrape(self, url):
        self.scraper.scrape(url)

    def search(self, query):
        self.model.to(self.device)
        with torch.no_grad():
            query_embedding = self.model.encode(query)
            documents = self.document_repository.search(query_embedding)
            for doc in documents:
                print(doc.doc_id)
            return documents

    def index(self):
        json_files = sorted(list(self.data_dir.glob("*.json")))
        for _, file in enumerate(tqdm(json_files, desc="Processing JSON files")):
            with open(file) as f:
                doc = json.load(f)
                doc_text = self.processor.process(doc)
                embedding = self.encoder.encode(doc_text)

            self.document_repository.create(
                doc_text=doc["body"],
                doc_id=doc["id"],
                embedding=embedding,
            )
