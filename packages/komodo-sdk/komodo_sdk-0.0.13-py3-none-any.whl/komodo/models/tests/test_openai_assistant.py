import pytest

from komodo.models.framework.assistant import AssistantRequest
from komodo.models.framework.responder import ask
from komodo.models.openai.openai_assistant import openai_assistant_response


@pytest.skip("Skipping all openai tests", allow_module_level=True)
def test_openai_assistant_with_search_api():
    request = AssistantRequest(prompt="What is the latest on Kineo Capital?")
    response = openai_assistant_response(request)
    print(response.text)


def test_openai_assistant_with_options_data():
    response = ask(agent_id="wolf@kmdo.app", prompt="What are the latest AAPL options prices?")
    print(response.text)


def test_openai_chat_with_search_api():
    response = ask(agent_id="synthia@kmdo.app", prompt="What is the latest on Kineo Capital?")
    print(response.text)


def test_openai_assistant_with_xlsx_api():
    prompt = "Can you analyze this dataset for the fields marked as Keep in the Conexio datasheet in NE-Gamma.xlsx and tell me what kind of insights be developed from this datasheet?"
    response = ask(prompt=prompt)
    print(response.text)


def test_openai_assistant_with_user_preferences():
    prompt = "I'd like to change my name to John Doe. I like Mediterranean food. Can you update my preferences?"
    response = ask(prompt=prompt, agent_id=CONCIERGE_AGENT)
    print(response.text)


def test_openai_assistant_update_user_preferences():
    prompt = "Please address me as Senor Emperor. I like Italian food. Can you update my preferences?"
    response = ask(prompt=prompt, agent_id=CONCIERGE_AGENT)
    print(response.text)


def test_openai_assistant_delete_user_preferences():
    prompt = "Please reset all my preferences."
    response = ask(prompt=prompt, agent_id=CONCIERGE_AGENT)
    print(response.text)


def test_openai_assistant_get_user_preferences():
    prompt = "What kind of food do I like?"
    response = ask(prompt=prompt, agent_id=CONCIERGE_AGENT)
    print(response.text)


def test_openai_assistant_implied_user_preferences():
    prompt = "Please address me as Senor Emperor. I like Italian food."
    response = ask(prompt=prompt, agent_id=CONCIERGE_AGENT)
    print(response.text)


def test_openai_assistant_with_memory():
    prompt = "I'd like to change my name to John Doe. I like Mediterranean food."
    response = ask(prompt=prompt, agent_id=CONCIERGE_AGENT)
    print(response.text)


def test_openai_assistant_get_memory():
    prompt = "Summarize last few requests and responses."
    response = ask(prompt=prompt, agent_id=CONCIERGE_AGENT)
    print(response.text)


def test_openai_assistant_implied_memory():
    prompt = "What is happening in Boston?"
    response = ask(prompt=prompt, agent_id=CONCIERGE_AGENT)
    print(response.text)


def test_openai_assistant_location():
    prompt = "What is the location of Miami?"
    response = ask(prompt=prompt, agent_id=CONCIERGE_AGENT)
    print(response.text)


def test_openai_assistant_time():
    prompt = "What is the current time in Miami and New Delhi?"
    response = ask(prompt=prompt, agent_id=CONCIERGE_AGENT)
    print(response.text)


def test_openai_assistant_weather():
    prompt = "What is the current time and weather in Miami? Output in Fahrenheit."
    response = ask(prompt=prompt, agent_id=CONCIERGE_AGENT)
    print(response.text)


def test_openai_tools_time():
    result = time_action({"place": "Miami"})
    print(result)
