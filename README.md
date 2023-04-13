### quintus

```
pip install quintus
```

```
from quintus import Quintus

quintus = Quintus()

quintus.scrape().injest().chat("openai")
```

You can also use local models like Llama, add the models to you `models` directory then call quintus like this.

```
from quintus import Quintus

quintus = Quintus()

quintus.add_local_model("llama-7b", "llama-7b-ft").chat("local")

```

This project is very early stages, unstable and subject to large changes.
