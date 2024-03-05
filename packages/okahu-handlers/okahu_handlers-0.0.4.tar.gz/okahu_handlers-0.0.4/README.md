# Okahu callback handler

This package provides okahu callback handler for tracing callbacks in langchain.

## Installing the package
```
> python3 -m pip install pipenv

> pipenv install okahu-handlers
```

## References

[Managing application dependencies](https://packaging.python.org/en/latest/tutorials/managing-dependencies/)

## Usage
```python
from okahu_handlers.langchain.callback import OkahuCallbackHandler
from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

# Set the OKAHU_API_KEY environment variable, if not set already
os.environ["OKAHU_API_KEY"] = "okh_XXXXXXXX_XXXXXXXXXXXXXXXXXXXXXX"

# Create the callback using the constructor
handler = OkahuCallbackHandler(app_name="my_langchain_app")()
llm = OpenAI()
prompt = PromptTemplate.from_template("1 + {number} = ")

# Constructor callback: First, let's explicitly set the OkahuCallbackHandler when initializing our chain
chain = LLMChain(llm=llm, prompt=prompt, callbacks=[handler])
chain.invoke({"number":2})

# Request callbacks: Finally, let's use the request `callbacks` to achieve the same result
chain = LLMChain(llm=llm, prompt=prompt)
chain.invoke({"number":2}, {"callbacks":[handler]})
    
```

