## LLM Fine Tuning Examples

### [Sentiment Analysis using HuggingFace](https://huggingface.co/docs/transformers/tasks/sequence_classification)

```python
from pdexplorer import *
from pdexplorer.tests.fixtures import yelp_reviews
df = pd.DataFrame.from_records(yelp_reviews)
use(df) # load examples into pdexplorer
fthuggingface("stars text", task="sentiment-analysis", model_name="distilbert-base-uncased") # slow
askhuggingface("I absolutely loved Burgerosity!", task="sentiment-analysis")
```

### [Next Word Prediction using HuggingFace](https://huggingface.co/docs/transformers/tasks/language_modeling)

```python
from pdexplorer import *
from pdexplorer.tests.fixtures import eli5
df = pd.DataFrame.from_records(eli5)
use(df) # load examples into pdexplorer
fthuggingface("text", task="text-generation", model_name="distilgpt2") # slow
askhuggingface("A poem about Mickey Mouse in iambic pentameter:\n", task="text-generation")
```

### [Next Word Prediction using OpenAI (gpt-3.5-turbo)](https://platform.openai.com/docs/guides/fine-tuning/)

```python
from pdexplorer import *
from pdexplorer.tests.test_ftgpt import df
use(df)
ftgpt("assistant user system") # slow; requires OPENAI_API_KEY environment variable
askgpt("A poem about Mickey Mouse in iambic pentameter:\n")
```
