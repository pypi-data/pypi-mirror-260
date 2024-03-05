from komodo.core.tools.tool_registry import KomodoToolRegistry
from komodo.models.azure.azure import get_azure_openai_client
from komodo.models.framework.assistant import AssistantResponse, AssistantRequest
from komodo.models.framework.models import AZURE_OPENAI_GPT35_MODEL
from komodo.models.openai.openai_api import openai_chat_response_with_client, openai_invoke
from komodo.shared.utils.sentry_utils import sentry_trace


@sentry_trace
def azure_assistant_response(request: AssistantRequest) -> AssistantResponse:
    client = get_azure_openai_client(request.assistant['model'])
    return openai_chat_response_with_client(client, request)


# model ids are deployment names at Azure OpenAI
@sentry_trace
def azure_openai_invoke(prompt, model=AZURE_OPENAI_GPT35_MODEL, actions=None, messages=None,
                        metadata=None, output_format=None) -> AssistantResponse:
    client = get_azure_openai_client(model)
    tools = KomodoToolRegistry.get_tools(actions)
    return openai_invoke(client, model, prompt, tools, messages, metadata, output_format)
