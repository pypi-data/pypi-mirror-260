import json

from komodo.framework.komodo_agent import KomodoAgent, data_agent
from komodo.framework.komodo_datasource import KomodoDataSource
from komodo.framework.komodo_tool import KomodoTool
from komodo.framework.komodo_vectorstore import KomodoVectorStore


class KomodoApp:
    def __init__(self, shortcode, name, purpose, agents=None, tools=None, sources=None):
        self.shortcode = shortcode
        self.name = name
        self.purpose = purpose
        self.agents: [KomodoAgent] = agents or []
        self.tools: [KomodoTool] = tools or []
        self.data_sources: [KomodoDataSource] = sources or []
        self.vector_stores: [KomodoVectorStore] = []
        self.tools.append(self.search_data_tool())
        self.agents.append(data_agent(self.search_data_tool()))

    def add_agent(self, agent):
        self.agents += [agent]

    def get_agent(self, id):
        for a in self.agents:
            if a.id == id:
                return a
        return None

    def get_capabilities_of_agents(self):
        n = 0
        t = []
        for a in self.agents:
            if a.purpose is not None:
                n += 1
                t.append("{}. {}: {}".format(n, a.shortcode, a.purpose))
        return '\n'.join(t)

    def add_tool(self, tool):
        self.tools += [tool]

    def get_tool(self, id):
        for a in self.tools:
            if a.id == id:
                return a
        return None

    def get_capabilities_of_tools(self):
        n = 0
        t = []
        for a in self.tools:
            if a.purpose is not None:
                n += 1
                t.append("{}. {}: {}".format(n, a.shortcode, a.purpose))
        return '\n'.join(t)

    def add_data_source(self, ds1):
        self.data_sources += [ds1]

    def get_data_source(self, source):
        for a in self.data_sources:
            if a.id == source or a.name == source:
                return a
        return None

    def list_data(self, sources=None, metadata=False):
        if isinstance(sources, str):
            sources = sources.split(',')
        sources = sources or self.data_sources

        dataset = []
        for source in sources:
            if isinstance(source, str):
                source = self.get_data_source(source)

            for item in source.list_items():
                data = {'source': source.id, 'type': source.type, 'item': item}
                if metadata:
                    for doc in source.get_item(item):
                        data['metadata'] = doc.metadata
                        print(data)
                        dataset.append(data)
                else:
                    print(data)
                    dataset.append(data)

        return dataset

    def search_data_definition(self):
        return {
            "type": "function",
            "function": {
                "name": "appliance_data_search",
                "description": "Retrieve data from available data sources",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "String to semantic search for in the data sources"
                        }
                    },
                    "required": ["query"]
                }
            }
        }

    def get_data_as_tool_action(self, args):
        text = args['query']
        result = []
        for pc in self.vector_stores:
            result += pc.search(text, top_k=3)

        if len(result) > 0:
            return json.dumps(result)

        return "Found: {}. The answer is 42.".format(args['query'])

    def search_data_tool(self):
        return KomodoTool(shortcode="data_search",
                          name="Appliance Data Search Tool",
                          definition=self.search_data_definition(),
                          action=self.get_data_as_tool_action)

    def add_vector_store(self, store):
        self.vector_stores += [store]

    def get_vector_store(self, source):
        for a in self.vector_stores:
            if a.id == source or a.name == source:
                return a
        return None

    def capabilities(self):
        n = 0
        t = []
        for a in self.agents:
            if a.purpose is not None:
                n += 1
                t.append("{}. {}: {}".format(n, a.shortcode, a.purpose))

        return "I am " + self.name + \
            " appliance and my purpose is " + self.purpose + \
            ". I have agents with these capabilities: \n" + self.get_capabilities_of_agents() + \
            "\n\nI have tools with these capabilities: \n" + self.get_capabilities_of_tools()
