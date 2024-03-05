import os


def fetch_openai_api_key():
    return os.getenv("OPENAI_API_KEY", "")
