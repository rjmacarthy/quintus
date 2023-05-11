from tqdm import tqdm
import pydash as _
import torch
import os
from typing import List, Dict, Any

from database.repository import Repository
from database.schema.document import Document
from inference import Provider
from inference.openai.chat import OpenAIChat
from loaders.loaders import LoaderType
from loaders.zendesk import ZendeskLoader
from templates.prompts import Prompts
from utils.encoder import Encoder
from utils.model_config import save_model_config
from utils.processor import Processor
from utils.text import split_text, DOC_MAX_LENGTH

LOADER_MAP: Dict[LoaderType, Any] = {
    LoaderType.ZENDESK: ZendeskLoader,
}

PROVIDER_MAP: Dict[Provider, Any] = {
    Provider.OPEN_AI: OpenAIChat,
}


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
        self.encoder = Encoder(model_name)
        self.processor = Processor()
        self.document_repository = Repository(Document)
        self.prompts = Prompts(self.document_repository, self.encoder)
        self.model_name = model_name
        self.chat_provider = None

    def get_loader(self, loader_type: LoaderType):
        return LOADER_MAP[loader_type](self.url)

    def get_provider(self, provider: str):
        Provider = PROVIDER_MAP.get(provider)
        if Provider is None:
            raise Exception(f"Provider {Provider} not found")
        return Provider

    def load(self, loader_type: LoaderType, url: str):
        self.url = url
        loader = self.get_loader(loader_type)
        data = loader.get_data()
        self.injest(data)
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

    def injest(self, data: List[Dict[str, Any]]):
        for item in tqdm(data, desc="Saving embeddings..."):
            doc_text = self.processor.html_to_text(item["body"])
            if len(doc_text) > DOC_MAX_LENGTH:
                docs = split_text(doc_text)
                for doc in docs:
                    self.save_document(item["id"], doc, item["title"], item["url"])
            else:
                self.save_document(item["id"], doc_text, item["title"], item["url"])
        return self

    def chat(self, provider: str):
        return self.get_provider(provider)(self.prompts).chat()
