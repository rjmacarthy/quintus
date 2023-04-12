from src.quintus import Quintus
from dotenv import load_dotenv

load_dotenv()

quintus = Quintus()

quintus.injest()

documents = quintus.search("article")

for document in documents:
    print(document.doc_title)
