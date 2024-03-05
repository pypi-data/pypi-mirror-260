import os

from serpapi import GoogleSearch

from komodo.core.tools.web.action_serpapi_search import serpapi_search_action


def test_serpapi_google():
    search = GoogleSearch({
        "q": "kineo capital",
        "location": "New York, New York",
        "api_key": os.environ["SERP_API_KEY"]
    })
    result = search.get_dict()
    print(f'result:{result}')
    return result


def test_serpapi_bing():
    search = GoogleSearch({
        "engine": "bing",
        "q": "kineo capital",
        "location": "New York, New York",
        "api_key": os.environ["SERP_API_KEY"]
    })
    result = search.get_dict()
    print(f'result:{result}')
    return result


def test_serpapi_search_action():
    print(serpapi_search_action({"query": "Kineo Capital"}))


def test_serpapi_search_action_bing():
    print(serpapi_search_action({"query": "Kineo Capital", "engine": "bing"}))


def test_serpapi_search_action_params():
    print(serpapi_search_action({"query": "Kineo Capital", "engine": "bing", "params": {"hl": "fr"}}))
