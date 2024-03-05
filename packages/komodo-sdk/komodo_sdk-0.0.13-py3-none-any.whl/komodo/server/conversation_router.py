from fastapi import APIRouter, HTTPException, Depends, Request
from komodo.server.globals import get_appliance,get_email_from_header
from komodo.store.conversations_store import ConversationStore
from typing import List
from komodo.store.redis_database import RedisDatabase, get_redis_server

router = APIRouter(
    prefix='/api/v1/conversations',
    tags=['Conversations']
)

@router.post('/')
async def get_conversations(request: Request, email=Depends(get_email_from_header), appliance=Depends(get_appliance)):
    # Parse the request body as JSON
    body = await request.json()
    agent_shortcode = body.get("agent_shortcode")
    if not agent_shortcode:
        raise HTTPException(status_code=400, detail="Missing 'agent_shortcode' in Request")

    conversation_store = ConversationStore()
    conversations = conversation_store.get_conversations(email, agent_shortcode)

    if not conversations:
        raise HTTPException(status_code=404, detail="Conversations not found")
    return conversations


@router.get('/{guid}')
async def get_conversation(guid: str, email=Depends(get_email_from_header), appliance=Depends(get_appliance)):
    conversation_store = ConversationStore()
    conversation_data = conversation_store.get_conversation(guid)
    return conversation_data


@router.delete('/{guid}')
async def delete_conversation(request: Request, guid: str, email=Depends(get_email_from_header), appliance=Depends(get_appliance)):
    # Parse the request body as JSON
    body = await request.json()
    agent_shortcode = body.get("agent_shortcode")
    if not agent_shortcode:
        raise HTTPException(status_code=400, detail="Missing 'agent_shortcode' in Request")

    conversation_store = ConversationStore()
    response = conversation_store.delete_conversation(email,agent_shortcode,guid)
    return response


