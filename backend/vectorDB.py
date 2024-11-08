from pymilvus import MilvusClient
from app import sentence_model
from text_splitter import TextSplitter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


client = MilvusClient("milvus_demo.db")

class VectorDB:
    def __init__(self, client):
        self.client = client
        self.text_splitter = TextSplitter()

    def _create_collection(self, collection_name: str, dimension: int):
        if client.has_collection(collection_name=collection_name):
            client.drop_collection(collection_name=collection_name)
        client.create_collection(
            collection_name=collection_name,
            dimension=384,  # The vectors we will use in this demo has 768 dimensions
        )

    def _process_text_to_vectors(self, text, is_query: bool = False):
        docs = self.text_splitter.split_text(text, chunk_size=1)
        vectors = [sentence_model.encode(doc).tolist() for doc in docs]
        if is_query:
            return vectors
        data = [
            {"id": i, "vector": vectors[i], "text": docs[i]}
            for i in range(len(vectors))
        ]
        return data

    def insert_data(self, collection_name: str, text: str ):
        data = self._process_text_to_vectors(text)
        res = self.client.insert(collection_name=collection_name, data=data)
        logger.info(res)

    def query_data(self, collection_name, q):
        query_vectors = self._process_text_to_vectors(q, is_query=True)
        res = client.search(
            collection_name=collection_name,
            data=query_vectors,
            limit=2,
            output_fields=["text"],
        )
        return res


if __name__ == "__main__":
    vector_db = VectorDB(client)
    # vector_db.create_collection("demo_collection", 384)
    # res = vector_db.insert_data("demo_collection", "Artificial intelligence was founded as an "
    #                                                "academic discipline in 1956. Alan Turing was the first person to "
    #                                                "conduct substantial research in AI. Born in Maida Vale, London, "
    #                                                "Turing was raised in southern England.")



    res = vector_db.query_data("demo_collection", "Who is Alan Turing?")
    print(res)
