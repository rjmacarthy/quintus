import torch
import asyncio

from inference.local.model import LocalModel
from inference.local.stream import stream
from prompts.prompts import Prompts


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class LocalChat:
    def __init__(self):
        self.prompts = Prompts()

    def chat(self):
        local_model = LocalModel()
        model, tokenizer = local_model.get_instance()

        while True:
            user_input = input("👤: ")
            prompt = self.prompts.context_prompt(user_input, "The company")
            response = stream(prompt, tokenizer, model, device)
            asyncio.run(self.consume_stream(response))
            torch.cuda.empty_cache()

    async def consume_stream(self, stream):
        async for line in stream:
            print(f"{line}", end="", flush=True)
        print()
