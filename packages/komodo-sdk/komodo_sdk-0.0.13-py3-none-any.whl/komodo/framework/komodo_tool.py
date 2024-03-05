class KomodoTool:
    '''
    Base class for all Komodo tools. We use Langchain tools api to create Komodo tools.
    https://python.langchain.com/docs/modules/agents/tools/custom_tools
        '''

    def __init__(self, shortcode, definition, action, name=None, purpose=None):
        self.shortcode = shortcode
        self.definition = definition
        self.action = action
        self.name = name or definition['function']['name']
        self.purpose = purpose or definition['function']['description']

    def __str__(self):
        return f"KomodoTool: {self.shortcode} {self.name} ({self.purpose})"

    def to_dict(self):
        return {
            'shortcode': self.shortcode,
            'name': self.name,
            'purpose': self.purpose,
            'definition': self.definition
        }

    def run(self, args: dict):
        return self.action(args)
