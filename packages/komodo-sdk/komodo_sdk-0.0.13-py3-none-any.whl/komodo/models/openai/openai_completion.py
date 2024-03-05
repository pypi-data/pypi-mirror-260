import os

from openai import OpenAI

from komodo.models.framework.assistant import AssistantRequest, AssistantResponse
from komodo.models.openai.openai_api import openai_chat_response_with_client
from komodo.models.openai.openai_api_key import fetch_openai_api_key
from komodo.shared.utils.sentry_utils import sentry_trace


def openai_client():
    api_key = os.getenv("OPENAI_API_KEY", None)
    if not api_key:
        api_key = fetch_openai_api_key()
        os.environ["OPENAI_API_KEY"] = api_key

    client = OpenAI(api_key=api_key)
    return client


@sentry_trace
def openai_chat_response(request: AssistantRequest) -> AssistantResponse:
    return openai_chat_response_with_client(openai_client(), request)


def openai_list_assistants():
    return openai_client().beta.assistants.list()


def openai_get_assistant(assistant_id: str):
    return openai_client().beta.assistants.retrieve(assistant_id)


def openai_create_assistant(name: str, model: str, description: str, instructions: str, tools: list,
                            metadata: dict = None):
    return openai_client().beta.assistants.create(name=name, model=model, description=description,
                                                  instructions=instructions, tools=tools, metadata=metadata)


def openai_update_assistant(assistant_id: str, name: str, model: str, description: str, instructions: str, tools: list):
    return openai_client().beta.assistants.update(assistant_id=assistant_id, name=name, model=model,
                                                  description=description, instructions=instructions, tools=tools)


def openai_create_or_update_assistant(name: str, model: str, description: str, instructions: str, tools: list):
    assistant = openai_get_assistant(name)
    if assistant:
        return openai_update_assistant(assistant.id, name, model, description, instructions, tools)

    return openai_client().beta.assistants.create(name=name, model=model, description=description,
                                                  instructions=instructions, tools=tools)


def openai_delete_assistant(assistant_id: str):
    return openai_client().beta.assistants.delete(assistant_id=assistant_id)


if __name__ == "__main__":
    print(openai_get_assistant("asst_gmAV5Z4qx4tu5x4zO5xx9cHy"))
    assistants = openai_list_assistants()
    visualizers = filter(lambda x: x.name == "Data visualizer", assistants.data)
    for v in visualizers:
        print(v)
        print(v.id)
        openai_delete_assistant(v.id)
