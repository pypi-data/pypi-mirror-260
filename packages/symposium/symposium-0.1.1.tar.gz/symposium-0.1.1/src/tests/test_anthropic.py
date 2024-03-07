# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import dotenv
dotenv.load_dotenv()
import symposium.connectors.anthropic as ant
import pytest


@pytest.fixture
def anthropic_client():
    return ant.get_claud_client()


def test_claud_complete(anthropic_client):
    completion = ant.claud_complete(client=anthropic_client, prompt="I am Alex")
    assert completion is not None
