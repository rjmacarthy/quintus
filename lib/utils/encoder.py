from sentence_transformers import SentenceTransformer
import torch


class Encoder:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def encode(self, document: str):
        with torch.no_grad():
            embeddings = self.model.encode(document, device=self.device)
            return embeddings
