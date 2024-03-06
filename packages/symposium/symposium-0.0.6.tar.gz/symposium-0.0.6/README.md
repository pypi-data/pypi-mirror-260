# Symposium
Interactions with multiple language models.
## Anthropic
Import:
```python
from symposium.connectors import anthropic_rest as ant
```
#### Messages
```python
kwargs = {
    "model":                "claude-3-sonnet-20240229",
    "system":               "answer concisely",
    "messages":             [],
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
kwargs = {
    "model":                "claude-instant-1.2",
    "max_tokens":           5,
    "prompt":               f"{ant.HUMAN_PREFIX}{prompt}{ant.MACHINE_PREFIX}",
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
kwargs = {
    "model":                "gpt-3.5-turbo",
    "messages":             [],
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
kwargs = {
    "model":                "gpt-3.5-turbo-instruct",
    "prompt":               str,
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
kwargs = {
    "messages":             [],
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
kwargs = {
    "model": "chat-bison-001",
    "context": str,
    "examples": [],
    "messages": [],
    "temperature": 0.5,
    # no 'max_tokens', beware the effects of that!
    "n": 1,
    "top_p": 0.5,
    "top_k": None
}
responses = path.palm_content(messages, **kwargs)
```