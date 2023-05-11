import torch
import asyncio

from inference.local.model import get_local_model
from inference.local.stream import stream
from templates.prompts import Prompts

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class LocalChat:
    def __init__(self, prompts: Prompts):
        self.prompts = prompts

    def chat(self):
        model, tokenizer = get_local_model()

        while True:
            user_input = input("👤: ")
            prompt = self.prompts.context_prompt(user_input)
            response = stream(prompt, tokenizer, model, device)
            asyncio.run(self.consume_stream(response))
            torch.cuda.empty_cache()

    async def consume_stream(self, stream):
        async for line in stream:
            print(f"{line}", end="", flush=True)
        print()
