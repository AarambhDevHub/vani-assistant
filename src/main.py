"""Main application entry point (Async)."""

import sys
import signal
import asyncio
from .audio_utils import AudioRecorder
from .stt_handler import SpeechRecognizer
from .llm_handler import OllamaHandler
from .tts_google import TextToSpeechGoogle as TextToSpeech
from . import config
from .logger import logger

class VoiceAssistant:
    """Main voice assistant application (Async)."""
    
    def __init__(self):
        self.running = True
        self.assistant_name = config.ASSISTANT_NAME
        
        logger.info(f"🚀 Initializing {self.assistant_name} - Your AI Voice Assistant...")
        logger.info("=" * 50)
        
        try:
            self.audio_recorder = AudioRecorder()
            self.speech_recognizer = SpeechRecognizer()
            self.llm_handler = OllamaHandler()
            self.tts = TextToSpeech()
            
            logger.info("=" * 50)
            logger.info(f"✅ {self.assistant_name} is ready to help!")
            
        except Exception as e:
            logger.critical(f"❌ Initialization failed: {e}")
            sys.exit(1)
            
    async def initialize(self):
        """Async initialization of components."""
        await self.llm_handler.initialize()
    
    async def run(self):
        """Run the main assistant loop."""
        print("🎯 Commands:")
        print(f"  - Speak to {self.assistant_name} in English, Hindi, or Gujarati")
        print("  - Say 'exit', 'quit', or 'goodbye' to stop")
        print("  - Say 'reset' to clear conversation history")
        print(f"  - Say 'who are you' to learn about {self.assistant_name}")
        print("  - Press Ctrl+C to force quit")
        print()
        
        await self.initialize()
        
        while self.running:
            try:
                # Play beep
                self.audio_recorder.play_beep()
                
                # Record audio (Async)
                audio = await self.audio_recorder.record_audio()
                
                if audio is None:
                    continue
                
                # Transcribe (Async)
                result = await self.speech_recognizer.transcribe(audio)
                
                if result is None:
                    continue
                
                text, detected_language = result
                
                # Check for identity questions
                if self._is_identity_question(text):
                    await self._introduce(detected_language)
                    continue
                
                # Check for exit commands
                if self._is_exit_command(text):
                    goodbye_msg = {
                        'en': f'Goodbye! {self.assistant_name} signing off.',
                        'hi': f'अलविदा! {config.ASSISTANT_NAME_HI} विदा ले रही है।',
                        'gu': f'આવજો! {config.ASSISTANT_NAME_GU} જતી રહી છે.'
                    }.get(detected_language, 'Goodbye!')
                    
                    await self.tts.speak(goodbye_msg, detected_language)
                    logger.info("👋 Exiting...")
                    self.running = False
                    break
                
                # Check for reset command
                if self._is_reset_command(text):
                    self.llm_handler.reset_conversation()
                    reset_msg = {
                        'en': 'Conversation history cleared',
                        'hi': 'बातचीत का इतिहास साफ़ हो गया',
                        'gu': 'વાતચીત ઇતિહાસ સાફ થયો'
                    }.get(detected_language, 'Conversation history cleared')
                    
                    await self.tts.speak(reset_msg, detected_language)
                    continue
                
                # Generate response (Async)
                response = await self.llm_handler.generate_response(text, detected_language)
                
                if response:
                    await self.tts.speak(response, detected_language)
                else:
                    error_msg = {
                        'en': "I'm sorry, I couldn't process that",
                        'hi': 'क्षमा करें, मैं इसे संसाधित नहीं कर सका',
                        'gu': 'માફ કરશો, હું તેને પ્રક્રિયા કરી શક્યો નહીં'
                    }.get(detected_language, "I'm sorry, I couldn't process that")
                    
                    await self.tts.speak(error_msg, detected_language)
                
                print()
                
            except asyncio.CancelledError:
                logger.info("\n👋 Interrupted by user")
                break
            except Exception as e:
                logger.error(f"❌ Error: {e}")
                continue
        
        logger.info(f"✅ {self.assistant_name} stopped")
    
    def _is_identity_question(self, text: str) -> bool:
        identity_phrases = [
            'who are you', 'what is your name', 'your name',
            'तुम कौन हो', 'तुम्हारा नाम क्या है',
            'તમે કોણ છો', 'તમારું નામ શું છે'
        ]
        text_lower = text.lower()
        return any(phrase in text_lower for phrase in identity_phrases)
    
    async def _introduce(self, language: str):
        introductions = {
            'en': f"I am {config.ASSISTANT_NAME}, your multilingual AI voice assistant. I can help you in English, Hindi, and Gujarati!",
            'hi': f"मैं {config.ASSISTANT_NAME_HI} हूं, आपकी बहुभाषी AI आवाज सहायक। मैं अंग्रेजी, हिंदी और गुजराती में आपकी मदद कर सकती हूं!",
            'gu': f"હું {config.ASSISTANT_NAME_GU} છું, તમારી બહુભાષી AI વૉઇસ આસિસ્ટન્ટ. હું અંગ્રેજી, હિન્દી અને ગુજરાતીમાં તમારી મદદ કરી શકું છું!"
        }
        intro = introductions.get(language, introductions['en'])
        await self.tts.speak(intro, language)
    
    def _is_exit_command(self, text: str) -> bool:
        exit_words = [
            'exit', 'quit', 'goodbye', 'bye', 'stop',
            'बाहर निकलें', 'बंद करो', 'अलविदा', 'बाय',
            'બહાર નીકળો', 'બંધ કરો', 'અલવિદા', 'બાય'
        ]
        text_lower = text.lower()
        return any(word in text_lower for word in exit_words)
    
    def _is_reset_command(self, text: str) -> bool:
        reset_words = [
            'reset', 'clear history', 'start over',
            'रीसेट', 'इतिहास साफ़ करें',
            'રીસેટ', 'ઇતિહાસ સાફ કરો'
        ]
        text_lower = text.lower()
        return any(word in text_lower for word in reset_words)

def main():
    """Entry point."""
    assistant = VoiceAssistant()
    
    try:
        asyncio.run(assistant.run())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
