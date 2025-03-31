from flask import Flask, request, jsonify, send_from_directory
import os
from ctransformers import AutoModelForCausalLM

app = Flask(__name__)

# 1. Path to your model file:
MODEL_PATH = r"C:\models\llama-2-7b-chat.Q5_K_M.gguf"

# 2. Load the model at startup using ctransformers
llm = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    model_type="llama",  # 'llama' for Llama-based models
    gpu_layers=0         # 0 => run entirely on CPU; change if you want partial GPU offload
)

@app.route("/")
def serve_index():
    """
    Serve index.html from the same folder as app.py.
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(root_dir, "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """
    Handle POST requests from the chat UI.
    Generate a response using the Llama model.
    """
    data = request.get_json()
    user_message = data.get("message", "")

    # 3. Generate text from the model
    # ctransformers returns the generated text as a raw string.
    # If needed, you can pass more params like max_new_tokens, temperature, etc.
    output = llm(user_message, max_new_tokens=128)

    # 'output' is already the text. We can return it directly.
    return jsonify({"reply": output})

if __name__ == "__main__":
    # Run on localhost:5000
    app.run(host="127.0.0.1", port=5000, debug=True)
