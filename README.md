## Quintus

Quintus is a Python package that enables you to quickly and easily build conversational AI chatbots. It's designed to be easy to use and allows you to customize the chatbot to suit your specific needs. 

### Installation

You can install Quintus using pip:

```bash
pip install quintus
```

### Usage

Here's an example of how you can use Quintus to build a chatbot that interacts with the OpenAI API:

```python
from quintus import Quintus

quintus = Quintus()

quintus.scrape().injest().chat("openai")
```

In this example, `quintus` is a new instance of the `Quintus` class. We use the `scrape()` method to scrape relevant data from the web, and then `injest()` method to process and store the data. Finally, we call the `chat()` method and pass in the string "openai" to initiate a conversation with the OpenAI API.

### Using Local Models

You can also use local models with Quintus. To do so, add the models to your `models` directory, and then call the `add_local_model()` method. Here's an example:

```python
from quintus import Quintus

quintus = Quintus()

quintus.add_local_model("llama-7b", "llama-7b-ft").chat("local")
```

In this example, we've added a local model called "llama-7b". The `add_local_model()` method takes two arguments: the name of the model and the path to the model's directory. Finally, we call the `chat()` method and pass in the string "local" to initiate a conversation with the local model.

### Notes

Please note that this project is in very early stages, is unstable, and subject to large changes.
