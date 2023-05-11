from transformers import AutoTokenizer, AutoModelForTokenClassification
from utils.processor import Processor
from transformers import pipeline


class NamedEntityRecognition:
    def __init__(self, model_name):
        self.model_name = model_name
        self.processor = Processor()

    def process_entities(self, entities):
        processed_entities = {}
        for entity in entities:
            # Concatenate split words
            if entity["entity"] not in processed_entities:
                processed_entities[entity["entity"]] = entity["word"]
            else:
                # If the entity already exists and the current word is part of the same entity (signified by '##')
                if "##" in entity["word"]:
                    processed_entities[entity["entity"]] += entity["word"].replace(
                        "##", ""
                    )
                else:
                    # If it's a new occurrence of the same type of entity, add a separator
                    processed_entities[entity["entity"]] += ", " + entity["word"]

        # Remove duplicates
        for entity, words in processed_entities.items():
            unique_words = list(set(words.split(", ")))
            processed_entities[entity] = ", ".join(unique_words)

        entities_str = ", ".join(
            [f"{entity}:{words}" for entity, words in processed_entities.items()]
        )

        return entities_str

    def run(self, text):
        words = " ".join(text.split(" ")[:1000])
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = AutoModelForTokenClassification.from_pretrained(self.model_name)
        nlp = pipeline("ner", model=model, tokenizer=tokenizer)
        ner_results = nlp(words)
        processed = self.process_entities(ner_results)
        return processed
