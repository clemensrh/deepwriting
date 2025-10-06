#!/bin/bash

# Simple script to start the DeepWriting web interface
# Usage: ./start_web_interface.sh [model_path] [port]

# Default values
MODEL_PATH="${1:-./model/tf-1514981744-deepwriting_synthesis_model}"
PORT="${2:-5000}"

echo "==========================================="
echo "  DeepWriting Web Interface"
echo "==========================================="
echo ""
echo "Model path: $MODEL_PATH"
echo "Port: $PORT"
echo ""

# Check if model exists
if [ ! -d "$MODEL_PATH" ]; then
    echo "ERROR: Model directory not found: $MODEL_PATH"
    echo ""
    echo "Please download the model from:"
    echo "  https://files.ait.ethz.ch/projects/deepwriting/tf-1514981744-deepwriting_synthesis_model.tar.gz"
    echo ""
    echo "Then extract it to the model directory."
    exit 1
fi

# Check if data exists
if [ ! -f "./data/deepwriting_validation.npz" ]; then
    echo "WARNING: Validation dataset not found at ./data/deepwriting_validation.npz"
    echo ""
    echo "The model requires the validation dataset. Please download from:"
    echo "  https://files.ait.ethz.ch/projects/deepwriting/deepwriting_dataset.zip"
    echo ""
    echo "Press Ctrl+C to abort, or any other key to continue anyway..."
    read -n 1 -s
    echo ""
fi

# Set PYTHONPATH
export PYTHONPATH=$PYTHONPATH:./source

echo "Starting web interface..."
echo "Open your browser to: http://localhost:$PORT"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask app
python app.py -M "$MODEL_PATH" -P "$PORT"
