from komodo.framework.komodo_tool import KomodoTool
from komodo.models.framework.assistant import AssistantRequest, AssistantResponse
from komodo.models.openai.openai_process_actions import process_actions_gpt_legacy_api
from komodo.shared.utils.sentry_utils import sentry_trace


def openai_chat_response_with_client(client, request: AssistantRequest) -> AssistantResponse:
    messages = []
    messages.append({'role': 'system', "content": request.instructions()})
    # messages.append({'role': 'system', "content": request.preferences()})
    # messages.append({'role': 'system', "content": request.special_requests()})

    tools = request.tools()
    metadata = {}
    if request.user:
        metadata['user_id'] = request.user['email']
        metadata['name'] = request.user['name']
    if request.assistant:
        metadata['agent_id'] = request.assistant['shortcode']

    output_format = None
    if request.assistant and 'output_format' in request.assistant:
        output_format = request.assistant['output_format']

    return openai_invoke(client, request.model(), request.prompt, tools, messages, metadata, output_format)


@sentry_trace
def openai_invoke(client, model, prompt, tools=None, messages=None, metadata=None,
                  output_format=None) -> AssistantResponse:
    response = invoke_text_model(client, model, prompt,
                                 tools=tools,
                                 messages=messages,
                                 metadata=metadata,
                                 output_format=output_format)
    text = response.choices[0].message.content
    status = response.choices[0].finish_reason
    return AssistantResponse(model=model, status=status, output=response, text=text)


def get_definitions(tools):
    definitions = []
    for t in tools or []:
        if isinstance(t, str):
            definitions.extend(get_tools([t]))
        elif isinstance(t, dict) and 'definition' in t:
            definitions.append(t['definition'])
        elif isinstance(t, KomodoTool):
            definitions.append(t.definition)
        else:
            raise ValueError(f"Invalid tool: {t}")
    return definitions


def invoke_text_model(client, model, prompt, tools=None, messages=None, metadata=None, output_format=None):
    messages = messages or []
    messages.append({'role': 'user', "content": prompt})
    params = {
        "model": model,
        "messages": messages
    }

    definitions = get_definitions(tools)
    if tools and len(tools) > 0:
        params['tools'] = definitions

    if output_format and len(output_format) > 0 and 'json' in output_format:
        params['response_format'] = {"type": "json_object"}

    response = client.chat.completions.create(**params)
    response_message = response.choices[0].message
    messages.append(response_message)

    tool_calls = response_message.tool_calls
    while tool_calls:
        outputs = process_actions_gpt_legacy_api(response, metadata, tools)
        for output in outputs:
            messages.append(output)

        response = client.chat.completions.create(model=model, messages=messages, tools=definitions)
        response_message = response.choices[0].message
        messages.append(response_message)
        tool_calls = response_message.tool_calls

    return response
