from flask import Flask, request, jsonify
from llama_cpp import Llama
from flask_cors import CORS
from pdf_processor import extract_text_from_pdf
from model_utils import ModelManager
from pymilvus import MilvusClient
from vectorDB import VectorDB
import logging

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
    # 初始化Milvus客户端
    client = MilvusClient("milvus_demo.db")
    # 初始化LLM模型
    llm_model = Llama(
        # model_path="mistral-7b-instruct-v0.2.Q2_K.gguf",
        model_path= "mistral-7b-instruct-v0.2.Q8_0.gguf",
        n_ctx=32768,  # The max sequence length to use - note that longer sequence lengths require much more resources
        n_threads=8,            # The number of CPU threads to use, tailor to your system and the resulting performance
        n_gpu_layers=35,         # The number of layers to offload to GPU, if you have GPU acceleration available
        temperature=0.1,  # 设置温度以控制输出的随机性
        top_p=0.1,  # 设置top-p采样
        frequency_penalty=0.0,  # 设置频率惩罚
        presence_penalty=0.0  # 设置出现惩罚
    )
    # 句向量模型
    sentence_model = ModelManager.get_model()
    vector_db = VectorDB(client, sentence_model)


@app.route('/')
def hello_world():
    response = llm_model("say 200 words")
    return jsonify({"answer": response['choices'][0]['text']})


@app.route('/chat', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get("question", "")
 
    response = llm_model(question,
                         max_tokens=512,  # Generate up to 512 tokens
                            # stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
                            echo=True )       # Whether to echo the prompt)
    assistant_message = response['choices'][0]['text']
    return jsonify({
        "answer": assistant_message,
        # "history": chat_histories[session_id]  # 可选：返回更新后的历史记录
    })


@app.route('/vector-search', methods=['POST'])
def query_VectorDB():
    try:
        data = request.json
        question = data.get("question", "")
        if not question:
            return jsonify({'error': '问题不能为空'}), 400

        logger.info(f"Received question: {question}")  # 添加日志
        res = vector_db.query_data("demo_collection", question)
        print(f"Query result: {res}")  # 添加日志
        if not res:
            llm_q = ""
        else:
            llm_q = res[0][0]["entity"]["text"]
        # assistant_message = llm_q
        response = llm_model(llm_q,max_tokens=512,  # Generate up to 512 tokens
                            # stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
                            echo=True )
        assistant_message = response['choices'][0]['text']

        return jsonify({
            # "answer": res,
            "answer": assistant_message,
        })
    except Exception as e:
        print(f"Error in vector search: {str(e)}")  # 添加错误日志
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    # print(request.files)
    if 'pdf' not in request.files:
        return jsonify({'error': '没有文件'}), 400
        
    file = request.files['pdf']

    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    try:
        # 读取PDF文件内容
        text_content = file.read()
        decoded_text = extract_text_from_pdf(text_content)
        logger.info(decoded_text)
        vector_db.insert_data("demo_collection", decoded_text)
        
        return jsonify({
            "text": "PDF uploaded successfully",  # 临时响应
            "status": "success"
        })
        
    except UnicodeDecodeError:
        return jsonify({'error': '文件编码错误'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_resources()
    app.run(host='127.0.0.1', port=8080, debug=False)
    # app.run(host='0.0.0.0', port=8080)
