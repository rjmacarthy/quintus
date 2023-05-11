from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from utils.processor import Processor


class Summarization:
    def __init__(self, model_name):
        self.model_name = model_name
        self.processor = Processor()

    def run(self, text):
        words = " ".join(text.split(" ")[:1000])
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        string = self.processor.process(words)
        inputs = tokenizer.encode(string, return_tensors="pt")

        summary_ids = model.generate(
            inputs,
            min_length=50,
            max_new_tokens=200,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True,
        )
        summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True)
        return summary[0]
