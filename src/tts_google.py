"""Text-to-speech using Google TTS with multilingual support (Async)."""

from gtts import gTTS
import pygame
import tempfile
import os
import time
import asyncio
from typing import Optional
from .logger import logger

class TextToSpeechGoogle:
    """Converts text to speech using Google TTS with language detection (Async)."""
    
    def __init__(self, default_lang: str = 'en', default_tld: str = 'com', slow: bool = False):
        self.default_lang = default_lang
        self.default_tld = default_tld
        self.slow = slow
        
        self.lang_tld_map = {
            'en': 'com',
            'hi': 'co.in',
            'gu': 'co.in',
            'mr': 'co.in',
            'pa': 'co.in',
            'bn': 'co.in',
            'ta': 'co.in',
            'te': 'co.in',
            'kn': 'co.in',
            'ml': 'co.in',
            'es': 'es',
            'fr': 'fr',
            'de': 'de',
            'ja': 'co.jp',
            'zh': 'com',
        }
        
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            logger.info(f"✅ Google TTS initialized")
        except Exception as e:
            logger.error(f"❌ pygame initialization error: {e}")
            raise
    
    async def speak(self, text: str, language: str = None):
        """Speak the given text (Async wrapper)."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._speak_sync, text, language)

    def _speak_sync(self, text: str, language: str = None):
        """Synchronous speech logic."""
        if not text or not text.strip():
            return
        
        lang = language or self.default_lang
        tld = self.lang_tld_map.get(lang, 'com')
        
        try:
            lang_display = {
                'en': 'English',
                'hi': 'Hindi (हिन्दी)',
                'gu': 'Gujarati (ગુજરાતી)',
            }.get(lang, lang.upper())
            
            logger.info(f"🔊 Speaking [{lang_display}]: {text}")
            
            temp_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
            temp_path = temp_file.name
            temp_file.close()
            
            try:
                tts = gTTS(text=text, lang=lang, tld=tld, slow=self.slow)
                tts.save(temp_path)
                
                pygame.mixer.music.load(temp_path)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                time.sleep(0.1)
                    
            except Exception as e:
                logger.error(f"❌ TTS error: {e}")
                
            finally:
                try:
                    pygame.mixer.music.unload()
                except: pass
                
                time.sleep(0.2)
                
                try:
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                except: pass
                    
        except Exception as e:
            logger.error(f"❌ TTS error: {e}")
    
    def stop(self):
        """Stop current speech."""
        try:
            pygame.mixer.music.stop()
        except: pass
    
    def change_accent(self, tld: str):
        self.default_tld = tld
        logger.info(f"✅ Default accent changed to: {tld}")
    
    def set_default_language(self, lang: str):
        self.default_lang = lang
        logger.info(f"✅ Default language changed to: {lang}")
    
    def __del__(self):
        try:
            pygame.mixer.quit()
        except: pass
