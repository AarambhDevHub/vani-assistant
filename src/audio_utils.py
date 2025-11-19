"""Audio recording utilities (Async)."""

import speech_recognition as sr
import numpy as np
import sounddevice as sd
import asyncio
from typing import Optional
from . import config
from .logger import logger

class AudioRecorder:
    """Handles audio recording from microphone (Async)."""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 1.0
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5
        
    async def record_audio(self) -> Optional[sr.AudioData]:
        """Record audio from microphone (Async wrapper)."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._record_audio_sync)

    def _record_audio_sync(self) -> Optional[sr.AudioData]:
        """Synchronous recording logic."""
        try:
            with sr.Microphone(sample_rate=16000) as source:
                logger.info("🎤 Listening... (speak clearly and close to mic)")
                
                logger.debug("   Calibrating for background noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                audio = self.recognizer.listen(
                    source,
                    timeout=10,
                    phrase_time_limit=10
                )
                
                logger.info("✅ Recording complete")
                return audio
                
        except sr.WaitTimeoutError:
            logger.warning("⚠️ No speech detected - try speaking louder")
            return None
        except Exception as e:
            logger.error(f"❌ Recording error: {e}")
            return None
    
    def play_beep(self, frequency: int = 800, duration: float = 0.1):
        """Play a beep sound (Sync - fast enough)."""
        try:
            sample_rate = 44100
            t = np.linspace(0, duration, int(sample_rate * duration))
            wave = 0.3 * np.sin(2 * np.pi * frequency * t)
            sd.play(wave, sample_rate)
            sd.wait()
        except Exception:
            pass

class AudioPlayer:
    """Handles audio playback."""
    
    @staticmethod
    def play_audio(audio_data: np.ndarray, sample_rate: int):
        try:
            sd.play(audio_data, sample_rate)
            sd.wait()
        except Exception as e:
            logger.error(f"❌ Playback error: {e}")
