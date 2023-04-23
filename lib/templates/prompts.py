from templates.templates import (
    get_system_prompt,
    get_system_prompt_test,
    get_context_prompt,
)

from database.repository import Repository


class Prompts:
    def __init__(self, repository: Repository):
        self.repository = repository

    def get_context(self, question):
        max_prompt_length = 1024
        results = self.repository.search(question)
        text = " ".join([result.doc_text for result in results[:3]])
        context = text[:max_prompt_length]
        return context

    def context_prompt(self, question):
        context = self.get_context(question)
        return get_context_prompt(question, context)

    def system_prompt(self, entity):
        return get_system_prompt(entity)

    def system_prompt_test(self, entity):
        return get_system_prompt_test(entity)
