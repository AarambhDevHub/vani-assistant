"""Configuration settings for the voice assistant."""

import os

# Assistant Identity
ASSISTANT_NAME = "Vani"
ASSISTANT_NAME_HI = "वाणी"
ASSISTANT_NAME_GU = "વાણી"

# Ollama settings
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2:3b"
OLLAMA_API_ENDPOINT = f"{OLLAMA_BASE_URL}/api/generate"

# faster-whisper settings
WHISPER_MODEL = "medium"

# Audio settings
SAMPLE_RATE = 16000
CHANNELS = 1
RECORD_SECONDS = 10
SILENCE_THRESHOLD = 3000
SILENCE_DURATION = 1.2

# TTS settings
TTS_RATE = 160
TTS_VOLUME = 0.9

# Web Search settings
ENABLE_WEB_SEARCH = True  # Set to False to disable web search
WEB_SEARCH_MAX_RESULTS = 3

# System prompt with web search capability
SYSTEM_PROMPT = f"""You are {ASSISTANT_NAME}, a helpful AI voice assistant with web search capability.
You can understand and respond in English, Hindi, and Gujarati. Provide concise, clear, and friendly 
responses in the same language as the user's question. Keep answers brief since they will be spoken aloud.

When provided with web search results, use them to give accurate, current information.
Important: Respond ONLY in the language the user speaks. Do not mix languages."""
