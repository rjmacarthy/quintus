import torch
import asyncio

from local_model import get_model
from inference.stream import stream
from store import Store
from schema.config import LocalModelConfig
from database.repository import Repository
from templates.simple import simple_prompt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

async def consume_stream(stream):
    async for line in stream:
        print(f"{line}", end="", flush=True)
    print()  # Print a newline at the end


if __name__ == "__main__":
    config_repository = Repository(LocalModelConfig)
    config = config_repository.get()
    model, tokenizer = get_model(config)
    store = Store()
    while True:
        prompt = simple_prompt(input("User: "), store)
        response = stream(prompt, tokenizer, model, device)
        asyncio.run(consume_stream(response))
        torch.cuda.empty_cache()
