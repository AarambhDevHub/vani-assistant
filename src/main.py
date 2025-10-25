"""Main application entry point."""

import sys
import signal
from .audio_utils import AudioRecorder, AudioPlayer
from .stt_handler import SpeechRecognizer
from .llm_handler import OllamaHandler
from .tts_google import TextToSpeechGoogle as TextToSpeech
from . import config


class VoiceAssistant:
    """Main voice assistant application."""
    
    def __init__(self):
        # Get assistant name based on system language
        assistant_name = config.ASSISTANT_NAME
        
        print(f"🚀 Initializing {assistant_name} - Your AI Voice Assistant...")
        print("=" * 50)
        
        try:
            self.audio_recorder = AudioRecorder()
            self.speech_recognizer = SpeechRecognizer()
            self.llm_handler = OllamaHandler()
            self.tts = TextToSpeech()
            
            print("=" * 50)
            print(f"✅ {assistant_name} is ready to help!")
            print()
            
        except Exception as e:
            print(f"❌ Initialization failed: {e}")
            sys.exit(1)
    
    def run(self):
        """Run the main assistant loop."""
        assistant_name = config.ASSISTANT_NAME
        
        print("🎯 Commands:")
        print(f"  - Speak to {assistant_name} in English, Hindi, or Gujarati")
        print("  - Say 'exit', 'quit', or 'goodbye' to stop")
        print("  - Say 'reset' to clear conversation history")
        print(f"  - Say 'who are you' to learn about {assistant_name}")
        print("  - Press Ctrl+C to force quit")
        print()
        
        # Setup signal handler for graceful exit
        signal.signal(signal.SIGINT, self._signal_handler)
        
        while True:
            try:
                # Play beep to indicate ready to listen
                self.audio_recorder.play_beep()
                
                # Record audio
                audio = self.audio_recorder.record_audio()
                
                if audio is None:
                    continue
                
                # Transcribe speech to text and get language
                result = self.speech_recognizer.transcribe(audio)
                
                if result is None:
                    continue
                
                text, detected_language = result
                
                # Check for identity questions
                if self._is_identity_question(text):
                    self._introduce(detected_language)
                    continue
                
                # Check for exit commands
                if self._is_exit_command(text):
                    goodbye_msg = {
                        'en': f'Goodbye! {assistant_name} signing off.',
                        'hi': f'अलविदा! {config.ASSISTANT_NAME_HI} विदा ले रही है।',
                        'gu': f'આવજો! {config.ASSISTANT_NAME_GU} જતી રહી છે.'
                    }.get(detected_language, 'Goodbye!')
                    
                    self.tts.speak(goodbye_msg, detected_language)
                    print("👋 Exiting...")
                    break
                
                # Check for reset command
                if self._is_reset_command(text):
                    self.llm_handler.reset_conversation()
                    
                    reset_msg = {
                        'en': 'Conversation history cleared',
                        'hi': 'बातचीत का इतिहास साफ़ हो गया',
                        'gu': 'વાતચીત ઇતિહાસ સાફ થયો'
                    }.get(detected_language, 'Conversation history cleared')
                    
                    self.tts.speak(reset_msg, detected_language)
                    continue
                
                # Generate response in the detected language
                response = self.llm_handler.generate_response(text, detected_language)
                
                if response:
                    # Speak the response IN THE SAME LANGUAGE
                    self.tts.speak(response, detected_language)
                else:
                    error_msg = {
                        'en': "I'm sorry, I couldn't process that",
                        'hi': 'क्षमा करें, मैं इसे संसाधित नहीं कर सका',
                        'gu': 'માફ કરશો, હું તેને પ્રક્રિયા કરી શક્યો નહીં'
                    }.get(detected_language, "I'm sorry, I couldn't process that")
                    
                    self.tts.speak(error_msg, detected_language)
                
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Interrupted by user")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        print(f"✅ {assistant_name} stopped")
    
    def _is_identity_question(self, text: str) -> bool:
        """Check if user is asking about the assistant's identity."""
        identity_phrases = [
            'who are you', 'what is your name', 'your name',
            'तुम कौन हो', 'तुम्हारा नाम क्या है',
            'તમે કોણ છો', 'તમારું નામ શું છે'
        ]
        text_lower = text.lower()
        return any(phrase in text_lower for phrase in identity_phrases)
    
    def _introduce(self, language: str):
        """Introduce the assistant."""
        introductions = {
            'en': f"I am {config.ASSISTANT_NAME}, your multilingual AI voice assistant. I can help you in English, Hindi, and Gujarati!",
            'hi': f"मैं {config.ASSISTANT_NAME_HI} हूं, आपकी बहुभाषी AI आवाज सहायक। मैं अंग्रेजी, हिंदी और गुजराती में आपकी मदद कर सकती हूं!",
            'gu': f"હું {config.ASSISTANT_NAME_GU} છું, તમારી બહુભાષી AI વૉઇસ આસિસ્ટન્ટ. હું અંગ્રેજી, હિન્દી અને ગુજરાતીમાં તમારી મદદ કરી શકું છું!"
        }
        
        intro = introductions.get(language, introductions['en'])
        self.tts.speak(intro, language)
    
    def _is_exit_command(self, text: str) -> bool:
        """Check if text is an exit command (multilingual)."""
        exit_words = [
            'exit', 'quit', 'goodbye', 'bye', 'stop',
            'बाहर निकलें', 'बंद करो', 'अलविदा', 'बाय',
            'બહાર નીકળો', 'બંધ કરો', 'અલવિદા', 'બાય'
        ]
        text_lower = text.lower()
        return any(word in text_lower for word in exit_words)
    
    def _is_reset_command(self, text: str) -> bool:
        """Check if text is a reset command."""
        reset_words = [
            'reset', 'clear history', 'start over',
            'रीसेट', 'इतिहास साफ़ करें',
            'રીસેટ', 'ઇતિહાસ સાફ કરો'
        ]
        text_lower = text.lower()
        return any(word in text_lower for word in reset_words)
    
    def _signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully."""
        print(f"\n\n👋 {config.ASSISTANT_NAME} shutting down...")
        self.tts.stop()
        sys.exit(0)


def main():
    """Entry point."""
    assistant = VoiceAssistant()
    assistant.run()


if __name__ == "__main__":
    main()
