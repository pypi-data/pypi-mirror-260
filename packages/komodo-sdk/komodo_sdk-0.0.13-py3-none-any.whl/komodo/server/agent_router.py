from typing import AsyncGenerator

from fastapi import Depends, APIRouter, HTTPException, Request
from starlette.responses import StreamingResponse

from komodo.models.framework.runners import run_agent
from komodo.server.globals import get_appliance, get_email_from_header
from komodo.store.conversations_store import ConversationStore

router = APIRouter(
    prefix='/api/v1/agent',
    tags=['Agent']
)


@router.api_route('/ask', methods=['POST'])
async def ask_agent(request: Request, email=Depends(get_email_from_header), appliance=Depends(get_appliance)):
    # Parse the request body as JSON
    body = await request.json()
    # Extract the message and agent_info fields from the JSON body
    message = body.get("message")
    agent_shortcode = body.get("agent_shortcode")
    if not message or not agent_shortcode:
        raise HTTPException(status_code=400, detail="Missing 'message or agent_shortcode' in request body")

    # Get Agent Info based on short code
    agent_info = next((agent for agent in appliance.agents if agent.shortcode == agent_shortcode), None)
    if agent_info is None:
        raise HTTPException(status_code=400, detail="Respective Agent is not available")

    store = ConversationStore()
    if not body.get("guid"):
        title = message
        conversation = store.create_conversation(email, agent_shortcode, title)
    else:
        conversation = store.get_conversation_header(body.get("guid"))

    store.add_message(conversation, email, message)

    # Here you would run your agent with the provided message and agent information
    reply = run_agent(agent_info, message)

    store.add_message(conversation, agent_shortcode, reply.text)

    return {"reply": reply.text, "message": message}


@router.get("/ask-streamed")
async def ask_agent_streamed(email: str, agent_shortcode: str, prompt: str, guid: str = None,
                             appliance=Depends(get_appliance)):
    print("email: ", email, "agent_shortcode: ", agent_shortcode, "prompt: ", prompt)

    # Get Agent Info based on short code
    agent_info = next((agent for agent in appliance.agents if agent.shortcode == agent_shortcode), None)
    if agent_info is None:
        raise HTTPException(status_code=400, detail="Respective Agent is not available")

    store = ConversationStore()
    if guid is None or guid == "":
        title = prompt
        conversation = store.create_conversation(email, agent_shortcode, title)
    else:
        conversation = store.get_conversation_header(guid)
    store.add_message(conversation, email, prompt)

    # Here you would run your agent with the provided message and agent information
    reply = run_agent(agent_info, prompt)
    store.add_message(conversation, agent_shortcode, reply.text)

    return StreamingResponse(komodo_async_generator(reply.text), media_type='text/event-stream')


async def komodo_async_generator(reply: str) -> AsyncGenerator[str, None]:
    for part in reply.split(" "):  # komodo.stream_response(prompt=prompt):
        try:
            yield f"data: {part}\n\n"
        except Exception as e:
            print(e)
            return  # this will close the connection

    print("stream complete")
    yield "event: stream-complete\ndata: {}\n\n"
