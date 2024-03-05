from komodo.core.tools.web.action_tavily_search import tavily_search_description, tavily_search_action


def test_tavily_api():
    query = "\"Kineo Capital\" +information +safe"
    result = tavily_search_action({"query": query})
    print(f'search_result:{result}')
    return result


def test_tavily_description():
    print(tavily_search_description())


def test_tavily_search_action():
    print(tavily_search_action({"query": "Kineo Capital"}))
