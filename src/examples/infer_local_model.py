import torch
import asyncio

from inference.local.model import get_model
from inference.local.stream import stream
from src.quintus import Quintus
from database.schema.config import LocalModelConfig
from database.repository import Repository
from templates.prompts import Prompts

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


async def consume_stream(stream):
    async for line in stream:
        print(f"{line}", end="", flush=True)
    print()  # Print a newline at the end


if __name__ == "__main__":
    prompts = Prompts()
    config_repository = Repository(LocalModelConfig)
    config = config_repository.get()
    model, tokenizer = get_model(config)
    quintus = Quintus()
    while True:
        prompt = prompts.context_prompt(input("User: "), quintus)
        response = stream(prompt, tokenizer, model, device)
        asyncio.run(consume_stream(response))
        torch.cuda.empty_cache()
