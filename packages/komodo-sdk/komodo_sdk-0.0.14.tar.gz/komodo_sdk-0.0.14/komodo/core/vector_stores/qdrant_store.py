import json
import uuid
from time import sleep

from langchain.text_splitter import NLTKTextSplitter
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import CollectionInfo

from komodo.framework.komodo_vectorstore import KomodoVectorStore
from komodo.shared.embeddings.openai import get_embeddings


class QdrantStore(KomodoVectorStore):

    def __init__(self, name, index=None):
        super().__init__(name, type="qdrant", id=index)
        self.client = QdrantClient(":memory:")
        self.collection_name = self.id
        self.get_collection()

    def get_collection(self) -> CollectionInfo:
        collections = self.client.get_collections()
        print(collections)

        # only create collection if it doesn't exist
        if self.collection_name not in [c.name for c in collections.collections]:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1536,
                    distance=models.Distance.COSINE,
                ),
            )

        collections = self.client.get_collections()
        print(collections)
        return self.client.get_collection(collection_name=self.collection_name)

    def embeddings(self, text):
        return get_embeddings().embed_query(text)

    def upsert(self, id, text, metadata=None):
        embeddings = self.embeddings(text)
        metadata = metadata or {}
        metadata["text"] = text
        self.client.upsert(
            collection_name=self.collection_name,
            points=models.Batch(ids=[id], vectors=[embeddings], payloads=[metadata]),
        )
        collection_vector_count = self.client.get_collection(collection_name=self.collection_name).vectors_count
        print(f"Vector count in collection: {collection_vector_count}")

    def wait_for_upsert(self, id):
        upserted = False
        while not upserted:
            try:
                self.client.retrieve(self.collection_name, [id])
                upserted = True
                print("Upserted: ", id)
            except Exception as e:
                sleep(1)
                print("Waiting for upsert: " + str(e))
                pass

    def upsert_documents(self, documents, chunk_size=1200, chunk_overlap=100, pages=1000):
        text_splitter = NLTKTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        for document in documents:
            text = document.page_content
            texts = text_splitter.split_text(text)
            print("Split text into {} chunks of size: {}".format(len(texts), chunk_size))

            data_to_upsert = []
            for i, t in enumerate(texts[:pages]):
                print("Adding chunk:", i)
                metadata = {}
                metadata["source"] = document.metadata['source'] if document.metadata['source'] else ""
                metadata["title"] = document.metadata['title'] if document.metadata['title'] else ""
                metadata["description"] = document.metadata['description'] if document.metadata['description'] else ""
                metadata["language"] = document.metadata['language'] if document.metadata['language'] else ""
                metadata["chunk"] = i
                metadata["text"] = t

                id = uuid.uuid4()
                embedding = get_embeddings().embed_query(t)
                data_to_upsert.append({"id": id, "values": embedding, "metadata": metadata})

            if len(data_to_upsert) > 0:
                ids = [d['id'] for d in data_to_upsert]
                embeddings = [d['values'] for d in data_to_upsert]
                metadatas = [d['metadata'] for d in data_to_upsert]
                self.client.upsert(collection_name=self.collection_name,
                                   points=models.Batch(ids=ids, vectors=embeddings, payloads=metadatas))

        collection_vector_count = self.client.get_collection(collection_name=self.collection_name).vectors_count
        print(f"Vector count in collection: {collection_vector_count}")

    def upsert_list(self, list, source='', pages=1000):
        data_to_upsert = []
        for i, t in enumerate(list[:pages]):
            print("Adding chunk:", i)
            s = json.dumps(t)

            metadata = {}
            metadata["source"] = source
            metadata["chunk"] = i
            metadata["text"] = s

            id = str(uuid.uuid4())
            embedding = get_embeddings().embed_query(s)
            data_to_upsert.append({"id": id, "values": embedding, "metadata": metadata})
            self.client.upsert(collection_name=self.collection_name,
                               points=models.Batch(ids=[id], vectors=[embedding], payloads=[metadata]))

        collection_vector_count = self.client.get_collection(collection_name=self.collection_name).vectors_count
        print(f"Vector count in collection: {collection_vector_count}")

    def search(self, query, top_k=10) -> list:
        try:
            encoded_query = get_embeddings().embed_query(query)

            result = self.client.search(
                collection_name=self.collection_name,
                query_vector=encoded_query,
                limit=top_k,
            )  # search qdrant collection for context passage with the answer

            context = [
                {'id': x.id, 'score': x.score, 'metadata': x.payload} for x in result
            ]  # extract title and payload from result
            return context

        except Exception as e:
            print({e})
            return []


if __name__ == "__main__":
    store = QdrantStore("test")
    collection = store.get_collection()
    print(store.to_dict(), collection.dict(), collection.vectors_count)

    store.upsert(3, "hello world", {"foo": "bar"})
    store.wait_for_upsert(3)
    print(store.search("hello", 3))
