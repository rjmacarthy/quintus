from utils.processor import Processor
from templates.templates import (
    get_system_prompt,
    get_system_prompt_test,
    get_context_prompt,
)


class Prompts:
    def __init__(self, quintus):
        self.quintus = quintus

    def process(self, question):
        max_prompt_length = 1024
        results = self.quintus.search(question)
        text = results[0].doc_text
        url = results[0].doc_url
        processor = Processor()
        context = processor.html_to_text(text)
        context = context[:max_prompt_length]
        return url, context

    def context_prompt(self, question):
        url, context = self.process(question)
        return get_context_prompt(question, context, url)

    def system_prompt(self, entity):
        return get_system_prompt(entity)

    def system_prompt_test(self, entity):
        return get_system_prompt_test(entity)
