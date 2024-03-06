# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
from typing import List, Dict
import requests


gemini_key              = environ.get("GOOGLE_API_KEY","") # GEMINI_KEY", "")
gemini_api_base         = "https://generativelanguage.googleapis.com/v1beta"
gemini_content_model    = environ.get("GEMINI_DEFAULT_CONTENT_MODEL", "gemini-1.0-pro")
gemini_embedding_model  = environ.get("GEMINI_DEFAULT_EMBEDDING_MODEL", "embedding-001")


def gemini_content(messages: List,
                   **kwargs) -> List:

    """A completions endpoint call through requests.
        kwargs:
            temperature     = 0 to 1.0
            top_p           = 0.0 to 1.0
            top_k           = The maximum number of tokens to consider when sampling.
            n               = 1 mandatory
            max_tokens      = number of tokens
            stop            = ["stop"]  array of up to 4 sequences
    """
    garbage = [{"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT","threshold": "BLOCK_NONE"},
               {"category": "HARM_CATEGORY_HATE_SPEECH","threshold": "BLOCK_NONE"},
               {"category": "HARM_CATEGORY_HARASSMENT","threshold": "BLOCK_NONE"},
               {"category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_NONE"}
    ]

    responses = []
    json_data = {"contents": kwargs.get("messages", messages),
                 "safetySettings":  garbage,
                 "generationConfig":{
                     "stopSequences":  kwargs.get("stop_sequences", ["STOP","Title"]),
                     "temperature":     kwargs.get("temperature", 0.5),
                     "maxOutputTokens": kwargs.get("max_tokens", 5),
                     "candidateCount":  kwargs.get("n", 1),
                     "topP":            kwargs.get("top_p", 0.9),
                     "topK":            kwargs.get("top_k", None)
                 }
            }
    try:
        url = f"{gemini_api_base}/models/{kwargs.get('model', gemini_content_model)}:generateContent"
        response = requests.post(
            url=url,
            params=f"key={gemini_key}",
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            if response.json().get('filters', None):
                raise Exception('Results filtered')
            else:
                for count, candidate in enumerate(response.json()['candidates']):
                    item = {"index": count,
                            "text": candidate['content']['parts'][0]['text'],
                            "finish_reason": candidate['finishReason'].lower()}
                    responses.append(item)
        else:
            print(f"Request status code: {response.status_code}")
        return responses
    except Exception as e:
        print(f"Unable to generate continuations response, {e}")
        return responses


def gemini_answer(contents: List,
                  **kwargs) -> List:

    """A completions endpoint call through requests.
        kwargs:
            temperature     = 0 to 1.0
            top_p           = 0.0 to 1.0
            top_k           = The maximum number of tokens to consider when sampling.
            n               = 1 mandatory
            max_tokens      = number of tokens
            stop            = ["stop"]  array of up to 4 sequences
    """
    garbage = [{"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT","threshold": "BLOCK_NONE"},
               {"category": "HARM_CATEGORY_HATE_SPEECH","threshold": "BLOCK_NONE"},
               {"category": "HARM_CATEGORY_HARASSMENT","threshold": "BLOCK_NONE"},
               {"category": "HARM_CATEGORY_DANGEROUS_CONTENT","threshold": "BLOCK_NONE"}
    ]

    responses = []
    # answerStyle =
    # ANSWER_STYLE_UNSPECIFIED = 0,
    # ABSTRACTIVE	Succint but abstract style
    # EXTRACTIVE	Very brief and extractive style.
    # VERBOSE       Verbose style including extra details. The response may be formatted as a sentence,
    #               paragraph, multiple paragraphs, or bullet points, etc.
    json_data = {"contents": contents,
                 "answerStyle": 1,
                 "safetySettings":  garbage,
                 "temperature":     kwargs.get("temperature", 0.5)
            }
    try:
        url = f"{gemini_api_base}/models/{kwargs.get('model', gemini_content_model)}:generateAnswer"
        response = requests.post(
            url=url,
            params=f"key={gemini_key}",
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            if response.json().get('filters', None):
                raise Exception('Results filtered')
            else:
                for count, candidate in enumerate(response.json()['candidates']):
                    item = {"index": count,
                            "text": candidate['content']['parts'][0]['text'],
                            "finish_reason": candidate['finishReason'].lower()}
                    responses.append(item)
        else:
            print(f"Request status code: {response.status_code}")
        return responses
    except Exception as e:
        print(f"Unable to generate continuations response, {e}")
        return responses


def gemini_embeddings(input_list: List[str],
                      **kwargs) -> List[Dict]:
    """Returns the embedding of a list of text strings.
    """
    embeddings_list = []
    json_data = {"texts": input_list} | kwargs
    try:
        response = requests.post(
            f"{gemini_api_base}/models/{kwargs.get('model', gemini_embedding_model)}:batchEmbedText",
            params=f"key={gemini_key}",
            json=json_data,
        )
        if response.status_code == requests.codes.ok:
            # embeddings_list = response.json()['embeddings']
            for count, candidate in enumerate(response.json()['embeddings']):
                item = {"index": count, "embedding": candidate['value']}
                embeddings_list.append(item)
        else:
            print(f"Request status code: {response.status_code}")
        return embeddings_list
    except Exception as e:
        print("Unable to generate Embeddings response")
        print(f"Exception: {e}")
        return embeddings_list


if __name__ == '__main__':
    # contents = [
    #     {
    #         "parts": [
    #             {"text": "Create a most concise text possible, preferrably just one sentence, answering the question: Can human nature be changed?"}
    #         ]
    #     }
    # ]
    contents = [
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
    kwa = {
        "temperature": 1.0,
        "max_tokens": 1000,
        "n": 1,
        "top_p": 0.9,
        "top_k": 50
    }

    a = gemini_content(contents=contents, **kwa)
    # contents = [
    #     {
    #         "role": "user",
    #         "parts": [
    #             {"text": "Can human nature be changed?"},
    #         ]
    #     }
    # ]
    # kwa = {
    #     "temperature": 1.0
    # }
    # a = gemini_answer(contents=contents, **kwa)
    print('ok')
