from templates.templates import (
    get_system_prompt,
    get_system_prompt_test,
    get_context_prompt,
)

from database.repository import Repository


class Prompts:
    def __init__(self, repository: Repository, encoder):
        self.repository = repository
        self.encoder = encoder

    def get_context(self, question: str) -> str:
        max_prompt_length = 1024
        embeddings = self.encoder.encode(question)
        results = self.repository.search(embeddings)
        text = " ".join([result.doc_text for result in results[:3]])
        return text[:max_prompt_length]

    def context_prompt(self, question: str, entity: str) -> str:
        context = self.get_context(question)
        return get_context_prompt(question, context, entity)

    def system_prompt(self, entity: str) -> str:
        return get_system_prompt(entity)

    def system_prompt_test(self, entity: str) -> str:
        return get_system_prompt_test(entity)
