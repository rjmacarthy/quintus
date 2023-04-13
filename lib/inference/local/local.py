import torch
import asyncio

from inference.local.model import get_local_model
from inference.local.stream import stream

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


async def consume_stream(stream):
    async for line in stream:
        print(f"{line}", end="", flush=True)
    print()


def chat(prompts):
    model, tokenizer = get_local_model()

    while True:
        user_input = input("👤: ")
        prompt = prompts.context_prompt(user_input)
        response = stream(prompt, tokenizer, model, device)
        asyncio.run(consume_stream(response))
        torch.cuda.empty_cache()
