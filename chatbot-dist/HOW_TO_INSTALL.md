# Solisco Chatbot

This package contains the Solisco Chatbot—a self-contained, offline chatbot that uses Ollama along with a Llama2 or Mistral model to handle business inquiries. The application runs locally on your Windows laptop and is designed for use by the sales team.

## What's Included

- **app.py**: The Flask-based backend for the chatbot.
- **index.html**: The frontend HTML file for the chatbot UI.
- **requirements.txt**: A list of required Python packages (Flask and requests).
- **ollama.exe**: The Ollama executable (copied from your local installation).
- **start-chatbot.bat**: A batch file that starts Ollama and the Flask app.
- **HOW_TO_INSTALL.md**: The steps to follow for installing Solisco Chatbot.
> **Note:** The actual model is not bundled with this package. When the chatbot runs, Ollama will automatically pull the required model (e.g., `llama2:latest` or `mistral:7b-instruct`) if it isn’t already installed on your machine.

## Prerequisites

- **Python 3.8 or Higher**: Ensure that Python is installed on your laptop. Download it from [python.org](https://www.python.org/downloads/).
- **Internet Connection (for initial model download)**: The first time you run the chatbot, Ollama may need to download model layers.
- **Windows Operating System**: This package is designed for Windows.

## Installation & Setup Instructions

1. **Unzip the Package**  
   Unzip the provided `chatbot-dist.zip` file to a folder on your laptop (for example, `C:\Solisco Chatbot`).

2. **Install Python Dependencies**  
   Open a Command Prompt or PowerShell window in the `chatbot-dist` folder and run:
   ```cmd
   pip install -r requirements.txt
