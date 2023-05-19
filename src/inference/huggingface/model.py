from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class HuggingFaceModel:
    def __init__(
        self,
        model_name="TheBloke/Wizard-Vicuna-7B-Uncensored-HF",
        tokenizer_name="TheBloke/Wizard-Vicuna-7B-Uncensored-HF",
    ):
        self.model = None
        self.tokenizer = None

        if not self.model:
            self.load_model(model_name)
        if not self.tokenizer:
            self.load_tokenizer(tokenizer_name)

    def get_instance(self):
        return self.model, self.tokenizer

    def load_model(self, model_name):
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            load_in_8bit=True,
            torch_dtype=torch.float16,
            device_map="auto",
        )

    def load_tokenizer(self, tokenizer_name):
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
