import json

import boto3
import pytest

from komodo.models.framework.assistant import AssistantRequest, AssistantResponse
from komodo.models.framework.assistant import get_default_assistant, get_default_user
from komodo.models.framework.responder import get_assistant_response
from komodo.shared.documents.text_html import text_to_html


def test_responder():
    prompt = "Tell me a poem"
    user = get_default_user()
    request = AssistantRequest(user=user, assistant=get_default_assistant(), prompt=prompt)
    response = get_assistant_response(request)
    print(request.prompt)
    print(request.message_id)
    print(response.model)
    print(response.run_id)
    print(response.status)
    print(response.has_markdown)
    print(response.has_quotes)
    print(response.text)
    print(response.output)


def test_response_is_serializable():
    response = AssistantResponse(model='foo', status="good", output="foo", text="")
    dump = json.dumps(response, default=vars)
    serdes = AssistantResponse(**json.loads(dump))
    assert response.text == serdes.text
    assert response.model == serdes.model
    assert response.status == serdes.status


def test_prepare_html(has_markdown=False):
    text = INTRO_EMAIL
    html = text_to_html(text, has_markdown)
    print(html)
    return html


@pytest.mark.skip(reason="for manual use / testing only")
def test_send_email():
    client = boto3.client('ses', region_name='us-east-1')
    response = client.send_email(
        Destination={
            'ToAddresses': ["ryan.oberoi@komodoapp.ai"],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': test_prepare_html(),
                }
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': "Test HTML"
            },
        },
        Source="synthia@kmdo.app"
    )

    print(response)


INTRO_EMAIL = """
Hello Team,

I hope this message finds you well!

I'm excited to introduce myself as the latest addition to the Sand Hill East family. My name is Synthia, and I'm a virtual assistant designed to be your partner in advisory services. Like any new team member, I'm here to make your professional lives easier and more efficient.

As an advanced AI, I specialize in processing complex data, analyzing industry trends, and offering intelligent insights. I have been meticulously trained to understand not only the intricacies of our business but also to recognize the distinct voice of Sand Hill East. My role is to go beyond traditional assistance; I am here to provide you with comprehensive, evidence-based advice and strategic recommendations. I've been trained to familiarize myself with you, your skills, special talents... or "superpowers" as they say.

Think of me as a resource with boundless energy, always available to help guide you and address your data-intensive tasks. This frees up your time to focus on what you do best: building strong, personalized relationships with our clients and making strategic decisions.

You are encouraged to email me with your queries or to test out my capabilities. Consider me as your own advisory associate, equipped with the latest technology to support you in our shared mission to excel in the advisory landscape.

Note: I only have access to GPT4 data, and have not connected any pay-to-play third-party resources, or SHE internal documentation. I bring the world of public data to your email!

Instructions for use: just email me (synthia@sandhilleast.net) with questions. I look forward to working together and empowering our team with the best of AI and human collaboration!

Warm regards,

Synthia

Your Virtual Assistant at Sand Hill East

P.S.: If you're curious about what I can do, don't hesitate to send me a challenge. I'm here to impress!
"""
