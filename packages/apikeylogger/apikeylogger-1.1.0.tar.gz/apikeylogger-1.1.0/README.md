# apikeylogger

Track your *OpenAI* api usage **by key**, without any code change.

#### Installation

```bash
pip install apikeylogger
```

#### Setup
Create a *.env* file with your OpenAI *api key* and *organization id* ([find yours here](https://platform.openai.com/account/organization)), like this:
```bash
OPENAI_API_KEY = ""
OPENAI_ORG_ID = ""
```


#### Usage
```python
# This call will transparently log your API usage by key in a local json file *apikeylogs.json*
from apikeylogger import track_openai
track_openai()

# Your normal code that uses openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

response = client.chat.completions.create(
    messages = [
        {
            "role": "user",
            "content": "What is the meaning of life?",
        }
    ],
    model = "gpt-3.5-turbo-16k" # any model
)
```

#### Test

Run tests with:
```bash
pytest
```
