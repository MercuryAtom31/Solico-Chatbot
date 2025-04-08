#!/bin/bash
# Start Ollama to serve the model in the background
echo "Starting Ollama..."
ollama serve --model mistral:7b-instruct &

# Save the process ID if you need to kill it later (optional)
OLLAMA_PID=$!

# Wait for 5 seconds to allow Ollama to initialize
sleep 5

# Start the Flask app
echo "Starting Flask app..."
python3 app.py

# Optionally, when the Flask app stops, kill the Ollama process:
kill $OLLAMA_PID
echo "Ollama stopped."
