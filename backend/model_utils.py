from sentence_transformers import SentenceTransformer
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelManager:
    _instance = None
    _model = None
    MODEL_NAME = 'paraphrase-MiniLM-L6-v2'
    MODEL_PATH = Path(__file__).parent / 'local_models' / MODEL_NAME

    @classmethod
    def get_model(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance._model

    def __init__(self):
        if ModelManager._model is None:
            try:
                logger.info(f"Loading model {self.MODEL_NAME}...")
                if self.MODEL_PATH.exists():
                    logger.info("Loading model from local storage...")
                    ModelManager._model = SentenceTransformer(str(self.MODEL_PATH))
                else:
                    logger.info("Downloading model from the internet...")
                    ModelManager._model = SentenceTransformer(self.MODEL_NAME)
                    # Save to local storage
                    self.MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
                    ModelManager._model.save(str(self.MODEL_PATH))
                logger.info("Model loaded successfully!")
            except Exception as e:
                logger.error(f"Failed to load model: {str(e)}")
                raise
