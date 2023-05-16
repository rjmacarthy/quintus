import torch

from inference.local.model import get_model
from templates.prompts import Prompts
from transformers import GenerationConfig


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class Classifier:
    def __init__(self):
        self.prompts = Prompts()
        model, tokenizer = get_model()
        self.model = model.to(device)
        self.tokenizer = tokenizer

    def run(self, input_text: str):
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt").to(device)

        with torch.no_grad():
            generation_config = GenerationConfig(
                temperature=0.1,
                top_p=0.75,
                top_k=40,
                num_beams=4,
                stream_output=False,
            )

        generation_output = self.model.generate(
            generation_config=generation_config,
            input_ids=input_ids,
            return_dict_in_generate=True,
            output_scores=True,
            max_new_tokens=124,
        )
        s = generation_output.sequences[0]
        output = self.tokenizer.decode(s)
        return output.split("### Response:")[1].strip()
