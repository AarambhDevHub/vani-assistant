"""Audio recording utilities."""

import speech_recognition as sr
import numpy as np
import sounddevice as sd
from typing import Optional
from . import config


class AudioRecorder:
    """Handles audio recording from microphone."""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Better settings for clearer audio
        self.recognizer.energy_threshold = 4000  # Higher = require louder speech
        self.recognizer.dynamic_energy_threshold = True  # Auto-adjust
        self.recognizer.pause_threshold = 1.0  # Shorter pause = faster response
        self.recognizer.phrase_threshold = 0.3  # Minimum phrase length
        self.recognizer.non_speaking_duration = 0.5  # How long silence before stopping
        
    def record_audio(self) -> Optional[sr.AudioData]:
        """
        Record audio from microphone until silence is detected.
        
        Returns:
            AudioData object or None if recording failed
        """
        try:
            with sr.Microphone(sample_rate=16000) as source:
                print("🎤 Listening... (speak clearly and close to mic)")
                
                # Adjust for ambient noise (important!)
                print("   Calibrating for background noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Record audio
                audio = self.recognizer.listen(
                    source,
                    timeout=10,
                    phrase_time_limit=10  # Maximum 10 seconds
                )
                
                print("✅ Recording complete")
                return audio
                
        except sr.WaitTimeoutError:
            print("⚠️ No speech detected - try speaking louder")
            return None
        except Exception as e:
            print(f"❌ Recording error: {e}")
            return None
    
    def play_beep(self, frequency: int = 800, duration: float = 0.1):
        """Play a beep sound to indicate recording start/stop."""
        try:
            sample_rate = 44100
            t = np.linspace(0, duration, int(sample_rate * duration))
            wave = 0.3 * np.sin(2 * np.pi * frequency * t)
            sd.play(wave, sample_rate)
            sd.wait()
        except Exception as e:
            pass  # Ignore beep errors


class AudioPlayer:
    """Handles audio playback."""
    
    @staticmethod
    def play_audio(audio_data: np.ndarray, sample_rate: int):
        """
        Play audio data.
        
        Args:
            audio_data: Audio samples as numpy array
            sample_rate: Sample rate in Hz
        """
        try:
            sd.play(audio_data, sample_rate)
            sd.wait()
        except Exception as e:
            print(f"❌ Playback error: {e}")
