import gc
import torch
import asyncio

from model import get_model
from inference.config import config
from utils.processor import Processor
from inference.stream import stream
from store import Store

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model, tokenizer = get_model(config)
ds = Store()


def clear_torch_cache():
    gc.collect()
    torch.cuda.empty_cache()


def get_prompt(question):
    max_context_length = 500
    print("Searching for context...", question)
    results = ds.search(question)
    text = results[0].doc_text
    processor = Processor()
    context = processor.html_to_text(text)
    context = context[:max_context_length]
    
    prompt = f"""
        You are a helpful AI assistant who answers questions about the followin context.
        {context}
        Give a short but consice answer to the following question using the context above:
        {question}
    """

    return prompt


async def consume_stream(stream):
    async for line in stream:
        print(f"{line}", end="", flush=True)
    print()  # Print a newline at the end


if __name__ == "__main__":
    while True:
        prompt = get_prompt(input("User: "))
        response = stream(prompt, tokenizer, model, device)
        asyncio.run(consume_stream(response))
        torch.cuda.empty_cache()
