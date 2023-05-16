from tqdm import tqdm
import pydash as _
import torch
import os
from typing import List, Dict, Any

from api.api import Api
from database.repository import Repository
from database.schema.document import Document
from inference.local.chat import LocalChat
from inference.local.chat import LocalChat
from inference.local.classifier import Classifier
from inference.local.entity_extractor import EntityExtractor
from inference.local.summarizer import Summarizer
from inference.openai.chat import OpenAIChat
from inference.openai.chat import OpenAIChat
from loaders.zendesk import ZendeskLoader
from utils.encoder import Encoder
from utils.model_config import save_model_config
from utils.processor import Processor
from utils.text import split_text, DOC_MAX_LENGTH

class Quintus:
    def __init__(
        self,
        *,
        model_name=os.environ.get("EMBEDDING_MODEL")
        or "sentence-transformers/all-mpnet-base-v2",
        parser="html.parser",
    ):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.parser = parser
        self.model_name = model_name
        self.processor = Processor()
        self.encoder = Encoder(model_name)
        self.document_repository = Repository(Document)
        self.local_chat = LocalChat()
        self.classifier = Classifier()
        self.entity_extractor = EntityExtractor()
        self.summarizer = Summarizer()

    def openai_chat(self):
        OpenAIChat().chat()
        
    def local_chat(self):
        LocalChat().chat()

    def serve(self):
        Api().serve()

    def injest(self, url: str):
        self.url = url
        loader = ZendeskLoader()
        data = loader.get_data()
        self.save(data)
        return self

    def add_local_model(self, model_name: str, ft_model_name: str):
        save_model_config(model_name, ft_model_name)
        return self

    def save_document(self, doc_id: str, doc_text: str, doc_title: str, doc_url: str):
        with torch.no_grad():
            embedding = self.encoder.encode(doc_text)
            self.document_repository.create(
                doc_id=doc_id,
                doc_text=doc_text,
                doc_title=doc_title,
                doc_url=doc_url,
                embedding=embedding,
            )
        return self

    def save(self, data: List[Dict[str, Any]]):
        for item in tqdm(data, desc="Saving embeddings..."):
            doc_text = self.processor.html_to_text(item["body"])
            if len(doc_text) > DOC_MAX_LENGTH:
                docs = split_text(doc_text)
                for doc in docs:
                    self.save_document(item["id"], doc, item["title"], item["url"])
            else:
                self.save_document(item["id"], doc_text, item["title"], item["url"])
        return self
