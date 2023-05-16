from prompts.templates import (
    get_classification_prompt,
    get_context_prompt,
    get_openai_classification_prompt,
    get_system_prompt,
)

from database.repository import Repository
from database.repository import Repository
from database.schema.document import Document
from utils.encoder import Encoder


class Prompts:
    def __init__(self):
        self.repository = Repository(Document)
        self.encoder = Encoder()

    def get_context(self, question: str) -> str:
        max_prompt_length = 1024
        num_relevant_docs = 3
        embeddings = self.encoder.encode(question)
        results = self.repository.search(embeddings)
        text = " ".join([result.doc_text for result in results[:num_relevant_docs]])
        return text[:max_prompt_length]

    def context_prompt(self, question: str, entity: str) -> str:
        context = self.get_context(question)
        return get_context_prompt(question, context, entity)

    def openai_classification_prompt(
        self, document: str, options: list, examples: list
    ) -> str:
        return get_openai_classification_prompt(document, options, examples)

    def classification_prompt(
        self, document: str, options: list, examples: list
    ) -> str:
        return get_classification_prompt(document, options, examples)

    def system_prompt(self, entity: str) -> str:
        return get_system_prompt(entity)
