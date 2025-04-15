from flask import Flask, request, Response, send_from_directory, jsonify
import os
import sys
import requests
import subprocess
import time
import json
from dotenv import load_dotenv
from search_module import SearchService
from query_analyzer import QueryAnalyzer

# Load environment variables
load_dotenv()

print("[DEBUG] SERPAPI_API_KEY after load_dotenv():", os.getenv("SERPAPI_API_KEY"))

app = Flask(__name__)

# Ollama settings
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "llama2"
USE_FLASH_ATTENTION = True


def get_base_dir():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def start_ollama():
    local_ollama_path = os.path.join(get_base_dir(), "ollama.exe" if sys.platform == "win32" else "ollama")

    try:
        requests.get("http://localhost:11434/api/health", timeout=1)
        print("Ollama is already running.")
        return True
    except requests.exceptions.RequestException:
        print("Starting Ollama...")
        try:
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.Popen(
                    [local_ollama_path, "serve"],
                    startupinfo=startupinfo,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                )
            else:
                subprocess.Popen(
                    [local_ollama_path, "serve"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

            for _ in range(10):
                time.sleep(1)
                try:
                    requests.get("http://localhost:11434/api/health", timeout=1)
                    print("Ollama started successfully.")
                    return True
                except:
                    continue

            print("Ollama failed to start properly.")
            return False
        except Exception as e:
            print(f"Error starting Ollama: {e}")
            return False


def query_llm(prompt):
    print("\n[query_llm] Final prompt being sent to Ollama:\n" + "-"*50)
    print(prompt)
    print("-"*50)

    options = {
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 500,
    }
    if USE_FLASH_ATTENTION:
        options["use_flash_attention"] = True

    try:
        response = requests.post(
            OLLAMA_API,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": options
            },
            timeout=60
        )
        response.raise_for_status()
        output = response.json().get("response", "").strip()
        print("[query_llm] Received response from Ollama.")
        return output
    except requests.exceptions.RequestException as e:
        print(f"[query_llm ERROR] Ollama API call failed: {e}")
        return "Sorry, I encountered an issue connecting to my brain."


@app.route("/")
def serve_index():
    root_dir = get_base_dir()
    return send_from_directory(root_dir, "index.html")


@app.route("/chat", methods=["GET"])
def chat_sse():
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

            response = requests.post(
                OLLAMA_API,
                json={
                    "model": MODEL_NAME,
                    "prompt": prompt,
                    "stream": True,
                    "options": options
                },
                stream=True,
                timeout=60
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        text_piece = chunk.get("response", "")
                        if text_piece:
                            yield f"data: {text_piece}\n\n"
                    except json.JSONDecodeError:
                        continue
        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama API: {e}")
            yield "data: Sorry, I'm having trouble connecting to my brain.\n\n"

    return Response(sse_generate(), mimetype='text/event-stream')


@app.route("/chat-augmented", methods=["POST"])
def chat_with_search():
    data = request.json
    user_input = data.get("message", "")
    is_online = data.get("isOnline", False)

    print("\n[chat_with_search] Received message:", user_input)
    print("[chat_with_search] Online toggle is:", is_online)

    search_service = SearchService()
    analyzer = QueryAnalyzer()

    needs_live_info = analyzer.needs_current_info(user_input)
    engine = analyzer.determine_search_engine(user_input)

    print("[chat_with_search] Needs live info:", needs_live_info)
    print("[chat_with_search] Selected engine:", engine)

    # if is_online and needs_live_info:
    if is_online:
        if engine == "google_news":
            results = search_service.google_news_search(user_input)
        else:
            results = search_service.google_search(user_input)

        print(f"[chat_with_search] Fetched {len(results)} results from search engine.")

        context = ""
        for i, r in enumerate(results, 1):
            context += f"[{i}] {r['title']}\nSource: {r['link']}\nSnippet: {r['snippet']}\n"
            if 'date' in r:
                context += f"Date: {r['date']}\n"
            context += "\n"

        prompt = f"""Answer the following question based on the provided web search context:

Question: {user_input}

Web Search Results:
{context}

Please include citations such as [1], [2], etc. when referring to search results.
"""
    else:
        print("[chat_with_search] Using user input as prompt without web context.")
        prompt = user_input

    result = query_llm(prompt)
    return jsonify({"response": result})


@app.route("/serpapi-usage", methods=["GET"])
def serpapi_usage():
    serpapi_key = os.getenv("SERPAPI_API_KEY")
    try:
        print("[DEBUG] .env SERPAPI_API_KEY loaded as:", serpapi_key)

        usage_resp = requests.get("https://serpapi.com/account", params={"api_key": serpapi_key})
        print("[DEBUG] Status Code:", usage_resp.status_code)
        print("[DEBUG] Response Headers:", usage_resp.headers)
        print("[DEBUG] Content-Type:", usage_resp.headers.get("Content-Type"))

        usage_data = usage_resp.json()
        print("[DEBUG] Parsed JSON:", usage_data)

        searches_used = usage_data.get("this_month_usage", 0)
        searches_limit = usage_data.get("searches_per_month", 100)

        return jsonify({
            "used": searches_used,
            "limit": searches_limit
        })

    except Exception as e:
        print("[ERROR] Exception while contacting SerpAPI:", e)
        return jsonify({"used": -1, "limit": -1})








if __name__ == "__main__":
    if start_ollama():
        try:
            print(f"Checking if {MODEL_NAME} is available...")
            model_list = requests.get("http://localhost:11434/api/tags").json()
            available = [m["name"] for m in model_list.get("models", [])]
            if MODEL_NAME not in available:
                print(f"Pulling {MODEL_NAME}... (first time may be slow)")
                local_ollama_path = os.path.join(get_base_dir(), "ollama.exe" if sys.platform == "win32" else "ollama")
                subprocess.run([local_ollama_path, "pull", MODEL_NAME])
                print(f"Model {MODEL_NAME} pulled successfully.")
        except Exception as e:
            print(f"Error checking/pulling model: {e}")

    print("Starting Flask server...")
    app.run(host="127.0.0.1", port=5000, debug=False)
