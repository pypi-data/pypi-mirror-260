<img width="326" alt="Group 311 (2)" src="https://github.com/bananaml/fructose/assets/44653944/8162425c-a485-460f-b816-bcc6be5d2cef">


# LLM calls as strongly-typed functions

Fructose is a python package to create a dependable, strongly-typed interface around an LLM call.

Just slap the `@ai()` decorator on a type-annotated function and call it as you would a function. It's lightweight, syntactic sugar.

``` python
from fructose import Fructose
ai = Fructose()

@ai()
def describe(animals: list[str]) -> str:
  """
  Given a list of animals, use one word that'd describe them all.
  """

description = describe(["dog", "cat", "parrot", "goldfish"])
print(description) # -> "pets" type: str
```
The `@ai()` decorator introspects the function and builds a prompt to an LLM to perform the task whenever the function is invoked.

Fructose supports:
- args, kwargs, and return types
- primative types `str` `bool` `int` `float`
- compound types `list` `dict` `tuple` `Enum` `Optional`
- complex datatypes `@dataclass`
- nested types
- custom prompt templates
- local function calling

# 
## Installation
``` bash
pip3 install fructose
```

It currently executes the prompt with OpenAI, so you'll need to use your own OpenAI API Key
``` bash
export OPENAI_API_KEY=sk-abcdefghijklmnopqrstuvwxyz
```

## Features

### Complex DataTypes

``` python
from fructose import Fructose
from dataclasses import dataclass

ai = Fructose()

@dataclass
class Person:
    name: str
    hobbies: str
    dislikes: str
    obscure_inclinations: str
    age: int
    height: float
    is_human: bool

@ai()
def generate_fake_person_data() -> Person:
  """
    Generate fake data for a cliche aspiring author
  """

person = generate_fake_person_data()
print(person)
```

### Local Function Calling

Fructose `ai()` functions can choose to call local Python functions. Yes, even other `@ai()` functions.

Pass the functions into the decorator with the `uses` argument: `@ai(uses = [func_1, func_2])`

For example, here's a fructose function fetching HackerNews comments using a local function and the `requests` library:

``` python
from fructose import Fructose
import requests
from dataclasses import dataclass

ai = Fructose()

def get(uri: str) -> str:
    """
    GET request to a URI
    """
    return requests.get(uri).text

@dataclass
class Comment:
    username: str
    comment: str

@ai(uses=[get], debug=True)
def get_comments(uri: str) -> list[Comment]:
    """
    Gets all base comments from a hacker news post
    """
    

result = get_comments("https://news.ycombinator.com/item?id=22963649")

for comment in result:
    print(f"🧑 {comment.username}: \n💬 {comment.comment}\n")
```

Local function calling currently requires:
- type annotations on the function
- docstring on the function
- sane variable names for arguments
  
And supports arguments of basic types:
- `str` `bool` `int` `float` and `list`

## Customizing prompts via Flavors and your own templates

Fructose has a lightweight prompt wrapper that "just works" in most cases, but you're free to modify it. 

Note: This is an area of the API we're still figuring out, feel free to give your own suggestions.

### Flavors

Flavors are optional flags to change the behavior of the prompt.
- `random`: adds a random seed into the system prompt, to add a bit more variability
- `chain_of_thought`: splits calls into two steps: chain of thought for reasoning, then the structured generation.

You can set these on the decorator level:
```python
ai = Fructose(["random", "chain_of_thought"])
```

Or on the function level:
```python
@ai(flavors=["random", "chain_of_thought"])
def my_func():
    # ...
```

### Custom System Prompt Templates

You're free to bring your own prompt template, using the Jinja templating language.

To use a custom template on a function level, use the `system_template_path` argument in the `@ai()` decorator, with a relative path to your Jinja template file:

```python
@ai(system_template_path="relative/path/to/my_template.jinja")
def my_func():
    # ...
```

You can also set this on the decorator level, to make it default for all decorated functions.

The template must include the following variables:
-  `func_doc_string`: the docstring from the decorated function
-  `return_type_string`: the string-representation of the function's return types

For reference, here's the default Jinja template:

```jinja
You are an AI assistant tasked with the following problem:

{{ func_doc_string|trim() }}

The user will provide you with a dictionary object with any necessary arguments to solve the problem (Note that the json object may be empty). 

Your response should be in the following format: {{ return_type_string|trim() }}.

Answer with JSON in this format: 
{{ '{' }}
    \"response\": <your final answer in the format requested: {{ return_type_string|trim() }}>
{{ '}' }}
```

### Custom Chain Of Thought Prompt Templates

In the case of the `chain_of_thought` flavor being used, fructose will first run a chain-of-thought call, using a special system prompt. 

Customize it on the function level with the `chain_of_thought_template_path` argument in the `@ai()` decorator.

```python
@ai(
    flavors = ["chain_of_thought"], 
    chain_of_thought_template_path="relative/path/to/my_template.jinja"
)
def my_func():
    # ...
```

You can also set this on the decorator level, to make it default for all decorated functions.

---

### Stability

We are in v0, meaning the API is unstable version-to-version. Pin your versions to ensure new builds don't break!
Also note... since LLM generations are nondeterminsitic, the calls may break too!

### To develop

From the root of this repo:

Create a virtual env
``` bash
python3 -m venv venv
. ./venv/bin/activate
```

Install fructose into your pip environment with:
``` bash
pip3 install -e .
```
This installs the fructose package in editable mode. All imports of fructose will run the fructose source at `./src/fructose` directly.

Under /examples you'll find different usage examples. And run them like so:
``` bash
python3 examples/fake_data.py
```

Run tests with:
``` bash
python3 -m pytest
```
