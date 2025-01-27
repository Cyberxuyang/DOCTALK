from typing import List
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextSplitter:
    def split_text(self, text: str, chunk_size: int = 3) -> List[str]:

        try:
            # If the text does not contain punctuation, return the original text
            if not any(p in text for p in '。！？.!?'):
                return [text]
            
            # Split sentences by punctuation (Chinese and English punctuation)
            sentences = re.split(r'([。！？.!?])', text)
            
            # Recombine sentences and punctuation
            sentences = [''.join(i) for i in zip(sentences[0::2], sentences[1::2])]
            
            # Filter out empty sentences
            sentences = [s.strip() for s in sentences if s.strip()]
            
            # If the split results in an empty list, return the original text
            if not sentences:
                return [text]
            
            # Combine into chunks
            chunks = []
            current_chunk = []
            
            for sentence in sentences:
                current_chunk.append(sentence)
                if len(current_chunk) >= chunk_size:
                    chunks.append(''.join(current_chunk))
                    current_chunk = []
            
            # Handle remaining sentences
            if current_chunk:
                chunks.append(''.join(current_chunk))
            
            logger.info(f"Text has been split into {len(chunks)} chunks")
            return chunks if chunks else [text]  # If chunks is empty, return the original text
            
        except Exception as e:
            logger.error(f"Text splitting failed: {str(e)}")
            # Return the original text in case of an error
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