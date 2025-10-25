"""Text-to-speech using pyttsx3."""

import pyttsx3
from typing import Optional
from . import config


class TextToSpeech:
    """Converts text to speech."""
    
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            
            # Get available voices
            voices = self.engine.getProperty('voices')
            
            # Print available voices for debugging
            print("\n📢 Available voices:")
            for idx, voice in enumerate(voices):
                print(f"  {idx}: {voice.name} [{voice.id}]")
            
            # Try to find a better quality voice
            selected_voice = None
            
            # Priority order for voice selection
            voice_preferences = [
                'english-us',  # US English voices
                'english_rp',  # British English
                'english',     # Any English voice
                'female',      # Female voices often sound better
                'male'         # Male voices
            ]
            
            for preference in voice_preferences:
                for voice in voices:
                    if preference in voice.name.lower() or preference in voice.id.lower():
                        selected_voice = voice
                        break
                if selected_voice:
                    break
            
            # If no preferred voice found, use first available
            if not selected_voice and voices:
                selected_voice = voices[0]
            
            if selected_voice:
                self.engine.setProperty('voice', selected_voice.id)
                print(f"✅ Selected voice: {selected_voice.name}")
            
            # Adjust voice properties for more natural sound
            self.engine.setProperty('rate', config.TTS_RATE)      # Speaking speed
            self.engine.setProperty('volume', config.TTS_VOLUME)  # Volume
            
            print("✅ Text-to-speech initialized")
            
        except Exception as e:
            print(f"❌ TTS initialization error: {e}")
            self.engine = None
    
    def speak(self, text: str):
        """
        Speak the given text.
        
        Args:
            text: Text to speak
        """
        if not self.engine:
            print("⚠️ TTS engine not available")
            return
        
        try:
            print(f"🔊 Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
            
        except Exception as e:
            print(f"❌ TTS error: {e}")
    
    def stop(self):
        """Stop current speech."""
        if self.engine:
            try:
                self.engine.stop()
            except Exception:
                pass
    
    def change_voice(self, voice_index: int):
        """Change to a specific voice by index."""
        if not self.engine:
            return
        
        try:
            voices = self.engine.getProperty('voices')
            if 0 <= voice_index < len(voices):
                self.engine.setProperty('voice', voices[voice_index].id)
                print(f"✅ Voice changed to: {voices[voice_index].name}")
            else:
                print(f"⚠️ Voice index {voice_index} out of range (0-{len(voices)-1})")
        except Exception as e:
            print(f"❌ Error changing voice: {e}")
