from komodo.core.tools.web.action_scrape import setup_scraper_action
from komodo.core.tools.web.action_serpapi_search import setup_serpapi_search_action
from komodo.core.tools.web.action_tavily_search import setup_tavily_search_action


def setup_all_tools():
    setup_scraper_action()
    setup_serpapi_search_action()
    setup_tavily_search_action()
