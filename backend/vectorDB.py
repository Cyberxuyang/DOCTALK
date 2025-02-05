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
            dimension=384,  # The vectors we will use have 384 dimensions
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


    def insert_data(self, collection_name: str, text: str):
        logger.info(f"Inserting data into collection: {collection_name}")
        logger.info("Processing text for insertion")
        self._create_collection(collection_name=collection_name, dimension=384)
        data = self._process_text_to_vectors(text)
        res = self.client.insert(collection_name=collection_name, data=data)
        logger.info(f"Insertion result: {res}")

    def query_data(self, collection_name, q):
        logger.info(f"Processing query: {q}")
        query_vectors = self._process_text_to_vectors(q, forQuery=True)
        logger.info(f"Query vector shape: {len(query_vectors)}")
        
        if not query_vectors:
            return "No text to search"
            
        if not self.client.has_collection(collection_name):
            return "Collection does not exist"
            
        res = self.client.search(
            collection_name=collection_name,
            data=query_vectors,
            limit=2,
            output_fields=["sentence", "page"],
            params={"metric_type": "COSINE"},
        )
        return res

    def query_data_with_context(self, collection_name, q, context_size=2):
        """
        Query text and return context
        context_size: window size for context (per side), total window is 2*context_size + 1
        """
        try:
            logger.info(f"Processing context query: {q}")
            
            # First find the most relevant sentence
            query_vectors = self._process_text_to_vectors(q, forQuery=True)
            if not query_vectors:
                return "No text to search"
            
            if not self.client.has_collection(collection_name):
                return "Collection does not exist"
            
            # Get the most relevant sentence
            initial_res = self.client.search(
                collection_name=collection_name,
                data=query_vectors,
                limit=1,
                output_fields=["sentence", "page", "id"],
                params={"metric_type": "COSINE"},
            )
            
            if not initial_res or not initial_res[0]:
                return []
            
            # Get center sentence ID
            center_id = initial_res[0][0]["entity"]["id"]
            
            # Build context range IDs
            context_ids = list(range(
                max(0, center_id - context_size),
                min(center_id + context_size + 1, self.get_collection_size(collection_name))
            ))
            
            # Query context sentences
            context_results = self.client.query(
                collection_name=collection_name,
                expr=f"id in {context_ids}",
                output_fields=["sentence", "page", "id"]
            )
            
            # Sort by ID to ensure correct order
            if context_results:
                context_results.sort(key=lambda x: x["id"])
            
            return context_results

        except Exception as e:
            logger.error(f"Error in context query: {str(e)}")
            return []

    def get_collection_size(self, collection_name):
        """Get the number of documents in collection"""
        try:
            return self.client.get_collection_stats(collection_name)["row_count"]
        except:
            return 0


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


