import sys
sys.path.append('lib')

from processor import Processor
from faiss_store import FaissStore
from encoder import Encoder
import unittest
import os
import json


class TestFaissStore(unittest.TestCase):
    def setUp(self):
        self.data_dir = 'test_data'
        self.chunk_size = 50
        self.parser = 'html.parser'
        self.model_name = 'sentence-transformers/all-mpnet-base-v2'
        self.faiss_store = FaissStore(self.model_name, self.data_dir, self.chunk_size,
                                      self.parser, 'test_docs.index', 'test_faiss_store.pkl')

        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)

    def tearDown(self):
        if os.path.exists('test_docs.index'):
            os.remove('test_docs.index')
        if os.path.exists('test_faiss_store.pkl'):
            os.remove('test_faiss_store.pkl')
        if os.path.exists(self.data_dir):
            for file in os.listdir(self.data_dir):
                os.remove(os.path.join(self.data_dir, file))
            os.rmdir(self.data_dir)

    def test_index_documents(self):
        samples = [{
            'id': 123,
            'body': '<html><body>This is a sample article.</body></html>',
        },
            {
            'id': 456,
            'body': '<html><body>This is another document.</body></html>',
        }]
        for sample in samples:
            with open(os.path.join(self.data_dir, f'{sample["id"]}.json'), 'w') as f:
                json.dump(sample, f)

        self.faiss_store.index_documents()
        self.encoder = Encoder(self.model_name)
        self.assertTrue(os.path.exists('test_docs.index'))
        self.assertTrue(os.path.exists('test_faiss_store.pkl'))
        docs = self.faiss_store.search('sample article', 1)
        assert len(
            docs) == 1 and docs[0]['id'] == 0 and docs[0]['score'] > 0.9 and docs[0]['text'] == 'sample article'


if __name__ == '__main__':
    unittest.main()
