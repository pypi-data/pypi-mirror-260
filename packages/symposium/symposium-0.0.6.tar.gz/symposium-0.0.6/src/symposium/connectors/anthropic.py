# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""

HUMAN_PREFIX = "\n\nHuman:"
MACHINE_PREFIX = "\n\nAssistant:"


def get_claud_client():
    client = None
    try:
        import anthropic
        client = anthropic.Anthropic(
            # defaults to os.environ.get("ANTHROPIC_API_KEY")
            # api_key="my_api_key",
        )
    except ImportError:
        print("anthropic package is not installed")

    return client


def claud_complete(client, prompt, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    completion = None
    try:
        completion = client.completions.create(
            model=kwargs.get("model", "claude-instant-1.2"),
            max_tokens_to_sample=kwargs.get("max_tokens_to_sample", 5),
            prompt=f"{HUMAN_PREFIX}{prompt}{MACHINE_PREFIX}",
            stop_sequences=kwargs.get(
                "stop_sequences",
                [HUMAN_PREFIX, MACHINE_PREFIX]),
            temperature=kwargs.get("temperature", 0.5),
            top_k=kwargs.get("top_k", 250),
            top_p=kwargs.get("top_p", 0.5)
        )
    except Exception as e:
        print(e)
    return completion


def claud_message(client, messages, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    msg = None
    try:
        msg = client.messages.create(
            model=kwargs.get("model", "claude-2.0"),
            system=kwargs.get("system", None),
            messages=messages,
            max_tokens=kwargs.get("max_tokens", 1),
            stop_sequences=kwargs.get(
                "stop_sequences",
                [HUMAN_PREFIX, MACHINE_PREFIX]),
            stream=kwargs.get("stream", False),
            temperature=kwargs.get("temperature", 0.5),
            top_k=kwargs.get("top_k", 250),
            top_p=kwargs.get("top_p", 0.5)
        )
    except Exception as e:
        print(e)
    return msg


if __name__ == "__main__":
    client = get_claud_client()
    completion = claud_complete(client, "I am Alex")
    print(completion.completion)