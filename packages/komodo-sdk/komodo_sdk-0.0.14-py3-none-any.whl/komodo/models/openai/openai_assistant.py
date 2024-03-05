import json
import time

import sentry_sdk

from komodo.models.framework.assistant import AssistantResponse, AssistantRequest
from komodo.models.framework.models import OPENAI_GPT4_MODEL
from komodo.models.openai.openai_api import get_definitions
from komodo.models.openai.openai_api_key import fetch_openai_api_key
from komodo.models.openai.openai_process_actions import process_actions_gpt40_1106_preview
from komodo.shared.utils.sentry_utils import sentry_trace


def outputs_json(assistant):
    return 'output_format' in assistant and assistant['output_format'] == 'json'


@sentry_trace
def openai_assistant_response(request: AssistantRequest) -> AssistantResponse:
    from openai import OpenAI
    api_key = fetch_openai_api_key()
    client = OpenAI(api_key=api_key)
    thread = client.beta.threads.create()
    start_time = time.perf_counter()

    def elapsed_time():
        return int(100 * (time.perf_counter() - start_time)) / 100

    try:
        with sentry_sdk.start_span(op="create thread and run", description="create thread and run description"):
            prompt = request.prompt[:16000]  # limit to 16000 characters

            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=prompt
            )

            definitions = get_definitions(request.tools())
            definitions.append({"type": "retrieval"})

            names = [tool['function']['name'] for tool in definitions if
                     'function' in tool and 'name' in tool['function']]
            print("Creating run with functions: " + ", ".join(names))

            instructions = request.assistant['instructions']
            instructions += "\n\n" + request.preferences()
            # instructions += "\n\n" + request.special_requests()
            instructions += "\n\n"

            assistant_id = request.assistant['assistant_id']
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant_id,
                model=OPENAI_GPT4_MODEL,  # use the latest model for actions to work well
                instructions=instructions,
                tools=definitions,
                metadata={'user_id': request.user['email'], 'user_name': request.user['name'],
                          'agent_id': request.assistant['shortcode'], 'agent_name': request.assistant['name'], }
            )
            print("Run created: ", run.id, " time elapsed: ", elapsed_time())

        wait_for_secs = 3
        total_wait_in_secs = 0

        # "queued", "in_progress", "requires_action", "cancelling", "cancelled", "failed", "completed", "expired"
        with sentry_sdk.start_span(op="wait for run complete", description="wait for run complete description"):
            while run.status in ["queued", "in_progress", "requires_action", "cancelling"]:
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )

                # keep track of the run status in the database
                print("Run status is: " + run.status + " time slept " +
                      str(total_wait_in_secs) + " seconds" + " time elapsed: " + str(elapsed_time()))

                if run.status == "completed":
                    break

                if run.status == "requires_action":
                    print("Run requires action")
                    outputs = process_actions_gpt40_1106_preview(run, request.tools())
                    run = client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=outputs
                    )
                    wait_for_secs = 3

                # wait for few seconds before polling again
                with sentry_sdk.start_span(op="sleep", description="sleep description"):
                    time.sleep(wait_for_secs)
                    total_wait_in_secs += wait_for_secs
                    if run.status == "in_progress":
                        wait_for_secs = 5

        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            for message in messages:
                print(message.role + ": " + json.dumps(message, default=vars))

            for message in messages:
                for content in message.content:
                    if content.type == "text" and message.role == "assistant":
                        return AssistantResponse(model=request.assistant['model'],
                                                 status=run.status,
                                                 output=run,
                                                 text=content.text.value,
                                                 has_markdown=not outputs_json(request.assistant),
                                                 has_quotes=True,
                                                 is_json=outputs_json(request.assistant))

            print("Failed to get a proper response from completed run")
            user_message = "I apologize, this is unexpected but I am unable to help you at the moment."
            return AssistantResponse(model=request.assistant['model'], status="response error", output=run,
                                     text=user_message)

        else:
            error = run.last_error.message if run.last_error else "unknown"
            user_message = "Sorry, I am not able to help you with that right now. Please try again later."
            print("Open AI assistant run was not successful: " + run.status + " last error: " + error)
            return AssistantResponse(model=request.assistant['model'], status=run.status,
                                     output=run, text=user_message)

    finally:
        print("Deleting thread: " + thread.id)
        client.beta.threads.delete(thread_id=thread.id)
