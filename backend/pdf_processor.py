import io
import pdfplumber
import nltk
import os

# 指定 nltk_data 目录为项目内部的 backend/nltk_data
nltk_data_path = os.path.join(os.getcwd(), "backend", "nltk_data")

# 确保 nltk 在正确的目录加载数据
nltk.data.path.insert(0, nltk_data_path)  # 确保优先从这里加载

# 下载 punkt 到项目目录
nltk.download('punkt', download_dir=nltk_data_path)
nltk.download('punkt_tab')


def extract_text_by_page(pdf_binary):
    """
    Parse PDF binary data, extract text by page, and split by sentence, returning a mapping of sentences to their pages.
    """
    result = []

    # Read PDF binary data
    pdf_stream = io.BytesIO(pdf_binary)

    # Use pdfplumber to parse PDF
    with pdfplumber.open(pdf_stream) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            # Extract text from the current page
            text = page.extract_text()
            full_text = text
            # Skip if no text can be extracted
            if not text:
                print(f"Page {page_num} has no extractable text.")  # Debug information
                continue
            lines = text.split("\n")
            # Use NLTK to split by sentence
            for line in lines:
                clean_sentence = line.strip()  # Remove leading and trailing spaces
                if clean_sentence:  # Avoid adding empty lines
                    result.append({"page": page_num, "sentence": clean_sentence})

    return result


def simulate_frontend_upload(pdf_path):
    """模拟前端上传 PDF 二进制数据"""
    with open(pdf_path, "rb") as f:
        return f.read()


if __name__ == '__main__':
    # 替换为你的 PDF 文件路径
    pdf_path = "example.pdf"
    pdf_binary = simulate_frontend_upload(pdf_path)

    # 解析 PDF
    sentence_page_mapping = extract_text_by_page(pdf_binary)

    # 打印结果
    for mapping in sentence_page_mapping:
        print(f"Page {mapping['page']}: {mapping['sentence']}")

    print(sentence_page_mapping)
