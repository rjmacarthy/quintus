import torch
from transformers import LlamaTokenizer, LlamaForCausalLM
from peft import PeftModel
from pathlib import Path


def get_model(config):
    model_path = Path(__file__).parent / config.model_name_or_path
    ft_model_path = Path(__file__).parent / config.ft_model_name_or_path
    tokenizer = LlamaTokenizer.from_pretrained(model_path)

    model = LlamaForCausalLM.from_pretrained(
        model_path,
        load_in_8bit=True,
        torch_dtype=torch.float16,
        device_map="auto",
    )

    model = PeftModel.from_pretrained(
        model, ft_model_path, device_map={"": 0}, torch_dtype=torch.float16
    )

    return model, tokenizer
