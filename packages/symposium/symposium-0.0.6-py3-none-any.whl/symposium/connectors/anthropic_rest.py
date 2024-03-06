# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""

from os import environ
from typing import List, Dict
import requests

api_key             = environ.get("ANTHROPIC_API_KEY")

organization        = environ.get("ANTHROPIC_ORGANIZATION", "")
api_base            = environ.get("ANTHROPIC_API_BASE", "https://api.anthropic.com/v1")
api_type            = environ.get("ANTHROPIC_VERSION", "2023-06-01")
default_model       = environ.get("ANTHROPIC_DEFAULT_MODEL", "claude-instant-1.2")
completion_model    = environ.get("ANTHROPIC_COMPLETION_MODEL",'claude-instant-1.2')
message_model       = environ.get("ANTHROPIC_MESSAGE_MODEL",'claude-2.0')

HUMAN_PREFIX        = "\n\nHuman:"
MACHINE_PREFIX      = "\n\nAssistant:"

headers = {
    "x-api-key": api_key,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}


def claud_complete(prompt, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    responses = []
    json_data = {
        "model":                kwargs.get("model", completion_model),
        "max_tokens_to_sample": kwargs.get("max_tokens", 5),
        "prompt":               f"{HUMAN_PREFIX}{prompt}{MACHINE_PREFIX}",
        "stop_sequences":       kwargs.get("stop_sequences",[HUMAN_PREFIX]),
        "temperature":          kwargs.get("temperature", 0.5),
        "top_k":                kwargs.get("top_k", 250),
        "top_p":                kwargs.get("top_p", 0.5)
    }
    try:
        response = requests.post(
            f"{api_base}/complete",
            headers=headers,
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            obj = response.json()
            item = {"index": 0,
                    "author": "model",
                    "content": obj['completion'],
                    "stop_reason": obj['stop_reason']}
            responses.append(item)
        else:
            print(f"Request status code: {response.status_code}")
        return responses
    except Exception as e:
        print("Unable to generate Completions response")
        print(f"Exception: {e}")
        return responses


def claud_message(messages, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    responses = []
    json_data = {
        "model":                kwargs.get("model", message_model),
        "system":               kwargs.get("system", "answer concisely"),
        "messages":             kwargs.get("messages", messages),
        "max_tokens":           kwargs.get("max_tokens", 5),
        "stop_sequences":       kwargs.get("stop_sequences",['stop', HUMAN_PREFIX]),
        "stream":               kwargs.get("stream", False),
        "temperature":          kwargs.get("temperature", 0.5),
        "top_k":                kwargs.get("top_k", 250),
        "top_p":                kwargs.get("top_p", 0.5)
    }
    try:
        response = requests.post(
            f"{api_base}/messages",
            headers=headers,
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            obj = response.json()
            item = {"index": 0,
                    "author": "model",
                    "content": obj['content'][0]['text'],
                    "stop_reason": obj['stop_reason']
                    }
            responses.append(item)
        else:
            print(f"Request status code: {response.status_code}")
        return responses
    except Exception as e:
        print("Unable to generate Message response")
        print(f"Exception: {e}")
        return responses


if __name__ == "__main__":
    # completion = claud_complete( "I am Alex")
    # claude-3-opus-20240229, claude-3-sonnet-20240229
    messages = [
        {"role": "user", "content": "I am Alex"}
    ]
    kwa = {
        # "model": "claude-3-opus-20240229",
        "temperature": 0.5,
        "max_tokens": 10,
    }
    msg = claud_message(messages, **kwa)
    print("ok")