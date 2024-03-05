from komodo.models.bedrock.bedrock_claude import bedrock_claude_invoke
from komodo.models.bedrock.bedrock_cohere import bedrock_cohere_invoke
from komodo.models.bedrock.bedrock_titan import bedrock_titan_invoke
from komodo.models.framework.assistant import AssistantRequest, AssistantResponse
from komodo.shared.utils.sentry_utils import sentry_trace


@sentry_trace
def bedrock_assistant_response(request: AssistantRequest) -> AssistantResponse:
    prompt = request.build_prompt()
    return call_model(prompt, request.assistant['model'])


def call_model(prompt, model) -> AssistantResponse:
    try:
        print("Invoking model: " + model)
        if "titan" in model:
            return bedrock_titan_invoke(prompt, model)
        elif "claude" in model:
            return bedrock_claude_invoke(prompt, model)
        elif "cohere" in model:
            return bedrock_cohere_invoke(prompt, model)
        else:
            print("Error invoking model: " + model + " Defaulting to cohere.")
            return bedrock_cohere_invoke(prompt)

    except Exception as e:
        print("Error during invoke: " + str(e))
        output = "Sorry, I am having trouble processing your request. Please try again."
        return AssistantResponse(model=model, status="failed", output=output, text=output)
