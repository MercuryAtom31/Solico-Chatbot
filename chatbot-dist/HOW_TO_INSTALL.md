# Solisco Chatbot

This package contains the Solisco Chatbot—a self-contained, offline chatbot that uses Ollama along with a Llama2 or Mistral model to handle business inquiries. The application runs locally on your Windows laptop and is designed for use by our sales team.

## What's Included

- **app.py**: The Flask-based backend for the chatbot.
- **index.html**: The frontend HTML file for the chatbot UI.
- **requirements.txt**: A list of required Python packages (Flask and requests).
- **ollama.exe**: The Ollama executable (copied from your local installation).
- **start-chatbot.bat**: A batch file that starts Ollama and the Flask app.
- **README.md**: This instructions file.

> **Note:** The actual model is not bundled with this package. When the chatbot runs, Ollama will automatically pull the required model (e.g., `llama2:latest` or `mistral:7b-instruct`) if it isn’t already installed on your machine.

## Prerequisites

- **Python 3.8 or Higher**: Ensure that Python is installed on your laptop. Download it from [python.org](https://www.python.org/downloads/).
- **Internet Connection (for initial model download)**: The first time you run the chatbot, Ollama may need to download model layers.
- **Windows Operating System**: This package is designed for Windows.

## Installation & Setup Instructions

1. **Unzip the Package**  
   Unzip the provided `chatbot-dist.zip` file to a folder on your laptop (e.g., `C:\Solisco Chatbot`).

2. **Install Python Dependencies**  
   Before running the chatbot, you need to install the required Python packages.
   - Open a Command Prompt or PowerShell window.
   - Navigate to the unzipped folder (e.g., `C:\Solisco Chatbot\chatbot-dist`):
     ```cmd
     cd "C:\Solisco Chatbot\chatbot-dist"
     ```
   - Run the following command:
     ```cmd
     pip install -r requirements.txt
     ```
   This command installs Flask and requests, which are required by the chatbot application.

3. **Run the Application**  
   - Double-click the `start-chatbot.bat` file in the `chatbot-dist` folder, **or**
   - From the same Command Prompt/PowerShell window, run:
     ```cmd
     .\start-chatbot.bat
     ```
   The batch file will:
   - Launch `ollama.exe` in a separate window to serve the model.
   - Wait a few seconds for Ollama to start.
   - Start the Flask application (`app.py`).

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

- **Module Not Found Error**:  
If you receive an error like `ModuleNotFoundError: No module named 'flask'`, make sure you have installed the dependencies with:
```cmd
pip install -r requirements.txt
