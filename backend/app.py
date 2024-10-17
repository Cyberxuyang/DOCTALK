from flask import Flask, request, jsonify
from llama_cpp import Llama

app = Flask(__name__)

model = Llama(model_path="mistral-7b-instruct-v0.2.Q2_K.gguf")

@app.route('/')
def hello_world():
    response = model("Hello world!")
    return jsonify({"answer": response['choices'][0]['text']})

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get("question", "")
    response = model(question)
    return jsonify({"answer": response['choices'][0]['text']})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    # app.run(host='0.0.0.0', port=8080)
