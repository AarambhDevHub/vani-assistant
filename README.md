# 🎙️ Vani - Multilingual AI Voice Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Ollama](https://img.shields.io/badge/Ollama-Compatible-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

**Your intelligent, multilingual voice companion with web search powered by local AI**

[Features](#features) • [Quick Start](#quick-start) • [Installation](#installation) • [Usage](#usage) • [Configuration](#configuration) • [Troubleshooting](#troubleshooting)

</div>

---

## 🌟 Features

### Core Capabilities
- 🎤 **Advanced Speech Recognition** - faster-whisper (4x faster than standard Whisper)
- 🤖 **Local AI Processing** - Powered by Ollama (Llama 3.2 3B / Llama 3.3 1B)
- 🔊 **Natural Text-to-Speech** - Google TTS with language-specific accents
- 🌍 **Multilingual Support** - English, Hindi (हिन्दी), Gujarati (ગુજરાતી)
- 🌐 **Web Search Integration** - Real-time information from DuckDuckGo
- 📚 **Wikipedia Integration** - Accurate knowledge retrieval
- 🔒 **Privacy First** - AI processing runs 100% locally (except TTS & web search)
- 💬 **Context-Aware** - Remembers conversation history
- 🎯 **Auto Language Detection** - Automatically detects and responds in your language

### Technical Highlights
- **Smart Search Detection** - Automatically knows when to search the web
- **Multi-Source Information** - DuckDuckGo + Wikipedia fallback
- **Real-time voice interaction** with minimal latency
- **Optimized for Consumer Hardware** (8GB RAM, integrated GPU)
- **Production-Ready** with error handling and recovery
- **Cross-platform** (Ubuntu/Linux focus, adaptable to other OS)

### What Can Vani Do?

✅ **Answer factual questions** using Wikipedia  
✅ **Search the web** for current information  
✅ **Get latest news** from multiple sources  
✅ **Multilingual conversations** in 3 languages  
✅ **Context-aware chat** remembering conversation history  
✅ **Explain complex topics** with detailed information  

---

## 🚀 Quick Start

### Prerequisites

- **OS**: Ubuntu 20.04+ (or any Linux distribution)
- **Python**: 3.8 or higher
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 5GB free space for models
- **Internet**: Required for initial setup, TTS, and web search
- **Microphone**: Any USB or built-in microphone

### One-Command Setup

```
# Clone the repository
git clone https://github.com/AarambhDevHub/vani-assistant.git
cd vani-assistant

# Run automated setup
chmod +x setup.sh
./setup.sh

# Start Ollama (in separate terminal)
ollama serve

# Pull the AI model (recommended)
ollama pull llama3.2:3b

# Activate environment and launch Vani
source venv/bin/activate
python -m src.main
```

That's it! Vani is ready to talk 🎉

---

## 📦 Installation

### Step-by-Step Installation

#### 1. System Dependencies (Ubuntu/Debian)

```
sudo apt-get update
sudo apt-get install -y \
    portaudio19-dev \
    python3-dev \
    python3-pip \
    espeak \
    espeak-ng \
    ffmpeg \
    build-essential \
    wget
```

#### 2. Install Ollama

```
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve

# In another terminal, pull the model
ollama pull llama3.2:3b
```

#### 3. Project Setup

```
# Create project directory
mkdir vani-assistant
cd vani-assistant

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Download Voice Models

```
# Download faster-whisper model (automatic on first run)
# Or pre-download for offline use:
python -c "from faster_whisper import WhisperModel; WhisperModel('medium')"
```

---

## 📁 Project Structure

```
vani-assistant/
├── venv/                          # Virtual environment
├── src/                           # Source code
│   ├── __init__.py               # Package initializer
│   ├── main.py                   # Main application entry point
│   ├── config.py                 # Configuration settings
│   ├── audio_utils.py            # Audio recording utilities
│   ├── stt_handler.py            # Speech-to-text (faster-whisper)
│   ├── llm_handler.py            # LLM integration (Ollama)
│   ├── tts_google.py             # Text-to-speech (Google TTS)
│   └── web_search.py             # Web search & Wikipedia integration
├── models/                        # Downloaded voice models (auto-created)
├── requirements.txt               # Python dependencies
├── setup.sh                       # Automated setup script
├── .gitignore                     # Git ignore file
└── README.md                      # This file
```

---

## 🎯 Usage

### Starting Vani

```
# Make sure Ollama is running
ollama serve

# Activate virtual environment
source venv/bin/activate

# Run Vani
python -m src.main
```

### Voice Commands

#### Basic Interaction
```
You: "Hello Vani!"
Vani: "Hello! How can I help you today?"

You: "What is Python?"
Vani: *Searches Wikipedia* "Python is a high-level programming language..."

You: "Latest news about India"
Vani: *Searches web* "According to recent reports..."

You: "Thank you, goodbye"
Vani: "Goodbye! Vani signing off."
```

#### Web Search Examples

```
You: "What's the weather in Mumbai today?"
Vani: *Searches web* "According to current reports, Mumbai has..."

You: "Who won the cricket match?"
Vani: *Searches news* "In the recent match..."

You: "Bitcoin price now"
Vani: *Searches web* "The current Bitcoin price is..."
```

#### Multilingual Conversations

**English:**
```
You: "Hello Vani, who are you?"
Vani: "I am Vani, your multilingual AI voice assistant with web search capability!"
```

**Hindi (हिन्दी):**
```
You: "आज की ताज़ा खबर क्या है?"
Vani: *वेब खोज* "हाल की रिपोर्टों के अनुसार..."
```

**Gujarati (ગુજરાતી):**
```
You: "મુંબઈમાં હવામાન કેવું છે?"
Vani: *વેબ શોધ* "વર્તમાન અહેવાલો અનુસાર..."
```

### Special Commands

| Command | Description | Languages |
|---------|-------------|-----------|
| `"who are you"` / `"तुम कौन हो"` / `"તમે કોણ છો"` | Ask about Vani's identity | All |
| `"goodbye"` / `"अलविदा"` / `"અલવિદા"` | Exit the application | All |
| `"reset"` / `"रीसेट"` / `"રીસેટ"` | Clear conversation history | All |
| `"latest news"` / `"ताज़ा खबर"` / `"તાજા સમાચાર"` | Search for news | All |
| `Ctrl+C` | Force quit | - |

---

## ⚙️ Configuration

### Customize Vani

Edit `src/config.py` to personalize your assistant:

```
# Assistant Identity
ASSISTANT_NAME = "Vani"           # Change to your preferred name
ASSISTANT_NAME_HI = "वाणी"        # Hindi name
ASSISTANT_NAME_GU = "વાણી"        # Gujarati name

# AI Model Selection
OLLAMA_MODEL = "llama3.2:3b"      # Options: llama3.2:3b, llama3.3:1b, phi3:latest

# Speech Recognition Model
WHISPER_MODEL = "medium"           # Options: tiny, base, small, medium, large

# Web Search Settings
ENABLE_WEB_SEARCH = True           # Enable/disable web search
WEB_SEARCH_MAX_RESULTS = 5         # Number of search results

# Audio Settings
SILENCE_THRESHOLD = 3000           # Microphone sensitivity
RECORD_SECONDS = 10                # Maximum recording duration
```

### Popular Name Suggestions

| Name | Meaning | Script |
|------|---------|--------|
| **Vani** ⭐ | Voice | वाणी / વાણી |
| **Saral** | Simple/Easy | सरल / સરળ |
| **Mitra** | Friend | मित्र / મિત્ર |
| **Bodhi** | Enlightenment | बोधि / બોધિ |
| **Aria** | Musical/Air | - |
| **Echo** | Tech-inspired | - |

### Model Comparison

| Model | Size | Speed | Quality | Multilingual | Best For |
|-------|------|-------|---------|--------------|----------|
| **llama3.2:3b** ⭐ | 2GB | Fast | Excellent | ⭐⭐⭐⭐⭐ | **Recommended** |
| llama3.3:1b | 1GB | Very Fast | Very Good | ⭐⭐⭐⭐ | Low-resource systems |
| phi3:latest | 2.3GB | Medium | Good | ⭐⭐ | English-focused |
| gemma2:2b | 1.5GB | Fast | Very Good | ⭐⭐⭐⭐⭐ | 140+ languages |

---

## 🔧 Troubleshooting

### Common Issues

#### ❌ Web Search Timeout

**Problem:** `DuckDuckGo search failed: operation timed out`

**Solution:**
```
# In src/web_search.py, increase timeout
self.ddgs = DDGS(timeout=20)  # Increase from default 10 to 20 seconds
```

#### ❌ Wikipedia Not Found

**Problem:** Wikipedia returns no results

**Solution:**
- Vani automatically falls back to web search
- Wikipedia works best for factual "what is" questions
- Try rephrasing: "What is Python?" instead of "Tell me Python"

#### ❌ Microphone Not Detected

**Problem:** No audio input detected

**Solution:**
```
# Test your microphone
arecord -d 5 test.wav
aplay test.wav

# Check available devices
python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"

# Install PulseAudio controls
sudo apt-get install pavucontrol
pavucontrol  # Adjust input device
```

#### ❌ Ollama Connection Error

**Problem:** `Cannot connect to Ollama`

**Solution:**
```
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Verify model is available
ollama list
```

#### ❌ Poor Speech Recognition

**Problem:** Whisper not transcribing correctly

**Solutions:**
1. **Speak closer to microphone** (6-12 inches)
2. **Reduce background noise** (turn off fans, music)
3. **Upgrade Whisper model:**
   ```
   # In config.py
   WHISPER_MODEL = "large"  # Better accuracy but slower
   ```
4. **Adjust microphone sensitivity:**
   ```
   # In config.py
   SILENCE_THRESHOLD = 4000  # Higher = require louder speech
   ```

#### ❌ TTS Not Working

**Problem:** No audio output from text-to-speech

**Solution:**
```
# Check internet connection (gTTS requires internet)
ping -c 3 google.com

# Install pygame dependencies
sudo apt-get install python3-pygame

# Test pygame
python -c "import pygame; pygame.mixer.init(); print('OK')"
```

### Performance Optimization

#### For 8GB RAM Systems

```
# In config.py
WHISPER_MODEL = "small"          # Use smaller model
OLLAMA_MODEL = "llama3.3:1b"     # Use 1B parameter model
WEB_SEARCH_MAX_RESULTS = 3       # Fewer search results
```

#### For Better Accuracy

```
# In config.py
WHISPER_MODEL = "medium"         # or "large" if you have 16GB+ RAM
OLLAMA_MODEL = "llama3.2:3b"     # Best multilingual support
WEB_SEARCH_MAX_RESULTS = 5       # More comprehensive results
```

---

## 📊 System Requirements

### Minimum Requirements
- **CPU:** Intel Core i5 (8th gen) or AMD Ryzen 5
- **RAM:** 8GB
- **Storage:** 5GB free space
- **Internet:** For TTS and web search

### Recommended Requirements
- **CPU:** Intel Core i7 or AMD Ryzen 7
- **RAM:** 16GB
- **Storage:** 10GB free space
- **Internet:** Broadband connection

### Tested Systems
- ✅ ASUS VivoBook 14 (Intel i5-1135G7, 8GB RAM) - **Works Great**
- ✅ Ubuntu 20.04 LTS
- ✅ Ubuntu 22.04 LTS
- ✅ Ubuntu 24.04 LTS

---

## 📝 Requirements

**requirements.txt:**
```
# Core dependencies
faster-whisper>=1.0.0
SpeechRecognition>=3.10.0
sounddevice>=0.4.6
requests>=2.31.0
pyaudio>=0.2.14

# Whisper dependencies
torch>=2.0.0
torchaudio>=2.0.0
ffmpeg-python

# TTS
gtts>=2.3.0
pygame>=2.5.0

# Web Search & Knowledge
duckduckgo-search>=5.0.0
beautifulsoup4>=4.12.0
wikipedia-api>=0.6.0
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```
# Fork and clone the repository
git clone https://github.com/yourusername/vani-assistant.git
cd vani-assistant

# Create a new branch
git checkout -b feature/your-feature-name

# Make your changes and commit
git add .
git commit -m "Add your feature"

# Push to your fork
git push origin feature/your-feature-name

# Create a Pull Request
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI Whisper** - Speech recognition technology
- **Ollama** - Local LLM inference
- **Meta Llama** - Open-source language models
- **Google TTS** - Text-to-speech synthesis
- **faster-whisper** - Optimized Whisper implementation
- **DuckDuckGo** - Web search API
- **Wikipedia** - Knowledge base

---

## 📧 Support

### Getting Help

- 📖 Check the [Troubleshooting](#troubleshooting) section
- 💬 Open an [Issue](https://github.com/yourusername/vani-assistant/issues)
- 📧 Email: your.email@example.com

### Resources

- [Ollama Documentation](https://ollama.com/docs)
- [Whisper Documentation](https://github.com/openai/whisper)
- [faster-whisper GitHub](https://github.com/SYSTRAN/faster-whisper)
- [DuckDuckGo Search](https://github.com/deedy5/duckduckgo_search)

---

## ⭐ Star History

If you find Vani useful, please consider giving it a star on GitHub!

---

<div align="center">

**Made with ❤️ for the open-source community**

*Empowering multilingual voice interactions with local AI and web search*

[⬆ Back to Top](#-vani---multilingual-ai-voice-assistant)

</div>
