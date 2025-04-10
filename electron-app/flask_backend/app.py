from flask import Flask, request, Response, send_from_directory
import os
import sys
import requests
import subprocess
import time
import json

app = Flask(__name__)

# Ollama settings
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "llama2"
USE_FLASH_ATTENTION = True  # Enable or disable Flash Attention


def get_base_dir():
    """
    When running as a onefile bundle, PyInstaller extracts all files into a temporary
    folder referenced by sys._MEIPASS. Otherwise, return the directory containing this file.
    """
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def start_ollama():
    """Start Ollama in the background if it's not already running."""
    # Build a path to the local ollama.exe (bundled in the same folder as our EXE)
    local_ollama_path = os.path.join(get_base_dir(), "ollama.exe")

    try:
        # Check if Ollama is running by making a test request
        requests.get("http://localhost:11434/api/health", timeout=1)
        print("Ollama is already running.")
        return True
    except requests.exceptions.RequestException:
        print("Starting Ollama...")
        if sys.platform == "win32":
            try:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                process = subprocess.Popen(
                    [local_ollama_path, "serve"],
                    startupinfo=startupinfo,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                )
                # Wait for Ollama to start
                for _ in range(10):
                    time.sleep(1)
                    try:
                        requests.get("http://localhost:11434/api/health", timeout=1)
                        print("Ollama started successfully.")
                        return True
                    except requests.exceptions.RequestException:
                        continue

                print("Ollama failed to start properly.")
                return False

            except Exception as e:
                print(f"Error starting Ollama: {e}")
                return False
        else:
            # For Linux/Mac (if needed)
            subprocess.Popen(
                [local_ollama_path, "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(5)
            return True


@app.route("/")
def serve_index():
    # Serve the single index.html file from our base directory.
    root_dir = get_base_dir()
    print("DEBUG: Serving index from", root_dir, flush=True)
    return send_from_directory(root_dir, "index.html")


@app.route("/chat", methods=["GET"])
def chat_sse():
    # Get user message from query string
    user_message = request.args.get("message", "")

    system_prompt = (
        "You are the BPSA (Business Products Sales Assistant) Chatbot.\n"
        "Your purpose is to help users with business product information "
        "and sales inquiries. Be concise, helpful, and accurate.\n"
    )

    prompt = f"{system_prompt}\nUser: {user_message}\nAssistant:"

    def sse_generate():
        try:
            options = {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 500,
            }
            if USE_FLASH_ATTENTION:
                options["use_flash_attention"] = True

            resp = requests.post(
                OLLAMA_API,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": True,  # Enable streaming
                    "options": options
                },
                stream=True,
                timeout=60
            )
            resp.raise_for_status()

            for line in resp.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        text_piece = chunk.get("response", "")
                        if text_piece:
                            yield f"data: {text_piece}\n\n"
                    except json.JSONDecodeError:
                        pass

        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama API: {e}")
            yield "data: Sorry, I'm having trouble connecting to my brain.\n\n"

    return Response(sse_generate(), mimetype='text/event-stream')


if __name__ == "__main__":
    # Start Ollama before starting Flask
    if start_ollama():
        try:
            print(f"Checking if {MODEL_NAME} is available...")
            model_list = requests.get("http://localhost:11434/api/tags").json()
            available = [m["name"] for m in model_list.get("models", [])]
            if MODEL_NAME not in available:
                print(f"Pulling {MODEL_NAME}... (first time may be slow)")
                local_ollama_path = os.path.join(get_base_dir(), "ollama.exe")
                subprocess.run([local_ollama_path, "pull", MODEL_NAME])
                print(f"Model {MODEL_NAME} pulled successfully.")
        except Exception as e:
            print(f"Error checking/pulling model: {e}")

    print("Starting Flask server...")
    app.run(host="127.0.0.1", port=5000, debug=False)
