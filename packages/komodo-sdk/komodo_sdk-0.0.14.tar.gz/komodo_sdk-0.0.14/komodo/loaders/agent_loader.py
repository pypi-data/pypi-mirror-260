from komodo.framework.komodo_agent import KomodoAgent
from komodo.loaders.tool_loader import ToolLoader
from komodo.store.agent_store import AgentStore


class AgentLoader:
    @classmethod
    def load(cls, shortcode) -> KomodoAgent:
        agent = AgentStore().retrieve_agent(shortcode)
        komodo_agent = KomodoAgent(name=agent.name,
                                   instructions=agent.instructions,
                                   purpose=agent.purpose,
                                   model=agent.model,
                                   provider=agent.provider,
                                   shortcode=agent.shortcode,
                                   email=agent.email,
                                   reply_as=agent.reply_as,
                                   phone=agent.phone,
                                   assistant_id=agent.assistant_id,
                                   output_format=agent.output_format,
                                   footer=agent.footer)

        for shortcode in agent.tool_shortcodes:
            tool = ToolLoader.load(shortcode)
            komodo_agent.add_tool(tool)

        return komodo_agent
