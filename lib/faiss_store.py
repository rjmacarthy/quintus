from pathlib import Path
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

import faiss
import json
import pickle
import pydash as _
import numpy as np
import torch

from encoder import Encoder
from processor import Processor


class FaissStore:
    def __init__(self,
                 model_name,
                 data_dir='data',
                 chunk_size=1500,
                 parser='html.parser',
                 index_name='docs.index',
                 store_name='faiss_store.pkl'
                 ):
        self.model = SentenceTransformer(model_name)
        self.store = faiss.IndexFlatIP(768)
        self.device = torch.device(
            'cuda:0' if torch.cuda.is_available() else 'cpu')
        self.chunk_size = chunk_size
        self.parser = parser
        self.data_dir = Path(data_dir)
        self.encoder = Encoder(model_name)
        self.processor = Processor()
        self.index_name = index_name
        self.store_name = store_name
        self.doc_id_to_text = {}

    def load_store(self):
        with open(self.store_name, "rb") as f:
            self.store = pickle.load(f)

    def _add_to_index(self,embedding):
        self.store.add(embedding.reshape(1, -1))


    def index_documents(self):
        json_files = sorted(list(self.data_dir.glob('*.json'))) 
        for idx, file in enumerate(tqdm(json_files, desc='Processing JSON files')):
            with open(file) as f:
                doc = json.load(f)
                doc_text = self.processor.process(doc)
                embedding = self.encoder.encode(doc_text)
                self.doc_id_to_text[idx] = doc_text
                self._add_to_index(embedding)

        faiss.write_index(self.store, self.index_name)
        self.store.index = None

        with open(self.store_name, "wb") as f:
            pickle.dump(self.store, f)

    def search(self, query, k=10):
        self.model.to(self.device)
        with torch.no_grad():
            query_embedding = self.model.encode(query, device=self.device)
        self.store.nprobe = 1
        distances, indices = self.store.search(
            query_embedding.reshape(1, -1), k)
        indices = indices[0]
        distances = distances[0]
        results = []
        for idx, dist in zip(indices, distances):
            if idx in self.doc_id_to_text:  # retrieve text based on doc ID mapping
                doc_text = self.doc_id_to_text[idx]
                results.append({
                    'id': idx,
                    'text': doc_text,
                    'score': float(dist),
                })
        return results
