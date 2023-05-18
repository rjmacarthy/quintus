## Quintus

Quintus is a Python package that enables you to quickly and easily build conversational Q&A chatbots using semantic search and LLM inference. It's designed to be easy to use and allows you to customize the chatbot to suit your specific needs. As time goes on, new loaders will be added to enhance its functionality. Currently, the available loaders support classification, named entity recognition, summarization, and more.

### Installation

The best way is to clone the repository and install the dependencies.

### Usage

To get started, you can ingest data using Quintus as shown below:

```python
from quintus import Quintus

quintus = Quintus()

url = "https://postman.zendesk.com/api/v2/help_center/en-us/articles.json"

quintus.injest(url).serve() # Api should be now loaded locally.
```

Please note that this project is still in its early stages and may undergo significant changes. It is recommended to exercise caution when using it in production environments.
