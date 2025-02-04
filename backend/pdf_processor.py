import io
import pdfplumber
import nltk
import os

# Specify the nltk_data directory within the project as backend/nltk_data
nltk_data_path = os.path.join(os.getcwd(), "backend", "nltk_data")

# Ensure nltk loads data from the correct directory
nltk.data.path.insert(0, nltk_data_path)  # Ensure it loads from here first

# Download punkt to the project directory
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
            # Use NLTK to split text into sentences
            sentences = nltk.tokenize.sent_tokenize(text)
            for sentence in sentences:
                clean_sentence = sentence.strip()  # Remove leading and trailing spaces
                if clean_sentence:  # Avoid adding empty lines
                    result.append({"page": page_num, "sentence": clean_sentence})

    return result


def extract_full_text(pdf_binary):
    """
    Parse PDF binary data and extract the full text.
    """
    full_text = []

    # Read PDF binary data
    pdf_stream = io.BytesIO(pdf_binary)

    # Use pdfplumber to parse PDF
    with pdfplumber.open(pdf_stream) as pdf:
        for page in pdf.pages:
            # Extract text from the current page
            text = page.extract_text()
            if text:
                full_text.append(text)

    return "\n".join(full_text)


def simulate_frontend_upload(pdf_path):
    """Simulate frontend upload of PDF binary data"""
    with open(pdf_path, "rb") as f:
        return f.read()


if __name__ == '__main__':
    # Replace with your PDF file path
    pdf_path = "example.pdf"
    pdf_binary = simulate_frontend_upload(pdf_path)

    # Parse PDF
    sentence_page_mapping = extract_text_by_page(pdf_binary)

    # Print results
    for mapping in sentence_page_mapping:
        print(f"Page {mapping['page']}: {mapping['sentence']}")

    print(sentence_page_mapping)
