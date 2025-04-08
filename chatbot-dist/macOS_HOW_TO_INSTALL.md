## Running on macOS

Follow these steps to set up and run the Solisco Chatbot on a Mac:

### 1. Install Prerequisites

- **Python 3.8 or Higher:**
  - Download the latest version from [python.org](https://www.python.org/downloads/), or install via Homebrew by running:
    ```bash
    brew install python
    ```
  - Verify the installation by opening Terminal and typing:
    ```bash
    python3 --version
    ```

- **Ollama:**
  - Visit [https://ollama.ai](https://ollama.ai) and download the macOS version of Ollama.
  - Follow the provided instructions to install Ollama on your system.
  - Ensure that the `ollama` command is available in your Terminal. You can check this by typing:
    ```bash
    which ollama
    ```
  - If it doesn’t appear, you might need to add its installation directory to your PATH.

### 2. Unzip the Package

- Unzip `chatbot-dist.zip` to a convenient location on your Mac, for example:
  ```bash
  ~/Desktop/chatbot-dist
  
### 3. Install Python Dependencies

- Open Terminal and navigate to the unzipped folder, for example:
  ```bash
  cd ~/Desktop/chatbot-dist
- Install the required Python packages by running:
  ```bash
  pip3 install -r requirements.txt
  
### 4. Prepare the Startup Shell Script

- Ensure that the provided shell script start-chatbot.sh is executable. If it is not yet executable, run:
  ```bash
  chmod +x start-chatbot.sh
  
### 5. Run the Chatbot

- In Terminal, from within the chatbot-dist folder, start the chatbot by running:
  ```bash
  ./start-chatbot.sh
  
> **Note:** The script will:
- Start Ollama in the background to serve the specified model (e.g., llama2:latest or mistral:7b-instruct).
- Wait for 5 seconds to allow Ollama to initialize.
- Start the Flask app (app.py), which hosts the chatbot interface.

4. **Access the Chatbot**  
   Open your web browser and navigate to:

http://127.0.0.1:5000

You should see the chatbot interface load. Test the functionality by sending a message.

## How It Works

- **Ollama**:  
The application uses `ollama.exe` to serve the model. If the specified model (e.g., `llama2:latest` or `mistral:7b-instruct`) is not already present, Ollama will automatically download it.

- **Flask App**:  
The Flask backend listens on port 5000 and uses server-sent events (SSE) for real-time streaming of responses from the model.

## Troubleshooting

**Command Not Found Errors**:  
- If you see an error like command not found: ollama, ensure that Ollama is installed and that its path is added to your shell's PATH variable.
- If python3 is not recognized, verify your Python installation.

**Dependency Issues:**: 

- If you encounter errors related to missing Python packages, re-run:
  ```bash
  pip3 install -r requirements.txt
  
**Model Download Delays:**: 

- The first run may take time as Ollama downloads model layers. Ensure you have a stable internet connection.
