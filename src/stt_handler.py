"""Speech recognition using faster-whisper - Optimized multilingual STT."""

from faster_whisper import WhisperModel
import speech_recognition as sr
from typing import Optional, Tuple
from . import config
import tempfile
import os


class SpeechRecognizer:
    """Converts speech to text using faster-whisper (optimized)."""
    
    def __init__(self):
        print(f"Loading faster-whisper model '{config.WHISPER_MODEL}'...")
        
        # Initialize faster-whisper with optimal settings for CPU
        self.model = WhisperModel(
            config.WHISPER_MODEL,
            device="cpu",              # Use "cuda" if you have NVIDIA GPU
            compute_type="int8",       # Use int8 for faster CPU inference
            cpu_threads=4,             # Adjust based on your CPU cores
            num_workers=1
        )
        
        print("✅ faster-whisper model loaded (4x faster than standard Whisper)")
        print("   Supported: English, Hindi (हिन्दी), Gujarati (ગુજરાતી) + 90+ languages")
    
    def transcribe(self, audio: sr.AudioData) -> Optional[Tuple[str, str]]:
        """
        Transcribe audio to text with auto language detection.
        
        Args:
            audio: AudioData from speech_recognition
            
        Returns:
            Tuple of (text, language_code) or None if transcription failed
        """
        try:
            # Convert audio to WAV format
            wav_data = audio.get_wav_data()
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False
            ) as temp_audio:
                temp_audio.write(wav_data)
                temp_path = temp_audio.name
            
            try:
                # Transcribe with faster-whisper (auto language detection)
                segments, info = self.model.transcribe(
                    temp_path,
                    language=None,              # Auto-detect
                    beam_size=5,                # Higher = more accurate, slower
                    vad_filter=True,            # Voice Activity Detection - removes silence
                    vad_parameters=dict(
                        min_silence_duration_ms=500,  # Better silence detection
                        speech_pad_ms=400
                    ),
                    temperature=0.0,            # Deterministic output
                    compression_ratio_threshold=2.4,
                    log_prob_threshold=-1.0,
                    no_speech_threshold=0.6
                )
                
                # Combine all segments into full text
                text = " ".join([segment.text for segment in segments]).strip()
                detected_lang = info.language
                
                # Language name mapping
                lang_names = {
                    "en": "English",
                    "hi": "Hindi (हिन्दी)",
                    "gu": "Gujarati (ગુજરાતી)",
                    "mr": "Marathi (मराठी)",
                    "pa": "Punjabi (ਪੰਜਾਬੀ)",
                    "bn": "Bengali (বাংলা)",
                    "ta": "Tamil (தமிழ்)",
                    "te": "Telugu (తెలుగు)"
                }
                lang_display = lang_names.get(detected_lang, detected_lang)
                
                if text:
                    print(f"📝 You said [{lang_display}]: {text}")
                    print(f"   Detection confidence: {info.language_probability:.2%}")
                    return (text, detected_lang)
                else:
                    print("⚠️ No speech detected in audio")
                    return None
                    
            finally:
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            import traceback
            traceback.print_exc()
            return None
