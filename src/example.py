from dotenv import load_dotenv

load_dotenv()

from store import Store

ds = Store()

documents = ds.search("How to sign up?")

for document in documents:
    print(document.doc_id, document.doc_text)
