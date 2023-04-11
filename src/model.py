import torch
from transformers import LlamaTokenizer, LlamaForCausalLM
from peft import PeftModel


def get_model(config):
    tokenizer = LlamaTokenizer.from_pretrained(config.model_name)

    model = LlamaForCausalLM.from_pretrained(
        config.model_name,
        load_in_8bit=True,
        torch_dtype=torch.float16,
        device_map="auto",
    )

    model = PeftModel.from_pretrained(
        model, config.ft_model_name, device_map={"": 0}, torch_dtype=torch.float16
    )

    return model, tokenizer
