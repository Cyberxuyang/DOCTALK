from PyPDF2 import PdfReader
import io

def extract_text_from_pdf(pdf_binary):
    """
    从PDF二进制数据中提取文本
    """
    try:
        # 创建内存中的PDF文件对象
        pdf_file = io.BytesIO(pdf_binary)
        # 创建PDF阅读器
        pdf_reader = PdfReader(pdf_file)
        
        # 提取所有页面的文本
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
            
        return text
    except Exception as e:
        raise Exception(f"PDF处理错误: {str(e)}") 