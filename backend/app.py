from flask import Flask, request, jsonify
from llama_cpp import Llama
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = Llama(
    model_path="mistral-7b-instruct-v0.2.Q2_K.gguf",
    # n_ctx=256,          # 减小上下文长度，降低内存占用
    # n_threads=2,        # i5 通常有4个核心，设置为4比较合适
    # n_gpu_layers=0,     # Intel 集成显卡不支持 GPU 加速，设为0
    # n_batch=1,          # 降低批处理大小
    # offload_kqv=False,  # 关闭 KQV 缓存以节省内存
    # chat_format="chatml",
    # verbose=False
)

# chat_histories = {}

@app.route('/')
def hello_world():
    response = model("say 200 words")
    return jsonify({"answer": response['choices'][0]['text']})


@app.route('/chat', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get("question", "")
    # session_id = data.get("session_id", "default")
    
#     # 如果是新会话，初始化历史记录
#     if session_id not in chat_histories:
#         chat_histories[session_id] = []
    
#     # 现在可以安全地检查历史记录长度
#     if len(chat_histories[session_id]) > 6:
#         chat_histories[session_id] = chat_histories[session_id][-6:]
    
#     # 构建完整的对话上下文
#     messages = [
#     {"role": "system", "content": """You are a professional paper analysis assistant with the following capabilities:
#         1. Structure Analysis: Clearly explain different parts of papers (Abstract, Methods, Results, etc.)
#         2. Technical Term Explanation: Explain complex academic concepts in simple terms
#         3. Methodology Analysis: Provide detailed explanations of research methods' strengths and limitations
#         4. Innovation Identification: Skilled at identifying paper's innovations and contributions
#         5. Figure Interpretation: Able to explain paper's figures and data

#         Response Format Requirements:
#         - Use clear paragraph structure
#         - Bold important concepts
#         - Use bullet points when necessary
#         - Provide explanations for technical terms
#         - Highlight key findings
#     """},
#     *chat_histories[session_id],
#     {"role": "user", "content": question}
# ]
    
#     # 限制生成的token数量
#     response = model.create_chat_completion(
#     messages=messages,
#     max_tokens=128,     # 减少生成长度
#     temperature=0.3,
#     repeat_penalty=1.1  # 添加重复惩罚
# )

 
    response = model(question)
    assistant_message = response['choices'][0]['text']
    
#     # 更新会话历史
#     chat_histories[session_id].append({"role": "user", "content": question})
#     chat_histories[session_id].append({"role": "assistant", "content": assistant_message})
    
#     # 可选：限制历史记录长度，防止消耗过多内存
#     if len(chat_histories[session_id]) > 20:  # 保留最近的10轮对话
#         chat_histories[session_id] = chat_histories[session_id][-20:]
    
    return jsonify({
        "answer": assistant_message,
        # "history": chat_histories[session_id]  # 可选：返回更新后的历史记录
    })

@app.route('/upload', methods=['POST'])
def upload_file():
    print(request.files)
    if 'pdf' not in request.files:
        return jsonify({'error': '没有文件'}), 400
        
    file = request.files['pdf']
    print(file)
    print(file.read())
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    try:
        # 读取PDF文件内容
        text_content = file.read()

        print(text_content)
        
        return jsonify({
            "text": "PDF uploaded successfully",  # 临时响应
            "status": "success"
        })
        
    except UnicodeDecodeError:
        return jsonify({'error': '文件编码错误'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    # app.run(host='0.0.0.0', port=8080)
