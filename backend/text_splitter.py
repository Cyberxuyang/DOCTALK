from typing import List
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextSplitter:
    def split_text(self, text: str, chunk_size: int = 3) -> List[str]:
        """
        将长文本按句子分割，并组合成指定大小的块
        
        Args:
            text: 输入的长文本
            chunk_size: 每个块包含几个句子
            
        Returns:
            List[str]: 分割后的文本块列表
        """
        try:
            # 如果文本不包含标点符号，直接返回原文本
            if not any(p in text for p in '。！？.!?'):
                return [text]
            
            # 按标点符号分割句子（中英文标点）
            sentences = re.split(r'([。！？.!?])', text)
            
            # 重新组合句子和标点
            sentences = [''.join(i) for i in zip(sentences[0::2], sentences[1::2])]
            
            # 过滤空句子
            sentences = [s.strip() for s in sentences if s.strip()]
            
            # 如果分割后为空，返回原文本
            if not sentences:
                return [text]
            
            # 组合成块
            chunks = []
            current_chunk = []
            
            for sentence in sentences:
                current_chunk.append(sentence)
                if len(current_chunk) >= chunk_size:
                    chunks.append(''.join(current_chunk))
                    current_chunk = []
            
            # 处理剩余的句子
            if current_chunk:
                chunks.append(''.join(current_chunk))
            
            logger.info(f"文本已分割成 {len(chunks)} 个片段")
            return chunks if chunks else [text]  # 如果chunks为空，返回原文本
            
        except Exception as e:
            logger.error(f"文本分割失败: {str(e)}")
            # 发生错误时返回原文本
            return [text]

# 测试代码
if __name__ == "__main__":
    # 测试文本
    test_text = """
    人工智能是计算机科学的一个分支，它企图了解智能的实质。并生产出一种新的能sdfgasgf以人类智能相似的方式做出反应的智能机器。
    人工智能的研究包括机器人、语言识别fasdfasd、图像识别、自然语言处理和专家系统等。
    人工智能从诞生以来，理论和技术日益成熟，应sadfa用领域也不断扩大。可以设想，未来人工智能bada[sdkfko;'faw带来的科技产品，将会是人类智慧的"容器"。
    人工智能可以对人的意识、思维的信息过程的模拟。人工智能不是人的智能，但能像人那样思考、也可能超过人的智能。
    """
    
    splitter = TextSplitter()
    chunks = splitter.split_text(test_text, chunk_size=2)
    
    print("\n分割结果:")
    for i, chunk in enumerate(chunks, 1):
        print(f"\nChunk {i}:\n{chunk}")