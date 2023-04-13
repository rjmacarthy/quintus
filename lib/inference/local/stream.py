import torch
import asyncio
import pydash as _

from inference.local.generate import generate


async def stream(prompt, tokenizer, model, device):
    sequence = torch.empty(0).to(device)
    last_printed_index = 0

    async for token, is_finished in generate(prompt, tokenizer, model, device):
        sequence = torch.cat((sequence, token))
        if token < tokenizer.vocab_size:
            text = tokenizer.decode(sequence, skip_special_tokens=True)
            new_text = text[last_printed_index:]
            yield new_text
            last_printed_index = len(text)
            await asyncio.sleep(0.01)

        if is_finished:
            break
