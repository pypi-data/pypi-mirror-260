# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ


api_key             = environ.get("OPENAI_API_KEY")
api_key_path        = environ.get("OPENAI_API_KEY_PATH")

organization        = environ.get("OPENAI_ORGANIZATION")
organization_id     = environ.get("OPENAI_ORGANIZATION_ID")
api_base            = environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
api_type            = environ.get("OPENAI_API_TYPE", "open_ai")
default_model       = environ.get("OPENAI_DEFAULT_MODEL", "gpt-3.5-turbo")
completion_model    = environ.get("OPENAI_COMPLETION_MODEL",'gpt-3.5-turbo-instruct')
embedding_model     = environ.get("OPENAI_EMBEDDING_MODEL",'text-embedding-ada-002')  # text-similarity-davinci-001


def get_openai_client():
    client = None
    try:
        import openai
        client = openai.OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            # api_key="api_key",
        )
    except ImportError:
        print("openai package is not installed       pip install symposium[openai]")

    return client


def openai_complete(client, prompt, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    completion = None
    try:
        completion = client.completions.create(
            model           =kwargs.get("model", completion_model),
            max_tokens      =kwargs.get("max_tokens_to_sample", 5),
            prompt          =kwargs.get("prompt", prompt),
            suffix          =kwargs.get("suffix", None),
            stop            =kwargs.get("stop_sequences",["stop"]),
            n               =kwargs.get("n", 1),
            best_of         =kwargs.get("best_of", 1),
            seed            =kwargs.get("seed", None),
            frequency_penalty=kwargs.get("frequency_penalty", None),
            presence_penalty=kwargs.get("presence_penalty", None),
            logit_bias      =kwargs.get("logit_bias", None),
            logprobs        =kwargs.get("logprobs", None),
            temperature     =kwargs.get("temperature", 0.5),
            top_p           =kwargs.get("top_p", 0.5),
            user            =kwargs.get("user", None)
        )
    except Exception as e:
        print(e)
    return completion


def openai_message(client, messages, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    msg = None
    try:
        msg = client.chat.completions.create(
            model           =kwargs.get("model", default_model),
            messages        =messages,
            max_tokens      =kwargs.get("max_tokens_to_sample", 5),
            stop            =kwargs.get("stop_sequences", ["stop"]),
            response_format =kwargs.get("response_format", None),
            tools           =kwargs.get("tools", None),
            tool_choice     =kwargs.get("tool_choice", None),
            seed            =kwargs.get("seed", None),
            frequency_penalty=kwargs.get("frequency_penalty", None),
            presence_penalty=kwargs.get("presence_penalty", None),
            logit_bias      =kwargs.get("logit_bias", None),
            logprobs        =kwargs.get("logprobs", None),
            top_logprobs    =kwargs.get("top_logprobs", None),
            temperature     =kwargs.get("temperature", 0.5),
            top_p           =kwargs.get("top_p", 0.5),
            user            =kwargs.get("user", None)
        )
    except Exception as e:
        print(e)
    return msg


if __name__ == "__main__":
    client = get_openai_client()
    completion = openai_complete(client, "I am Alex")
    print("ok")