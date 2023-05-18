import json
import os
import unittest

import sys

sys.path.append("src")

from lib.quintus import Quintus

model_name = os.environ.get("EMBEDDING_MODEL")


class TestStore(unittest.TestCase):
    def setUp(self):
        self.data_dir = "test_data"
        self.parser = "html.parser"

        self.document_store = Quintus(
            data_dir=self.data_dir,
            db_name="test_embeddings",
        )

        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)

        samples = [
            {
                "id": 123,
                "body": "<html><body>This is a sample article.</body></html>",
            },
            {
                "id": 456,
                "body": "<html><body>This is another document.</body></html>",
            },
        ]

        for sample in samples:
            with open(os.path.join(self.data_dir, f'{sample["id"]}.json'), "w") as f:
                json.dump(sample, f)

    def tearDown(self):
        self.document_store.document_repository.delete_all()

    def test_index_documents(self):
        self.document_store.index()
        docs = self.document_store.search("article")
        self.assertEqual(len(docs), 2)


if __name__ == "__main__":
    unittest.main()
