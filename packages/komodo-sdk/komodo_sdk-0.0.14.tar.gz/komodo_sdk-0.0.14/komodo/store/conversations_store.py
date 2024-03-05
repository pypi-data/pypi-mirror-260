from komodo.proto.model_pb2 import Conversation, Message
from komodo.store.redis_database import RedisDatabase, get_redis_server
from google.protobuf import json_format
from google.protobuf.json_format import Parse
import json
import uuid
from datetime import datetime

class ConversationStore:
    def __init__(self, database=RedisDatabase.CONVERSATIONS):
        self.redis = get_redis_server(database)

    def add_conversation_guid(self, user_email, agent_id, guid):
        key = f"user:{user_email}:agent:{agent_id}"
        self.redis.sadd(key, guid)

    def add_header(self, guid, title, created_at, user_email, agent_id):
        conversation = Conversation(guid=guid,title=title,created_at=created_at,user_email=user_email,agent_shortcode=agent_id)
        header_data = conversation.SerializeToString()
        header_key = f"guid:{guid}:conversation"
        self.redis.set(header_key,header_data)
        return conversation

    def add_message(self, conversation, sender, text):
        now = datetime.utcnow().isoformat() + 'Z' 
        message = Message(guid=str(uuid.uuid4()), sender=sender, text=text, created_at=now)
        message_data = message.SerializeToString()
        guid = conversation.get('guid') if isinstance(conversation, dict) else getattr(conversation, 'guid')
        messages_key = f"guid:{guid}:messages"
        self.redis.rpush(messages_key, message_data)

    def create_conversation(self,user_email,agent_id,title):
        now = datetime.utcnow().isoformat() + 'Z' 
        conversation_guid=str(uuid.uuid4())
        self.add_conversation_guid(user_email, agent_id, conversation_guid)
        conversation = self.add_header(conversation_guid, title, now, user_email, agent_id)
        return conversation

    def get_conversation_header(self,guid):
        header_key = f"guid:{guid}:conversation"
        conversation = self.redis.get(header_key)
        conv = Conversation()
        conv.ParseFromString(conversation)
        conv_dict = json.loads(json_format.MessageToJson(conv))
        return conv_dict

    # Method to retrieve conversation GUIDs
    def retrieve_conversation_guids(self, user_email, agent_id):
        key = f"user:{user_email}:agent:{agent_id}"
        guids = self.redis.smembers(key)
        # Decode each guid from bytes to string
        decoded_guids = [guid.decode('utf-8') for guid in guids]
        return decoded_guids

    def get_conversation(self,guid):
        conversation_header = self.get_conversation_header(guid)
        conversation_messages = self.get_messages(guid)
        # Modify here to wrap the response in a list to match the array structure
        conversation_data = [{
            "conversation": conversation_header,
            "messages": conversation_messages
        }]
        return conversation_data


    def get_conversations(self,user_email,agent_id):
        conversations_data = []
        conversation_guids = self.retrieve_conversation_guids(user_email,agent_id)
        for guid in conversation_guids:
            conv_data=self.get_conversation_header(guid)
            conversations_data.append(conv_data)
        return conversations_data

    # Method to retrieve messages for a specific conversation
    def get_messages(self, conversation_guid):
        messages_key = f"guid:{conversation_guid}:messages"
        messages_data = self.redis.lrange(messages_key, 0, -1)
        messages = []
        for msg_data in messages_data:
            msg = Message()
            msg.ParseFromString(msg_data)
            # Convert protobuf message to dictionary
            message_dict = json.loads(json_format.MessageToJson(msg))
            messages.append(message_dict)
        return messages

    def delete_conversation(self, guid, user_email, agent_id):
        messages_key = f"guid:{guid}:messages"
        self.redis.delete(messages_key)

        header_key = f"guid:{guid}:conversation"
        self.redis.delete(messages_key)

        # Remove the GUID from the set of conversations for the user-agent pair in the CONVERSATIONS database
        conversation_key = f"user:{user_email}:agent:{agent_id}"
        self.redis.srem(conversation_key, guid)

        return {
            "guid" : guid,
            "success" : True,
            "message" : "Deleted the conversation successfully"
        }



