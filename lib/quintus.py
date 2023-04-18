from tqdm import tqdm
import pydash as _
import torch
import os

from database.repository import Repository
from database.schema.document import Document
from inference import Providers
from inference.local import chat as local_chat
from inference.openai import chat
from loaders.loaders import LoaderType
from loaders.zendesk import ZendeskLoader
from templates.prompts import Prompts
from utils.encoder import Encoder
from utils.model_config import save_model_config
from utils.processor import Processor
from utils.text import split_text, DOC_MAX_LENGTH

LOADER_MAP = {
    LoaderType.ZENDESK: ZendeskLoader,
}

PROVIDER_MAP = {
    Providers.OPEN_AI: chat,
    Providers.LOCAL_MODEL: local_chat,
}


class Quintus:
    def __init__(
        self,
        *,
        model_name=os.environ.get("EMBEDDING_MODEL")
        or "sentence-transformers/all-mpnet-base-v2",
        parser="html.parser",
        db_name="embeddings",
        db_user="postgres",
        db_password="",
        db_host="localhost",
        db_port=5432,
    ):
        self.device = torch.device(
            "cuda:0" if torch.cuda.is_available() else "cpu")
        self.parser = parser
        self.encoder = Encoder(model_name)
        self.processor = Processor()
        self.document_repository = Repository(
            Document, db_name=db_name, db_user=db_user, db_password=db_password,
            db_host=db_host, db_port=db_port
        )
        self.prompts = Prompts(self)
        self.model_name = model_name

    def get_loader(self, loader_type):
        return LOADER_MAP[loader_type](self.url)


    def get_provider(self, provider):
        provider_fn = PROVIDER_MAP.get(provider)
        if provider_fn is None:
            raise Exception(f"Provider {provider} not found")
        return provider_fn

    def load(self, loader_type, url):
        self.url = url
        loader = self.get_loader(loader_type)
        data = loader.get_data()
        self.injest(data)
        return self

    def add_local_model(self, model_name, ft_model_name=None):
        save_model_config(model_name, ft_model_name)
        return self

    def search(self, query: str):
        with torch.no_grad():
            return self.document_repository.search(self.encoder.encode(query))

    def save_document(self, doc_id, doc_text, doc_title, doc_url):
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

    def injest(self, data):
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
        return self.get_provider(provider)(self.prompts)
