
from langchain_community.embeddings import OpenAIEmbeddings


def get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings()
