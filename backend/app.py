from flask import Flask, request, jsonify
from llama_cpp import Llama
from flask_cors import CORS

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 设置为16MB或更大
CORS(app)

model = Llama(model_path="mistral-7b-instruct-v0.2.Q2_K.gguf")

@app.route('/')
def hello_world():
    response = model("Hello world!")
    return jsonify({"answer": response['choices'][0]['text']})

@app.route('/chat', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get("question", "")
    context = data.get("context", "")  # 获取PDF文本
    # 将问题和上下文一起传递给模型
    response = model(f"Context: {context}\nQuestion: {question}")
    return jsonify({"answer": response['choices'][0]['text']})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    # app.run(host='0.0.0.0', port=8080)
