import torch
from transformers import LlamaTokenizer, LlamaForCausalLM
from peft import PeftModel
from pathlib import Path

from database.repository import Repository
from database.schema.config import LocalModelConfig


def get_local_model():
    conig_repository = Repository(LocalModelConfig)
    config = conig_repository.get_first()
    models_dir = Path(__file__).parent.parent.parent / "models"

    model_path = models_dir / config.model_name_or_path
    ft_model_path = models_dir / config.ft_model_name_or_path

    print(f"Loading model from {model_path}")
    print(f"Loading fine-tuned model from {ft_model_path}")

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
