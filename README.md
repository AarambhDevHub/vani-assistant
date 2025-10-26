# 🎙️ Vani - Multilingual AI Voice Assistant with Desktop Control

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Ollama](https://img.shields.io/badge/Ollama-Compatible-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

**Your intelligent, multilingual voice companion with web search and desktop automation powered by local AI**

[Features](#features) • [Quick Start](#quick-start) • [Installation](#installation) • [Usage](#usage) • [Desktop Commands](#desktop-commands) • [Configuration](#configuration) • [Troubleshooting](#troubleshooting)

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
- 🖥️ **Desktop Automation** - Control your computer with voice commands
- 🔒 **Privacy First** - AI processing runs 100% locally (except TTS & web search)
- 💬 **Context-Aware** - Remembers conversation history
- 🎯 **Auto Language Detection** - Automatically detects and responds in your language

### Desktop Control Features 🆕
- **Open Applications** - Launch any installed app by voice
- **Close Applications** - Close running apps
- **Open Websites** - Open websites in specific browsers
- **System Information** - Check battery, CPU, memory usage
- **Screenshots** - Capture your screen
- **Volume Control** - Adjust system volume
- **File Search** - Find files on your computer
- **Smart Command Understanding** - Natural language commands

### Technical Highlights
- **Smart Command Detection** - Automatically knows when to search web or control desktop
- **Multi-Source Information** - DuckDuckGo + Wikipedia fallback
- **Intelligent URL Parsing** - Understands "Open YouTube in Firefox"
- **Process Management** - Reliable app opening and closing
- **Real-time voice interaction** with minimal latency
- **Optimized for Consumer Hardware** (8GB RAM, integrated GPU)
- **Production-Ready** with error handling and recovery
- **Cross-platform** (Ubuntu/Linux focus, adaptable to other OS)

### What Can Vani Do?

✅ **Answer factual questions** using Wikipedia  
✅ **Search the web** for current information  
✅ **Get latest news** from multiple sources  
✅ **Control your desktop** - open apps, websites, files  
✅ **System monitoring** - battery, CPU, memory  
✅ **Take screenshots** on command  
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

That's it! Vani is ready to talk and control your desktop! 🎉

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
    wget \
    amixer
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
│   ├── web_search.py             # Web search & Wikipedia integration
│   └── desktop_automation.py     # Desktop control system 🆕
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

### Desktop Commands 🆕

#### Open Applications
```
You: "Open terminal"
Vani: "Opening terminal"

You: "Launch Firefox"
Vani: "Opening firefox"

You: "Start calculator"
Vani: "Opening calculator"
```

#### Open Websites
```
You: "Open YouTube in Firefox"
Vani: "Opening youtube.com in firefox"

You: "Go to Google"
Vani: "Opening google.com in default browser"

You: "Visit GitHub in Chrome"
Vani: "Opening github.com in chrome"
```

#### Close Applications
```
You: "Close terminal"
Vani: "Closed terminal"

You: "Quit Firefox"
Vani: "Closed firefox"

You: "Exit Chrome"
Vani: "Closed chrome"
```

#### System Commands
```
You: "Take a screenshot"
Vani: "Screenshot saved to /home/user/Pictures/screenshot_20251026_103045.png"

You: "What's my battery level?"
Vani: "Battery: 75% (on battery)"

You: "Check system status"
Vani: "CPU: 45%, Memory: 60%, Battery: 75%"

You: "Volume up"
Vani: "Volume increased"

You: "Mute volume"
Vani: "Volume muted"
```

### Web Search Examples

```
You: "Latest news about India"
Vani: *Searches web* "According to recent reports..."

You: "What's the weather in Mumbai?"
Vani: *Searches web* "Current weather in Mumbai..."

You: "Bitcoin price now"
Vani: *Searches web* "The current Bitcoin price is..."
```

### Knowledge Queries

```
You: "What is Python?"
Vani: *Searches Wikipedia* "Python is a high-level programming language..."

You: "Who is Mahatma Gandhi?"
Vani: *Searches Wikipedia* "Mahatma Gandhi was an Indian lawyer..."
```

### Multilingual Conversations

**English:**
```
You: "Hello Vani, who are you?"
Vani: "I am Vani, your multilingual AI voice assistant with web search and desktop control!"
```

**Hindi (हिन्दी):**
```
You: "टर्मिनल खोलो"
Vani: "terminal खोल दिया"

You: "आज की ताज़ा खबर क्या है?"
Vani: *वेब खोज* "हाल की रिपोर्टों के अनुसार..."
```

**Gujarati (ગુજરાતી):**
```
You: "ટર્મિનલ ખોલો"
Vani: "terminal ખોલ્યું"

You: "મુંબઈમાં હવામાન કેવું છે?"
Vani: *વેબ શોધ* "વર્તમાન હવામાન..."
```

### Voice Commands Reference

| Category | Commands | Languages |
|----------|----------|-----------|
| **Apps** | "open/launch/start [app]" | All |
| **Websites** | "open/go to [site] in [browser]" | All |
| **Close** | "close/quit/exit [app]" | All |
| **Screenshot** | "take screenshot/capture screen" | All |
| **System** | "battery/cpu/memory/system status" | All |
| **Volume** | "volume up/down/mute" | All |
| **Identity** | "who are you" | All |
| **Exit** | "goodbye/bye/exit" | All |
| **Reset** | "reset conversation" | All |

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

# Desktop Automation
ENABLE_DESKTOP_CONTROL = True      # Enable/disable desktop automation

# Audio Settings
SILENCE_THRESHOLD = 3000           # Microphone sensitivity
RECORD_SECONDS = 10                # Maximum recording duration
```

### Model Comparison

| Model | Size | Speed | Quality | Multilingual | Desktop | Best For |
|-------|------|-------|---------|--------------|---------|----------|
| **llama3.2:3b** ⭐ | 2GB | Fast | Excellent | ⭐⭐⭐⭐⭐ | ✅ | **Recommended** |
| llama3.3:1b | 1GB | Very Fast | Very Good | ⭐⭐⭐⭐ | ✅ | Low-resource systems |
| phi3:latest | 2.3GB | Medium | Good | ⭐⭐ | ✅ | English-focused |
| gemma2:2b | 1.5GB | Fast | Very Good | ⭐⭐⭐⭐⭐ | ✅ | 140+ languages |

---

## 🔧 Troubleshooting

### Desktop Control Issues

#### ❌ Application Won't Open

**Problem:** Desktop commands not working

**Solution:**
```
# Verify application is installed
which firefox  # Should show path if installed

# Install missing applications
sudo apt-get install firefox gnome-terminal nautilus

# Check desktop_automation.py apps dictionary
# Add custom applications if needed
```

#### ❌ Website Won't Open

**Problem:** "Could not open website"

**Solution:**
- Ensure default browser is set: `xdg-settings set default-web-browser firefox.desktop`
- Try specifying browser: "Open YouTube **in Firefox**"

#### ❌ Can't Close Application

**Problem:** Application still running after close command

**Solution:**
- The app might have a different process name
- Use: `ps aux | grep [app-name]` to find actual process name
- Update `proc_map` in `desktop_automation.py`

### Web Search Timeout

**Problem:** `DuckDuckGo search failed: operation timed out`

**Solution:**
```
# In src/web_search.py, increase timeout
self.ddgs = DDGS(timeout=30)  # Increase from 20 to 30 seconds
```

### Poor Speech Recognition

**Problem:** Whisper not transcribing correctly

**Solutions:**
1. **Speak closer to microphone** (6-12 inches)
2. **Reduce background noise**
3. **Upgrade Whisper model:**
   ```
   WHISPER_MODEL = "large"  # In config.py
   ```
4. **Adjust microphone sensitivity:**
   ```
   SILENCE_THRESHOLD = 4000  # Higher = require louder speech
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

# Desktop Automation
pyautogui>=0.9.54
pynput>=1.7.6
psutil>=5.9.0
pillow>=10.0.0
```

---

## 🙏 Acknowledgments

- **OpenAI Whisper** - Speech recognition technology
- **Ollama** - Local LLM inference
- **Meta Llama** - Open-source language models
- **Google TTS** - Text-to-speech synthesis
- **faster-whisper** - Optimized Whisper implementation
- **DuckDuckGo** - Web search API
- **Wikipedia** - Knowledge base
- **PyAutoGUI** - Desktop automation
- **psutil** - System monitoring

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⭐ Star History

If you find Vani useful, please consider giving it a star on GitHub!

---

<div align="center">

**Made with ❤️ for the open-source community**

*Empowering multilingual voice interactions with local AI, web search, and desktop automation*

[⬆ Back to Top](#-vani---multilingual-ai-voice-assistant-with-desktop-control)

</div>
