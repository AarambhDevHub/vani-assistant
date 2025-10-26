# 🎙️ Vani - Multilingual AI Voice Assistant with Vision

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Ollama](https://img.shields.io/badge/Ollama-Compatible-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

**Your intelligent, multilingual voice companion with vision, web search and desktop automation powered by local AI**

[Features](#features) • [Quick Start](#quick-start) • [Installation](#installation) • [Usage](#usage) • [Vision Commands](#vision-commands) • [Desktop Commands](#desktop-commands) • [Configuration](#configuration)

</div>

---

## 🌟 Features

### Core Capabilities
- 🎤 **Advanced Speech Recognition** - faster-whisper (4x faster than standard Whisper)
- 🤖 **Dual AI Models** - Llama 3.2 3B for conversation + Moondream for vision
- 👁️ **Computer Vision** - See through camera and understand images 🆕
- 🔊 **Natural Text-to-Speech** - Google TTS with language-specific accents
- 🌍 **Multilingual Support** - English, Hindi (हिन्दी), Gujarati (ગુજરાતી)
- 🌐 **Web Search Integration** - Real-time information from DuckDuckGo
- 📚 **Wikipedia Integration** - Accurate knowledge retrieval
- 🖥️ **Desktop Automation** - Control your computer with voice commands
- 🔒 **Privacy First** - AI processing runs 100% locally (except TTS & web search)
- 💬 **Context-Aware** - Remembers conversation and visual context
- 🎯 **Auto Language Detection** - Automatically detects and responds in your language

### Vision Capabilities 🆕
- **See and Describe** - Camera access with intelligent image analysis
- **Object Recognition** - Identify and count objects, people
- **Text Reading** - Read text, signs, labels from camera
- **Time Reading** - Read time from clocks and watches
- **Color Detection** - Identify and describe colors
- **Scene Understanding** - Understand location and context
- **Multilingual Vision** - Vision responses in 3 languages
- **Smart Question Answering** - Ask anything about what camera sees

### Desktop Control Features
- **Open Applications** - Launch any installed app by voice
- **Close Applications** - Close running apps
- **Open Websites** - Open websites in specific browsers
- **System Information** - Check battery, CPU, memory usage
- **Screenshots** - Capture your screen
- **Volume Control** - Adjust system volume
- **File Search** - Find files on your computer
- **Smart Command Understanding** - Natural language commands

### Technical Highlights
- **Multi-Model Architecture** - Moondream (vision) + Llama 3.2 (text)
- **Smart Command Detection** - Auto-activates camera when needed
- **Vision Context Memory** - Remembers what it saw for follow-up questions
- **Multi-Source Information** - DuckDuckGo + Wikipedia + Camera
- **Intelligent URL Parsing** - Understands complex commands
- **Real-time Processing** with minimal latency
- **Optimized for Consumer Hardware** (8GB RAM, integrated GPU)
- **Production-Ready** with error handling and recovery

### What Can Vani Do?

✅ **See and understand** through your camera  
✅ **Read text, time, prices** from images  
✅ **Count people and objects** in view  
✅ **Answer questions** about visual content  
✅ **Search the web** for current information  
✅ **Get latest news** from multiple sources  
✅ **Control your desktop** - apps, websites, files  
✅ **System monitoring** - battery, CPU, memory  
✅ **Multilingual conversations** in 3 languages  
✅ **Context-aware chat** with visual memory  

---

## 🚀 Quick Start

### Prerequisites

- **OS**: Ubuntu 20.04+ (or any Linux distribution)
- **Python**: 3.8 or higher
- **RAM**: 8GB minimum (16GB recommended for vision)
- **Storage**: 7GB free space for models
- **Internet**: Required for initial setup, TTS, and web search
- **Microphone**: Any USB or built-in microphone
- **Camera**: Webcam for vision features 🆕

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

# Pull the AI models
ollama pull llama3.2:3b    # For conversation
ollama pull moondream      # For vision 🆕

# Activate environment and launch Vani
source venv/bin/activate
python -m src.main
```

That's it! Vani is ready to see, talk and control your desktop! 🎉

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
    amixer \
    v4l-utils  # Camera tools
```

#### 2. Install Ollama & Models

```
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve

# Pull models
ollama pull llama3.2:3b    # Text/conversation model
ollama pull moondream      # Vision model 🆕
```

#### 3. Test Camera

```
# Check if camera is detected
ls /dev/video*

# Test camera (optional)
ffplay /dev/video0
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
│   ├── web_search.py             # Web search & Wikipedia
│   ├── desktop_automation.py     # Desktop control
│   ├── vision_handler.py         # Camera & vision 🆕
│   └── multi_model_handler.py    # Vision + Text coordination 🆕
├── requirements.txt               # Python dependencies
├── setup.sh                       # Automated setup script
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

### Vision Commands 🆕

#### Basic Vision
```
You: "What do you see?"
Vani: *Activates camera* "I can see: A person sitting at a desk with a laptop..."

You: "Describe what you see"
Vani: *Captures and analyzes* "Looking at the camera: A room with blue walls..."
```

#### Reading Text & Time
```
You: "What time does the clock show?"
Vani: *Reads clock* "I can see: The clock shows 3:30 PM"

You: "Read the text on the screen"
Vani: *Reads text* "I can see: The screen displays 'Welcome to Ubuntu'"

You: "What's written on the paper?"
Vani: *Reads paper* "I can see: The paper says 'Meeting at 5 PM'"
```

#### Counting & Recognition
```
You: "How many people are in the room?"
Vani: *Counts people* "I can see: There are 2 people in this image"

You: "How many chairs do you see?"
Vani: *Counts objects* "I can see: There are 3 chairs visible"

You: "What color is the wall?"
Vani: *Analyzes colors* "I can see: The wall is blue"
```

#### Multilingual Vision

**Hindi:**
```
You: "क्या दिख रहा है?"
Vani: "मैं देख रहा हूं: एक व्यक्ति कंप्यूटर पर काम कर रहा है..."

You: "घड़ी में क्या समय है?"
Vani: "मैं देख रहा हूं: घड़ी 3:30 बजे दिखा रही है"
```

**Gujarati:**
```
You: "તમે શું જુઓ છો?"
Vani: "હું જોઈ રહ્યો છું: એક વ્યક્તિ ડેસ્ક પર બેઠો છે..."

You: "ઘડિયાળમાં કેટલો સમય છે?"
Vani: "હું જોઈ રહ્યો છું: ઘડિયાળ 3:30 બતાવે છે"
```

### Desktop Commands

#### Open Applications
```
You: "Open terminal"
Vani: "Opening terminal"

You: "Launch Firefox"
Vani: "Opening firefox"
```

#### Open Websites
```
You: "Open YouTube in Firefox"
Vani: "Opening youtube.com in firefox"

You: "Go to Google"
Vani: "Opening google.com"
```

#### System Commands
```
You: "Take a screenshot"
Vani: "Screenshot saved to /home/user/Pictures/..."

You: "What's my battery level?"
Vani: "Battery: 75% (on battery)"

You: "Volume up"
Vani: "Volume increased"
```

### Web Search & Knowledge

```
You: "Latest news about India"
Vani: *Searches web* "According to recent reports..."

You: "What is Python?"
Vani: *Searches Wikipedia* "Python is a programming language..."
```

### Combined Vision + Conversation

```
You: "What do you see?"
Vani: "I can see: A laptop showing code on the screen"

You: "What programming language is that?"
Vani: *Uses vision context* "Based on what I see, it appears to be Python code"

You: "What color is the laptop?"
Vani: *Remembers previous image* "The laptop appears to be silver/gray"
```

### Voice Commands Reference

| Category | Commands | Languages | Model |
|----------|----------|-----------|-------|
| **Vision** | "what do you see/time/read/count" | All | Moondream 🆕 |
| **Web Search** | "latest news/weather/search" | All | DuckDuckGo |
| **Knowledge** | "what is/who is/explain" | All | Wikipedia + Llama |
| **Apps** | "open/launch/start [app]" | All | Desktop |
| **Websites** | "open [site] in [browser]" | All | Desktop |
| **System** | "screenshot/battery/volume" | All | Desktop |

---

## ⚙️ Configuration

### Customize Vani

Edit `src/config.py`:

```
# Assistant Identity
ASSISTANT_NAME = "Vani"
ASSISTANT_NAME_HI = "वाणी"
ASSISTANT_NAME_GU = "વાણી"

# AI Models
OLLAMA_MODEL = "llama3.2:3b"      # Text/conversation
VISION_MODEL = "moondream"         # Vision 🆕

# Speech Recognition
WHISPER_MODEL = "medium"           # tiny/base/small/medium/large

# Features
ENABLE_WEB_SEARCH = True
ENABLE_DESKTOP_CONTROL = True
ENABLE_VISION = True               # 🆕

# Camera
CAMERA_INDEX = 0                   # 0 for default camera 🆕

# Audio
SILENCE_THRESHOLD = 3000
RECORD_SECONDS = 10
```

### Model Options

| Model | Type | Size | Purpose | Best For |
|-------|------|------|---------|----------|
| **llama3.2:3b** ⭐ | Text | 2GB | Conversation | Multilingual chat |
| llama3.3:1b | Text | 1GB | Conversation | Low-resource systems |
| deepseek-r1:1.5b | Text | 1GB | Reasoning | Complex questions |
| **moondream** ⭐ | Vision | 1.7GB | Image analysis | Vision tasks 🆕 |

---

## 🔧 Troubleshooting

### Vision Issues 🆕

#### ❌ Camera Not Detected

```
# Check camera devices
ls /dev/video*

# Test camera
ffplay /dev/video0

# Install camera tools
sudo apt-get install v4l-utils
v4l2-ctl --list-devices
```

#### ❌ Moondream Not Found

```
# Pull Moondream model
ollama pull moondream

# Verify it's available
ollama list | grep moondream
```

#### ❌ Vision Commands Not Working

**Problem:** Camera doesn't activate when asking vision questions

**Solution:**
- Make sure `ENABLE_VISION = True` in config.py
- Use trigger phrases: "what do you see", "look at this", "how many"
- Check camera permissions: `sudo usermod -a -G video $USER`

### Performance Optimization

#### For 8GB RAM Systems

```
# In config.py
WHISPER_MODEL = "small"
OLLAMA_MODEL = "llama3.3:1b"
VISION_MODEL = "moondream"  # Already optimized
```

#### For 16GB+ RAM Systems

```
# In config.py
WHISPER_MODEL = "large"
OLLAMA_MODEL = "llama3.2:3b"
VISION_MODEL = "moondream"
```

---

## 📊 System Requirements

### Minimum Requirements
- **CPU:** Intel Core i5 (8th gen) or AMD Ryzen 5
- **RAM:** 8GB
- **Storage:** 7GB free space
- **Camera:** Any USB or integrated webcam 🆕
- **Internet:** For TTS and web search

### Recommended Requirements
- **CPU:** Intel Core i7 or AMD Ryzen 7
- **RAM:** 16GB
- **Storage:** 10GB free space
- **Camera:** 720p or better webcam 🆕
- **GPU:** Optional (CUDA for faster processing)

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

# Vision 🆕
opencv-python>=4.8.0
```

## 🙏 Acknowledgments

- **OpenAI Whisper** - Speech recognition
- **Ollama** - Local LLM inference
- **Meta Llama** - Language models
- **Moondream** - Vision model 🆕
- **Google TTS** - Text-to-speech
- **faster-whisper** - Optimized Whisper
- **DuckDuckGo** - Web search
- **Wikipedia** - Knowledge base
- **OpenCV** - Computer vision 🆕

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

<div align="center">

**Made with ❤️ for the open-source community**

*Empowering multilingual voice interactions with vision, local AI, web search, and desktop automation*

[⬆ Back to Top](#-vani---multilingual-ai-voice-assistant-with-vision)

</div>
