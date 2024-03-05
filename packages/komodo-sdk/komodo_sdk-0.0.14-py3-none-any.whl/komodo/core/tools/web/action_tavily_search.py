import os
import time

from requests import HTTPError
from tavily import TavilyClient

from komodo.core.tools.tool_registry import KomodoToolRegistry
from komodo.shared.utils.sentry_utils import sentry_trace

TAVILY_SEARCH_ACTION_NAME = "komodo_tavily_search"


def tavily_search_description():
    return {
        "type": "function",
        "function": {
            "name": TAVILY_SEARCH_ACTION_NAME,
            "description": "Accesses real-time data and insights from a wide range of internet sources, tailored to specific queries. Ideal for gathering current information on various topics.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Specify the search query to retrieve up-to-date and relevant information. Suitable for a broad spectrum of topics, ensuring accurate and professionally curated content."
                    },
                },
                "required": ["query"]
            }
        }
    }


# Function to perform a Tavily search
@sentry_trace
def tavily_search_action(args):
    attempts = 0
    while attempts < 3:
        try:
            tavily_client = TavilyClient(get_tavily_api_key())
            search_result = tavily_client.get_search_context(args["query"], search_depth="advanced", max_tokens=8000)
            return search_result
        except HTTPError as e:
            if e.response.status_code == 429 or e.response.status_code == 502:
                print("Attempt# " + str(attempts) + " Error: " + str(e))
                print("Rate limit exceeded. Waiting for 5 seconds...")
                time.sleep(5)
                attempts += 1


def get_tavily_api_key():
    return os.getenv("TAVILY_API_KEY", "")


def setup_tavily_search_action():
    KomodoToolRegistry.add_tool(TAVILY_SEARCH_ACTION_NAME, tavily_search_description(), tavily_search_action)
