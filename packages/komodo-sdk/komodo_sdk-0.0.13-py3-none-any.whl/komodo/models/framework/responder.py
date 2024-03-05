import json
import re
from datetime import datetime

import markdown2
from bs4 import BeautifulSoup

from komodo.models.azure.azure_openai import azure_assistant_response
from komodo.models.bedrock.bedrock_model import bedrock_assistant_response
from komodo.models.framework.assistant import AssistantRequest, AssistantResponse, get_default_assistant, \
    get_default_user
from komodo.models.openai.openai_assistant import openai_assistant_response
from komodo.models.openai.openai_completion import openai_chat_response
from komodo.shared.documents.text_html import text_to_html_paragraphs, HTML_TEMPLATE
from komodo.shared.utils.s3_file_utils import BaseExporter, NoopExporter


def ask(prompt, user_id="", agent_id="") -> AssistantResponse:
    user = get_default_user()
    assistant = get_default_assistant()
    request = AssistantRequest(user=user, assistant=assistant, prompt=prompt)
    response = get_assistant_response(request)
    return response


def get_assistant_response(request: AssistantRequest) -> AssistantResponse:
    print(request)
    start_time = datetime.now()
    if 'provider' in request.assistant:
        if request.assistant['provider'] == "openai":
            if is_openai_assistant(request):
                response = openai_assistant_response(request)
            else:
                response = openai_chat_response(request)

        elif request.assistant['provider'] == "azure":
            response = azure_assistant_response(request)
        elif request.assistant['provider'] == "bedrock":
            response = bedrock_assistant_response(request)
        else:
            raise Exception("Unknown provider: " + request.assistant['provider'])
    else:
        raise Exception("No provider specified for assistant: " + request.assistant['name'])

    response.started = start_time.timestamp()
    response.completed = datetime.now().timestamp()
    return response


def is_openai_assistant(request):
    return request.assistant['model'].startswith("asst_") or (
            'assistant_id' in request.assistant and request.assistant['assistant_id'] is not None and
            request.assistant['assistant_id'].startswith("asst_"))


def process_response(response: AssistantResponse, exporter: BaseExporter = NoopExporter()):
    exporter.write(name="raw.txt", body=response.text, content_type="text/plain")

    output = json.dumps(response.output, default=vars)
    exporter.write(name="output.txt", body=output, content_type="text/plain")

    data = response.text
    if response.has_quotes:
        data = data.replace("```html", "").replace("```markdown", "").replace("```json", "").replace("```", "")
        exporter.write(name="processed_quotes.txt", body=data, content_type="text/plain")

    if response.is_json:
        data = json.loads(data)
        data = json.dumps(data, indent=0).replace('\n', '<br>')
        exporter.write(name="processed_json.txt", body=data, content_type="text/html")
    else:
        if has_markdown:
            data = markdown2.markdown(data)
            exporter.write(name="processed_markdown.txt", body=data, content_type="text/html")

        data = text_to_html_paragraphs(data)
        exporter.write(name="processed_newlines.txt", body=data, content_type="text/html")

    data = HTML_TEMPLATE.replace('HTML_CONTENT', data)
    exporter.write(name="processed_template.txt", body=data, content_type="text/html")

    soup = BeautifulSoup(data, "html.parser")
    pretty = soup.prettify()
    exporter.write(name="processed_prettify.txt", body=pretty, content_type="text/html")
    return data


def has_markdown(text):
    return re.search("```markdown", text)
