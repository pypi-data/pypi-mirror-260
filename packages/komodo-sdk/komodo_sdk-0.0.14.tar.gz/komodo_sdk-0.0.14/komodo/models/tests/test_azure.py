from json import dumps

import pytest

from komodo.models.azure.azure_openai import azure_openai_invoke
from komodo.models.framework.models import AZURE_OPENAI_GPT35_MODEL, AZURE_OPENAI_GPT4_MODEL
from komodo.shared.tools.web.action_tavily_search import TAVILY_SEARCH_ACTION_NAME

TEST_PROMPT = """
### Identity
Act as a writer for a medium blog post with a funny side.

### Objective
Write a medium blog post on how to use Amazon Bedrock 
to write an article on how to use Bedrock.

### Response Format
Respond in HTML format
"""


@pytest.mark.skip(reason="This test is too slow")
def test_azure_completion():
    response = azure_openai_invoke(prompt=TEST_PROMPT)
    print(response)


def test_azure_completion_with_model():
    prompt = 'Write a tagline for an ice cream shop.'
    response = azure_openai_invoke(prompt=prompt, model=AZURE_OPENAI_GPT35_MODEL)
    print(dumps(response, default=vars))


@pytest.mark.skip(reason="This test is too slow")
def test_azure_completion_with_gpt4():
    prompt = 'Write a tagline for an ice cream shop.'
    response = azure_openai_invoke(prompt=prompt, model=AZURE_OPENAI_GPT4_MODEL)
    print(dumps(response, default=vars))


@pytest.mark.skip(reason="This test is too slow")
def test_azure_completion_with_search():
    prompt = 'What is the latest news today?'
    actions = [TAVILY_SEARCH_ACTION_NAME]
    response = azure_openai_invoke(prompt=prompt, model=AZURE_OPENAI_GPT35_MODEL, actions=actions)
    print(response)
