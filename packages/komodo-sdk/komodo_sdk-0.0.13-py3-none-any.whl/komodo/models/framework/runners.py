from komodo.framework.komodo_agent import KomodoAgent
from komodo.framework.komodo_tool import KomodoTool
from komodo.framework.komodo_user import KomodoUser
from komodo.models.framework.assistant import AssistantRequest, AssistantResponse
from komodo.models.framework.responder import get_assistant_response


def run_appliance(appliance, prompt):
    agent = coordinator_agent(appliance)
    return run_agent(agent, prompt)


def run_agent(agent, prompt) -> AssistantResponse:
    user = KomodoUser.default_user().to_dict()
    assistant = agent.to_dict()
    assistant['tools'] = agent.tools
    # assistant = agent
    # assistant.tools= agent.tools
    request = AssistantRequest(user=user, assistant=assistant, prompt=prompt)
    response = get_assistant_response(request)
    return response


def run_agent_as_tool(agent, args) -> str:
    response = run_agent(agent, args['system'] + "\n\n" + args['user'])
    return response.text


def agent_function_definition(agent):
    return {
        "type": "function",
        "function": {
            "name": agent.shortcode,
            "description": agent.purpose,
            "parameters": {
                "type": "object",
                "properties": {
                    "system": {
                        "type": "string",
                        "description": "Specify context and what exactly you need the agent to do in English."
                    },
                    "user": {
                        "type": "string",
                        "description": "The input to be processed by the agent."
                    },
                },
                "required": ["system", "user"]
            }
        }
    }


def get_agent_as_tool(agent):
    action = lambda args: run_agent_as_tool(agent, args)
    return KomodoTool(shortcode=agent.shortcode,
                      definition=agent_function_definition(agent),
                      action=action)


def coordinator_agent(appliance):
    return KomodoAgent(shortcode=appliance.shortcode + "_coordinator",
                       name='Coordinator Agent',
                       purpose='Coordinate other agents',
                       instructions='Coordinate the other agents to achieve the goal. Create system and user prompts for each agent based on task requirements and inputs.',
                       tools=[get_agent_as_tool(agent) for agent in appliance.agents])
