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
        "\nFORMATTING INSTRUCTIONS - ALWAYS FOLLOW THESE:\n"
        "1. For numbered lists, start each item on a new line with a number and period (1., 2., etc.)\n"
        "   CRITICAL: PUT A BLANK LINE BETWEEN EACH NUMBERED LIST ITEM like this:\n"
        "   1. First item text here\n\n"
        "   2. Second item text here\n\n"
        "   3. Third item text here\n\n"
        "   IMPORTANT: Continue with proper sequencing for all numbered lists (1,2,3,...10,11,12, etc.)\n"
        "   DO NOT restart numbering at 0 or 1 after reaching 9. Always use correct sequential numbers.\n"
        "2. For bullet lists, use * or - symbols, with each item on a new line and add blank lines between items\n"
        "3. IMPORTANT: Always separate distinct topics with blank lines (two newlines)\n"
        "4. Use clear paragraph breaks to organize information\n"
        "5. When explaining a complex topic, break it down into separate, clearly defined sections\n"
        "6. For emphasis, use *italic* or **bold** format\n"
        "7. For technical terms or code examples, use `code format`\n"
        "8. Ensure proper spacing between all content elements - this is critical for readability\n"
        "9. When introducing a list after a colon, always insert a newline first, like this:\n"
        "   \"Here are my top tips:\n\n1. First tip\"\n"
        "   NOT like this: \"Here are my top tips:1. First tip\"\n"
        "\nNever format lists like this: \"1. First item 2. Second item\" - there MUST be clear separation\n"
        "between numbered items using blank lines. The user interface relies on proper spacing to\n"
        "format your responses correctly.\n"
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
                        if chunk.get("done", False):
                            yield f"event: done\ndata: complete\n\n"
                        elif text_piece:
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
