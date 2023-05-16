from pathlib import Path
from peft import PeftModel
from transformers import LlamaTokenizer, LlamaForCausalLM  # TODO support other models
import torch

from database.repository import Repository
from database.schema.config import LocalModelConfig


class LocalModel:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        conig_repository = Repository(LocalModelConfig)
        self.config = conig_repository.get_first()

        if not self.model:
            self.load_model()
        if not self.tokenizer:
            self.load_tokenizer()

    def get_instance(self):
        return self.model, self.tokenizer

    def load_model(self):
        models_dir = Path(__file__).parent.parent.parent / "models"
        model_path = models_dir / self.config.model_name_or_path
        ft_model_path = models_dir / self.config.ft_model_name_or_path

        self.model = LlamaForCausalLM.from_pretrained(
            model_path,
            load_in_8bit=True,
            torch_dtype=torch.float16,
            device_map="auto",
        )

        self.model = PeftModel.from_pretrained(
            self.model, ft_model_path, device_map={"": 0}, torch_dtype=torch.float16
        )

    def load_tokenizer(self):
        models_dir = Path(__file__).parent.parent.parent / "models"
        model_path = models_dir / self.config.model_name_or_path
        self.tokenizer = LlamaTokenizer.from_pretrained(model_path)
