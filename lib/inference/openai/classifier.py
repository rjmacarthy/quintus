from inference.openai.model import OpenAIModel
from prompts.prompts import Prompts


class Classifier:
    def __init__(self):
        self.model = OpenAIModel()

    def run(self, document, options, examples=[]):
        prompt = Prompts().openai_classification_prompt(document, options, examples)
        messages = [{"role": "system", "content": self.prompts.system_prompt(prompt)}]
        return self.model.completion(messages)
