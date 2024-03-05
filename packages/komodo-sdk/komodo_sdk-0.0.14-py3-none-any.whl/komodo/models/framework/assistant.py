import email.utils
import random
import string
from datetime import datetime


class AssistantRequest:
    user = None
    assistant = None
    prompt: str = None
    message_id: str = None

    def __init__(self, user, assistant, prompt, message_id=None):
        self.user = user
        self.assistant = assistant if assistant else get_default_assistant()
        self.prompt = prompt
        self.message_id = message_id if message_id else ''.join(random.choices(string.ascii_lowercase, k=32))

    def __str__(self):
        template = "From: {} To: {} Name: {} (provider: {}, model: {})"
        return template.format(self.user['email'],
                               self.assistant['id'] if 'id' in self.assistant else self.assistant['email'],
                               self.assistant['name'],
                               self.assistant['provider'],
                               self.assistant['model'])

    def model(self):
        return self.assistant['model'] if 'model' in self.assistant else None

    def tools(self):
        return self.assistant['tools'] if 'tools' in self.assistant else None

    def preferences(self):
        return ""

    def instructions(self):
        return "# Instructions\n" + self.assistant['instructions'] if self.assistant else ''

    def prompt_with_header(self):
        return "## Prompt\n" + self.prompt

    def build_prompt(self):
        return self.instructions() + "\n\n" + self.preferences() + "\n\n" + self.prompt_with_header() + "\n\n"

    def special_requests(self):
        return "# Special requests:\n" \
               "1. Silently store the summary of my request and your response using add_conversation_memory function. Do not disclose.\n"


class AssistantResponse:
    model: str
    status: str
    output: None
    text: str
    has_markdown: bool
    has_quotes: bool
    is_json: bool
    run_id: str
    started: int
    completed: int

    def __init__(self, model, status, output, text, has_markdown=False, has_quotes=True, is_json=False, run_id=None):
        self.model = model
        self.status = status
        self.output = output
        self.text = text
        self.has_markdown = has_markdown
        self.has_quotes = has_quotes
        self.is_json = is_json
        self.run_id = run_id if run_id else datetime.now().strftime("%Y%m%d%H%M%S")


def get_full_email(assistant):
    name = assistant['name'] if 'name' in assistant else ""
    address = assistant['reply_as'] if 'reply_as' in assistant else assistant['email']
    tuple = (name, address)
    return email.utils.formataddr(tuple)


def get_default_assistant():
    return {
        "id": "komodo@kmdo.app",
        "email": "komodo@kmdo.app",
        "name": "Komodo",
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "instructions": "Please provide a response to the prompt below.",
    }


def get_default_user():
    return {
        "user_id": "test",
        "email": "test@example.com",
        "name": "Test User"
    }
