#!/bin/bash

echo "🚀 Setting up Ollama Voice Assistant..."
echo "======================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Install system dependencies for Ubuntu
echo "📦 Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y portaudio19-dev python3-pyaudio espeak ffmpeg wget

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install -r requirements.txt

# Download Piper voice model
echo "📥 Downloading Piper TTS voice model..."
mkdir -p models/voices
cd models/voices

if [ ! -f "en_US-amy-medium.onnx" ]; then
    echo "Downloading voice model..."
    wget "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/medium/en_US-amy-medium.onnx" -O en_US-amy-medium.onnx
    wget "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/amy/medium/en_US-amy-medium.onnx.json" -O en_US-amy-medium.onnx.json
else
    echo "Voice model already exists"
fi

cd ../..

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start using the voice assistant:"
echo "1. Make sure Ollama is running: ollama serve"
echo "2. Activate the environment: source venv/bin/activate"
echo "3. Run the assistant: python -m src.main"
