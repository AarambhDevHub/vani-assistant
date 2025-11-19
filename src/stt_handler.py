"""Speech recognition using faster-whisper - Optimized multilingual STT (Async)."""

from faster_whisper import WhisperModel
import speech_recognition as sr
from typing import Optional, Tuple
import asyncio
import tempfile
import os
from . import config
from .logger import logger

class SpeechRecognizer:
    """Converts speech to text using faster-whisper (optimized)."""
    
    def __init__(self):
        logger.info(f"Loading faster-whisper model '{config.WHISPER_MODEL}'...")
        
        # Initialize faster-whisper with optimal settings for CPU
        self.model = WhisperModel(
            config.WHISPER_MODEL,
            device="cpu",
            compute_type="int8",
            cpu_threads=4,
            num_workers=1
        )
        
        logger.info("✅ faster-whisper model loaded (4x faster than standard Whisper)")
        logger.info("   Supported: English, Hindi (हिन्दी), Gujarati (ગુજરાતી) + 90+ languages")
    
    async def transcribe(self, audio: sr.AudioData) -> Optional[Tuple[str, str]]:
        """Transcribe audio to text (Async wrapper)."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._transcribe_sync, audio)

    def _transcribe_sync(self, audio: sr.AudioData) -> Optional[Tuple[str, str]]:
        """Synchronous transcription logic."""
        try:
            wav_data = audio.get_wav_data()
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
                temp_audio.write(wav_data)
                temp_path = temp_audio.name
            
            try:
                segments, info = self.model.transcribe(
                    temp_path,
                    language=None,
                    beam_size=5,
                    vad_filter=True,
                    vad_parameters=dict(
                        min_silence_duration_ms=500,
                        speech_pad_ms=400
                    ),
                    temperature=0.0,
                    compression_ratio_threshold=2.4,
                    log_prob_threshold=-1.0,
                    no_speech_threshold=0.6
                )
                
                text = " ".join([segment.text for segment in segments]).strip()
                detected_lang = info.language
                
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
                    logger.info(f"📝 You said [{lang_display}]: {text}")
                    logger.debug(f"   Detection confidence: {info.language_probability:.2%}")
                    return (text, detected_lang)
                else:
                    logger.warning("⚠️ No speech detected in audio")
                    return None
                    
            finally:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            logger.error(f"❌ Transcription error: {e}")
            return None
