"""Text-to-speech using Google TTS with multilingual support."""

from gtts import gTTS
import pygame
import tempfile
import os
import time
from typing import Optional


class TextToSpeechGoogle:
    """Converts text to speech using Google TTS with language detection."""
    
    def __init__(self, default_lang: str = 'en', default_tld: str = 'com', slow: bool = False):
        """
        Initialize Google TTS.
        
        Args:
            default_lang: Default language code ('en' for English)
            default_tld: Default accent - 'com' (US), 'co.uk' (UK), 'co.in' (Indian)
            slow: Speak slowly if True
        """
        self.default_lang = default_lang
        self.default_tld = default_tld
        self.slow = slow
        
        # Language to TLD mapping for better accents
        self.lang_tld_map = {
            'en': 'com',      # English - US accent
            'hi': 'co.in',    # Hindi - Indian accent
            'gu': 'co.in',    # Gujarati - Indian accent
            'mr': 'co.in',    # Marathi - Indian accent
            'pa': 'co.in',    # Punjabi - Indian accent
            'bn': 'co.in',    # Bengali - Indian accent
            'ta': 'co.in',    # Tamil - Indian accent
            'te': 'co.in',    # Telugu - Indian accent
            'kn': 'co.in',    # Kannada - Indian accent
            'ml': 'co.in',    # Malayalam - Indian accent
            'es': 'es',       # Spanish
            'fr': 'fr',       # French
            'de': 'de',       # German
            'ja': 'co.jp',    # Japanese
            'zh': 'com',      # Chinese
        }
        
        try:
            # Initialize pygame mixer for audio playback
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            print(f"✅ Google TTS initialized")
            print(f"   Supports: English, Hindi, Gujarati, and 100+ languages")
        except Exception as e:
            print(f"❌ pygame initialization error: {e}")
            raise
    
    def speak(self, text: str, language: str = None):
        """
        Speak the given text in the specified language.
        
        Args:
            text: Text to speak
            language: Language code ('en', 'hi', 'gu', etc.) - auto-detects if None
        """
        if not text or not text.strip():
            return
        
        # Use provided language or default
        lang = language or self.default_lang
        
        # Get appropriate TLD for the language
        tld = self.lang_tld_map.get(lang, 'com')
        
        try:
            # Show what we're speaking
            lang_display = {
                'en': 'English',
                'hi': 'Hindi (हिन्दी)',
                'gu': 'Gujarati (ગુજરાતી)',
                'mr': 'Marathi (मराठी)',
                'pa': 'Punjabi (ਪੰਜਾਬੀ)',
                'bn': 'Bengali (বাংলা)',
                'ta': 'Tamil (தமிழ்)',
                'te': 'Telugu (తెలుగు)',
            }.get(lang, lang.upper())
            
            print(f"🔊 Speaking [{lang_display}]: {text}")
            
            # Create temporary file for audio
            temp_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
            temp_path = temp_file.name
            temp_file.close()
            
            try:
                # Generate speech using Google TTS with language-specific accent
                tts = gTTS(
                    text=text,
                    lang=lang,
                    tld=tld,
                    slow=self.slow
                )
                tts.save(temp_path)
                
                # Load and play the audio
                pygame.mixer.music.load(temp_path)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                # Small delay to ensure playback is complete
                time.sleep(0.1)
                    
            except Exception as e:
                print(f"❌ TTS error: {e}")
                print(f"⚠️ Make sure you have internet connection for gTTS")
                print(f"⚠️ Language '{lang}' may not be supported by gTTS")
                
            finally:
                # Clean up
                try:
                    pygame.mixer.music.unload()
                except:
                    pass
                
                # Wait a bit before deleting file
                time.sleep(0.2)
                
                # Delete temp file
                try:
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                except Exception:
                    pass
                    
        except Exception as e:
            print(f"❌ TTS error: {e}")
    
    def stop(self):
        """Stop current speech."""
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass
    
    def change_accent(self, tld: str):
        """
        Change default voice accent.
        
        Args:
            tld: 'com' (US), 'co.uk' (UK), 'com.au' (Australian), 'co.in' (Indian)
        """
        self.default_tld = tld
        print(f"✅ Default accent changed to: {tld}")
    
    def set_default_language(self, lang: str):
        """
        Set default language.
        
        Args:
            lang: Language code ('en', 'hi', 'gu', etc.)
        """
        self.default_lang = lang
        print(f"✅ Default language changed to: {lang}")
    
    def __del__(self):
        """Clean up pygame mixer."""
        try:
            pygame.mixer.quit()
        except:
            pass
