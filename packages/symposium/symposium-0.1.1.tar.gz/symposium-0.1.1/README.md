# Symposium
Interactions with multiple language models require at least a little bit of a 'unified' interface. The 'symposium' packagee is an attempt to do that. It is a work in progress and will change without notice.
## Anthropic
Import:
```python
from symposium.connectors import anthropic_rest as ant
```
#### Messages
```python
messages = [
  {"role": "user", "content": "Can we change human nature?"}
    
]
kwargs = {
    "model":                "claude-3-sonnet-20240229",
    "system":               "answer concisely",
    # "messages":             [],
    "max_tokens":           5,
    "stop_sequences":       ["stop", ant.HUMAN_PREFIX],
    "stream":               False,
    "temperature":          0.5,
    "top_k":                250,
    "top_p":                0.5
}
response = ant.claud_message(messages,**kwargs)
```
#### Completion
```python
prompt = "Can we change human nature?"
kwargs = {
    "model":                "claude-instant-1.2",
    "max_tokens":           5,
    # "prompt":               prompt,
    "stop_sequences":       [ant.HUMAN_PREFIX],
    "temperature":          0.5,
    "top_k":                250,
    "top_p":                0.5
}
response = ant.claud_complete(prompt, **kwargs)
```
## OpenAI
Import:
```python
from symposium.connectors import openai_rest as oai
```
#### Messages
```python
messages = [
  {"role": "user", "content": "Can we change human nature?"}
]
kwargs = {
    "model":                "gpt-3.5-turbo",
    # "messages":             [],
    "max_tokens":           5,
    "n":                    1,
    "stop_sequences":       ["stop"],
    "seed":                 None,
    "frequency_penalty":    None,
    "presence_penalty":     None,
    "logit_bias":           None,
    "logprobs":             None,
    "top_logprobs":         None,
    "temperature":          0.5,
    "top_p":                0.5,
    "user":                 None
}
responses = oai.gpt_message(messages, **kwargs)
```
#### Completion
```python
prompt = "Can we change human nature?"
kwargs = {
    "model":                "gpt-3.5-turbo-instruct",
    # "prompt":               str,
    "suffix":               str,
    "max_tokens":           5,
    "n":                    1,
    "best_of":              None,
    "stop_sequences":       ["stop"],
    "seed":                 None,
    "frequency_penalty":    None,
    "presence_penalty":     None,
    "logit_bias":           None,
    "logprobs":             None,
    "top_logprobs":         None,
    "temperature":          0.5,
    "top_p":                0.5,
    "user":                 None
}
responses = oai.gpt_complete(prompt, **kwargs)
```
## Gemini
Import:
```python
from symposium.connectors import gemini_rest as gem
```
#### Messages
```python
messages = [
        {
            "role": "user",
            "parts": [
                {"text": "Human nature can not be changed, because..."},
                {"text": "...and that is why human nature can not be changed."}
            ]
        },{
            "role": "model",
            "parts": [
                {"text": "Should I synthesize a text that will be placed between these two statements and follow the previous instruction while doing that?"}
            ]
        },{
            "role": "user",
            "parts": [
                {"text": "Yes, please do."},
                {"text": "Create a most concise text possible, preferably just one sentence}"}
            ]
        }
]
kwargs = {
    "model":                "gemini-1.0-pro",
    # "messages":             [],
    "stop_sequences":       ["STOP","Title"],
    "temperature":          0.5,
    "max_tokens":           5,
    "n":                    1,
    "top_p":                0.9,
    "top_k":                None
}
response = gem.gemini_content(messages, **kwargs)
```
 
## PaLM
Import:
```python
from symposium.connectors import palm_rest as path
```
#### Completion
```python
kwargs = {
    "model": "text-bison-001",
    "prompt": str,
    "temperature": 0.5,
    "n": 1,
    "max_tokens": 10,
    "top_p": 0.5,
    "top_k": None
}
responses = path.palm_complete(prompt, **kwargs)
```
#### Messages
```python
context = "This conversation will be happening between Albert and Niels"
examples = [
        {
            "input": {"author": "Albert", "content": "We didn't talk about quantum mechanics lately..."},
            "output": {"author": "Niels", "content": "Yes, indeed."}
        }
]
messages = [
        {
            "author": "Albert",
            "content": "Can we change human nature?"
        }, {
            "author": "Niels",
            "content": "Not clear..."
        }, {
            "author": "Albert",
            "content": "Seriously, can we?"
        }
]
kwargs = {
    "model": "chat-bison-001",
    # "context": str,
    # "examples": [],
    # "messages": [],
    "temperature": 0.5,
    # no 'max_tokens', beware the effects of that!
    "n": 1,
    "top_p": 0.5,
    "top_k": None
}
responses = path.palm_content(context, examples, messages, **kwargs)
```