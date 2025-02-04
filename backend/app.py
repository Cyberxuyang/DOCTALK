from flask import Flask, request, jsonify
from llama_cpp import Llama
from flask_cors import CORS
from model_utils import ModelManager
from pymilvus import MilvusClient
from vectorDB import VectorDB
import logging
from utils import clean_answer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Content-Length", "Accept", "X-Requested-With"],
        "expose_headers": ["Content-Length"],
        "supports_credentials": False,
        "max_age": 3600
    }
})


def init_resources():
    global client, llm_model, sentence_model, vector_db
    # Initialize Milvus client
    client = MilvusClient("milvus_demo.db")

    # # Mistral-7b-instruct-v0.2.Q8_0.gguf
    # llm_model = Llama(
    #     model_path= "mistral-7b-instruct-v0.2.Q8_0.gguf",
    #     n_ctx=2048,  # The max sequence length to use - note that longer sequence lengths require much more resources
    #     n_threads=4,            # The number of CPU threads to use, tailor to your system and the resulting performance
    #     n_gpu_layers=5,         # The number of layers to offload to GPU, if you have GPU acceleration available
    #     temperature=0.3,  # Set temperature to control randomness of output
    #     top_p=0.1,  # Set top-p sampling
    #     # repeat_penalty=1.2,
    #     frequency_penalty=0.0,  # Set frequency penalty
    #     presence_penalty=0.0,  # Set presence penalty
    #     # stop = ["</s>"],  # Stop immediately when "</s>" is encountered
    #     max_tokens=256,  # Generate up to 256 tokens
    # )


    # DeepSeek-Coder-V2-Lite-Instruct-Q5_K_M.gguf
    llm_model = Llama(
        # model_path="DeepSeek-Coder-V2-Lite-Instruct-Q5_K_M.gguf",
        model_path="DeepSeek-R1-Distill-Llama-8B-Q5_K_M.gguf",
        n_ctx=8192,
        n_threads=8,
        n_gpu_layers=10,
        temperature=0.3,
        top_p=0.9,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        repeat_penalty=1.2,
        stop=["</s>"],
        echo=False,  # Do not echo input
        encoding="utf-8"  # Specify encoding explicitly
    )
    # Sentence vector model
    sentence_model = ModelManager.get_model()
    vector_db = VectorDB(client, sentence_model)


@app.route('/', methods=['GET'])
def hello_world():
    response = llm_model("say 2 words")
    return jsonify({"answer": response['choices'][0]['text']})


@app.route('/chat', methods=['POST'])
def ask_question():
    try:
        data = request.json
        question = data.get("question", "")

        # 优化提示词
        prompt = (
            f"Please provide a **direct and factual answer** to the following question, **without any additional commentary or self-reflection**.\n"
            f"Question: {question}\n"
        )

        logger.info(f"start calling LLM")
        response = llm_model(prompt=prompt, max_tokens=100)  # 限制生成的最大字数
        logger.info(f"LLM response: {response}")

        # 提取生成的文本
        assistant_message = response['choices'][0]['text'].strip()

        assistant_message = clean_answer(assistant_message)

        return jsonify({
            "answer": assistant_message,
            # "history": chat_histories[session_id]  # 可选：返回更新后的历史记录
        })
    except Exception as e:
        logger.error(f"Error in model inference: {e}")
        return jsonify({'error': 'Model inference failed'}), 500

@app.route('/vector-search', methods=['POST'])
def query_VectorDB():
    try:
        data = request.json
        question = data.get("question", "")
        if not question:
            return jsonify({'error': 'Question cannot be empty'}), 400

        logger.info(f"Received question: {question}")  # Add log

        res = vector_db.query_data("demo_collection", question)
        logger.info(f"vector_db result: {res}")
        if not res:
            vec_res = ""
            page = ""
        else:
            vec_res = res[0][0]["entity"]["sentence"].strip()
            page = res[0][0]["entity"]["page"]

        # prompt = f"Text: '{vec_res}'\nQuestion: '{question}'\nAnswer (only the fact, no extra information)"
        prompt = (
            f"Based on '{vec_res}', Please provide a **direct and factual answer** to the following question, **without any additional commentary or self-reflection**.\n"
            f"Question: {question}\n"
        )

        logger.info(prompt)

        response = llm_model(prompt=prompt, max_tokens=256)
        assistant_message = response['choices'][0]['text']

        assistant_message = clean_answer(assistant_message)

        return jsonify({
            "answer": assistant_message,
            "vectorDB_answer": vec_res,
            "page": page
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():

    if 'pdf' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
        
    file = request.files['pdf']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Read PDF file content
        text_content = file.read()
        # decoded_text = extract_text_by_page(text_content)
        # logger.info(decoded_text)
        vector_db.insert_data("demo_collection", text_content)
        
        return jsonify({
            "text": "PDF uploaded successfully",
            "status": "success"
        })
        
    except UnicodeDecodeError:
        return jsonify({'error': 'File encoding error'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_resources()
    app.run(host='127.0.0.1', port=8080, debug=False)

