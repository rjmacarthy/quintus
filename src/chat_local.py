from model import get_model
from config import config
from processor import Processor
from stream import stream
from store import Store
import sys
import json
import gc
import torch
from pathlib import Path
import asyncio

parent_dir = Path(__file__).resolve().parent.parent

sys.path.append(str(parent_dir))


cwd = Path(__file__).resolve().parent
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model, tokenizer = get_model(config)
document_store = Store(model_name="sentence-transformers/all-mpnet-base-v2")


def clear_torch_cache():
    gc.collect()
    torch.cuda.empty_cache()


def get_prompt(question):
    result = document_store.search(question, top_k=1)
    with open(f"data/article{result[0]['doc_id']}.json") as f:
        document = json.load(f)

    processor = Processor()

    prompt = f"""
    You are a helpful AI assistant who can answer questions about the following article:
    {processor.to_text(document)}
    Give a detailed answer to the following question:
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
