import torch
import copy
from torch.nn import functional as F
import pydash as _
import torch
import asyncio


async def generate(input_text, tokenizer, model, device, **kwargs):
    input_ids = tokenizer.encode(input_text, return_tensors="pt").to(device)
    max_new_tokens = kwargs.pop("max_new_tokens", 2048)
    batch_size = input_ids.shape[0]
    input_length = input_ids.shape[-1]
    config = model.config
    config = copy.deepcopy(config)
    pad_token_id = config.pad_token_id
    eos_token_id = config.eos_token_id
    consecutive_eos_tokens = 0
    target_consecutive_eos_tokens = 5
    consecutive_line_breaks = 0
    target_consecutive_line_breaks = 2
    line_break_token = 13

    kwargs["output_attentions"] = False
    kwargs["output_hidden_states"] = False
    kwargs["use_cache"] = config.use_cache

    if isinstance(eos_token_id, int):
        eos_token_id = [eos_token_id]

    incomplete_sequences = input_ids.new_ones(batch_size)

    while True:
        outputs = model(input_ids, **kwargs, return_dict=True)

        logits = outputs.logits[:, -1, :]

        with torch.inference_mode():
            logits = logits

        probs = F.softmax(logits.float(), dim=-1)

        tokens = torch.argmax(probs, dim=-1)[:, None]

        token_logprobs = torch.gather(probs, 1, tokens)

        token_logprobs = torch.log(token_logprobs + 1e-7).squeeze(1)

        tokens = tokens.squeeze(1)

        if pad_token_id is not None:
            tokens = tokens * incomplete_sequences + pad_token_id * (
                1 - incomplete_sequences
            )

        input_ids = torch.cat([input_ids, tokens[:, None]], dim=-1)

        if eos_token_id is not None:
            not_eos = torch.all(
                torch.tensor([tokens != i for i in eos_token_id]), dim=0
            ).to(device)
            incomplete_sequences = incomplete_sequences.mul(not_eos.long())

            if tokens.item() == eos_token_id:
                consecutive_eos_tokens += 1
            else:
                consecutive_eos_tokens = 0

            if tokens.item() == line_break_token:
                consecutive_line_breaks += 1
            else:
                consecutive_line_breaks = 0

            if (
                consecutive_eos_tokens >= target_consecutive_eos_tokens
                or consecutive_line_breaks >= target_consecutive_line_breaks
            ):
                break

        status = incomplete_sequences.clone()

        if input_ids.shape[-1] - input_length >= max_new_tokens:
            status = 0 - status

        is_finished = incomplete_sequences.max() == 0

        await asyncio.sleep(0.01)

        yield tokens, is_finished

        if status.max() <= 0:
            break
