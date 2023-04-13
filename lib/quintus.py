from pathlib import Path
from tqdm import tqdm
import json
import pydash as _
import torch
import os

from database.repository import Repository
from database.schema.document import Document
from utils.model_config import save_model_config
from utils.encoder import Encoder
from utils.processor import Processor
from utils.scraper import Scraper
from inference.providers.openai import chat as openai_chat
from inference.local.local import chat as local_chat
from inference.providers.provider_names import ProviderNames
from templates.prompts import Prompts


class Quintus:
    def __init__(
        self,
        *,
        model_name=os.environ.get("EMBEDDING_MODEL")
        or "sentence-transformers/all-mpnet-base-v2",
        data_dir="data",
        parser="html.parser",
        db_name="embeddings",
    ):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.parser = parser
        self.data_dir = Path(data_dir)
        self.encoder = Encoder(model_name)
        self.processor = Processor()
        self.document_repository = Repository(Document, db_name)
        self.scraper = Scraper(self.data_dir)
        self.prompts = Prompts(self)
        self.model_name = model_name
        self.providers = ProviderNames

    def get_provider(self, provider):
        if provider == ProviderNames.OPEN_AI.value:
            return openai_chat
        if provider == ProviderNames.LOCAL_MODEL.value:
            return local_chat
        else:
            raise Exception(f"Provider {provider} not found")

    def scrape(self, url, filters):
        self.scraper.scrape(url, filters)
        return self
    
    def add_local_model(self, model_name, ft_model_name=None):
        save_model_config(model_name, ft_model_name)
        return self

    def search(self, query: str):
        with torch.no_grad():
            return self.document_repository.search(self.encoder.encode(query))

    def chat(self, provider: str):
        return self.get_provider(provider)(self.prompts)

    def injest(self):
        json_files = sorted(list(self.data_dir.glob("*.json")))
        for _, file in enumerate(tqdm(json_files, desc="Processing JSON files")):
            with open(file) as f:
                doc = json.load(f)
                doc_text = self.processor.html_to_text(doc["body"])
                embedding = self.encoder.encode(doc_text)
            self.document_repository.create(
                doc_id=doc["id"],
                doc_text=doc["body"],
                doc_title=doc["title"],
                doc_url=doc["url"],
                embedding=embedding,
            )
        return self
