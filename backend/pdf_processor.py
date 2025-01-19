from PyPDF2 import PdfReader
import io
import pdfplumber
import nltk

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

# 确保 punkt 句子分割模型已下载
nltk.download('punkt')

def extract_text_by_page(pdf_binary):
    """
    解析 PDF 二进制数据，按页提取文本，并按句子拆分，返回句子与所在页的映射
    """
    result = []

    # 读取 PDF 二进制数据
    pdf_stream = io.BytesIO(pdf_binary)

    # 使用 pdfplumber 解析 PDF
    with pdfplumber.open(pdf_stream) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            # 提取当前页的文本
            text = page.extract_text()

            # 如果无法提取文本，则跳过
            if not text:
                print(f"⚠️ Page {page_num} has no extractable text.")  # 调试信息
                continue

            # 使用 NLTK 按句子分割
            sentences = nltk.sent_tokenize(text)

            # 记录句子与页码
            for sentence in sentences:
                result.append({"page": page_num, "sentence": sentence})

    return result


def simulate_frontend_upload(pdf_path):
    """模拟前端上传 PDF 二进制数据"""
    with open(pdf_path, "rb") as f:
        return f.read()


if __name__ == '__main__':
    # # 替换为你的 PDF 文件路径
    # pdf_path = "example.pdf"
    # pdf_binary = simulate_frontend_upload(pdf_path)
    #
    # # 解析 PDF
    # sentence_page_mapping = extract_text_by_page(pdf_binary)
    #
    # # 打印结果
    # for mapping in sentence_page_mapping:
    #     print(f"Page {mapping['page']}: {mapping['sentence']}")

    import nltk

    print(nltk.data.path)

