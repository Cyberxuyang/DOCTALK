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
                logger.info(f"正在加载模型 {self.MODEL_NAME}...")
                if self.MODEL_PATH.exists():
                    logger.info("从本地加载模型...")
                    ModelManager._model = SentenceTransformer(str(self.MODEL_PATH))
                else:
                    logger.info("从网络下载模型...")
                    ModelManager._model = SentenceTransformer(self.MODEL_NAME)
                    # 保存到本地
                    self.MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
                    ModelManager._model.save(str(self.MODEL_PATH))
                logger.info("模型加载完成！")
            except Exception as e:
                logger.error(f"模型加载失败: {str(e)}")
                raise

# sentences = ["This is an example sentence", "Each sentence is converted"]
#
# embeddings = ModelManager.get_model().encode(sentences)
# print(embeddings)