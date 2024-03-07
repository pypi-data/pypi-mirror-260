# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""


def gemini_get_client():
    client = None
    try:
        import google.generativeai as genai
        client = genai.GenerativeModel('gemini-pro'
            # defaults to os.environ.get("GOOGLE_API_KEY")
        )
    except ImportError:
        print("openai package is not installed")

    return client


def gemini_content(client, **kwargs):
    """ All parameters should be in kwargs, but they are optional
    """
    response = client.generate_content("What is the meaning of life?")
    return response


if __name__ == "__main__":
    print("you launched main.")