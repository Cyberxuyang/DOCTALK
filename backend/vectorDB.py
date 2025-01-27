from pymilvus import MilvusClient

from model_utils import ModelManager
from pdf_processor import extract_text_by_page
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorDB:
    def __init__(self, client, sentence_model):
        self.client = client
        # self.text_splitter = TextSplitter()
        self.sentence_model = sentence_model

    def _create_collection(self, collection_name: str, dimension: int):
        if self.client.has_collection(collection_name=collection_name):
            self.client.drop_collection(collection_name=collection_name)
        self.client.create_collection(
            collection_name=collection_name,
            dimension=384,  # The vectors we will use in this demo have 768 dimensions
        )

    def _process_text_to_vectors(self, text, forQuery: bool = False):

        if forQuery:
            return [self.sentence_model.encode(text).tolist()]

        sentence_page_mapping = extract_text_by_page(text)

        for i in range(len(sentence_page_mapping)):
            sentence_page_mapping[i]["id"] = i
            sentence_page_mapping[i]["vector"] = self.sentence_model.encode(sentence_page_mapping[i]["sentence"])
        #
        return sentence_page_mapping


    def insert_data(self, collection_name: str, text: str ):
        logger.info(f"Inserting data into collection: {collection_name}")
        logger.info("[insert_data]: text:", text)
        self._create_collection(collection_name=collection_name, dimension=384)
        data = self._process_text_to_vectors(text)
        res = self.client.insert(collection_name=collection_name, data=data)
        logger.info(res)

    def query_data(self, collection_name, q):
        logger.info(f"[query_data]-q: {q}")
        query_vectors = self._process_text_to_vectors(q, forQuery=True)
        print(type(query_vectors))  # Expected to be <class 'list'>
        print(type(query_vectors[0]))  # Expected to be <class 'list'>
        print(len(query_vectors[0]))
        # logger.info(f"[query_data]-query_vectors: {query_vectors}")
        logger.info(f"[query_data] Query Vector Shape: {len(query_vectors)}")
        if not query_vectors:  # Check if vectors are empty
            return "No text to search"
            
        if not self.client.has_collection(collection_name):  # Check if collection exists
            return "Collection does not exist"
        res = self.client.search(
            collection_name=collection_name,
            data=query_vectors,
            limit=2,
            output_fields=["sentence", "page"],
            params={"metric_type": "COSINE"},
        )
        return res


if __name__ == "__main__":
    sentence_model = ModelManager.get_model()
    client = MilvusClient("milvus_demo.db")
    vector_db = VectorDB(client, sentence_model)
    text = ("Artificial intelligence was founded as an "
            "academic discipline in 1956. Alan Turing was the first person to "
            "conduct substantial research in AI. Born in Maida Vale, London, "
            "Turing was raised in southern England."
            )
    from pdf_processor import simulate_frontend_upload

    pdf_path = "example.pdf"
    pdf_binary = simulate_frontend_upload(pdf_path)
    res = vector_db._process_text_to_vectors(pdf_binary, False)
    # print(res)
    vector_db.insert_data("demo_collection",pdf_binary)
    res = vector_db.query_data("demo_collection", "xuyang")
    print(res)


