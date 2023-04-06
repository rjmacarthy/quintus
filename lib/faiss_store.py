from pathlib import Path
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

import faiss
import json
import pickle
import pydash as _
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
                 store_name='faiss_store.pkl',
                 indices_name='doc_id_to_filename.pkl',
                 store_path=None,
                 index_path=None,
                 indices_path = None
                 ):
        self.model = SentenceTransformer(model_name)
        self.store = faiss.IndexFlatIP(768)
        self.indices = {}
        self.device = torch.device(
            'cuda:0' if torch.cuda.is_available() else 'cpu')
        self.chunk_size = chunk_size
        self.parser = parser
        self.data_dir = Path(data_dir)
        self.encoder = Encoder(model_name)
        self.processor = Processor()
        self.index_name = index_name
        self.store_name = store_name
        self.indices_name = indices_name
        self.store_path = store_path
        self.index_path = index_path
        self.indices_path = indices_path
        self.index_to_id = {}

    def load_store(self):
        with open(self.store_path, "rb") as f:
            self.store = pickle.load(f)
        with open(self.indices_path, "rb") as f:
            self.indices = pickle.load(f)
        self.store.index = faiss.read_index(self.index_path)

    def _add_to_index(self,embedding):
        self.store.add(embedding.reshape(1, -1))

    def index_documents(self):
        json_files = sorted(list(self.data_dir.glob('*.json'))) 
        for idx, file in enumerate(tqdm(json_files, desc='Processing JSON files')):
            with open(file) as f:
                doc = json.load(f)
                doc_text = self.processor.process(doc)
                embedding = self.encoder.encode(doc_text)
                self.index_to_id[idx] = str(doc['id'])
                self._add_to_index(embedding)

        faiss.write_index(self.store, self.index_name)
        self.store.index = None

        with open(self.store_name, "wb") as f:
            pickle.dump(self.store, f)
            
        with open(self.indices_name, 'wb') as f:
            pickle.dump(self.index_to_id, f)

    def search(self, query, top_k=1):
        self.model.to(self.device)
        with torch.no_grad():
            query_embedding = self.model.encode(query, device=self.device)
        self.store.nprobe = 1
        distances, indices = self.store.search(query_embedding.reshape(1, -1), top_k)
        results = []
        for i in range(len(_.get(indices, 0))):
            result = {}
            result['score'] = _.get(distances, [0, i], 0.0)
            result['doc_id'] = _.get(self.indices, _.get(indices, [0, i]))
            results.append(result)
        return results