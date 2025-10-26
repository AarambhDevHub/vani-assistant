"""Multi-model handler for vision + conversation with smart detection."""

from typing import Optional
from .vision_handler import VisionHandler
from . import config
import requests


class MultiModelHandler:
    """Handle conversations using both vision (Moondream) and text (Llama) models."""
    
    def __init__(self):
        self.vision = VisionHandler()
        self.text_model = config.OLLAMA_MODEL
        self.ollama_url = config.OLLAMA_BASE_URL
        self.conversation_history = []
        self.vision_context = None
        self.last_vision_time = 0
        
        print("✅ Multi-model system ready (Moondream + Llama)")
    
    def _needs_vision(self, command: str) -> bool:
        """
        Intelligently detect if query needs vision/camera.
        Enhanced with better Hindi/Gujarati pattern matching.
        """
        cmd = command.lower()
        
        # Explicit vision triggers - EXPANDED
        explicit_triggers = [
            # English
            'what do you see', 'what can you see', 'look at', 'describe what you see',
            'tell me what you see', 'camera', 'take a look', 'show me',
            
            # Hindi - multiple variations
            'क्या दिख रहा है', 'क्या देख रहा है', 'क्या दीख रहा है',  # What do you see
            'देखो', 'दिखाओ', 'देख', 'क्या है',  # Look, show, see, what is
            'यह क्या है', 'ये क्या है',  # What is this
            'कैमरा', 'कैमरे से देखो',  # Camera
            
            # Gujarati - multiple variations  
            'તમે શું જુઓ છો', 'શું દેખાય છે', 'શું જોવા મળે છે',  # What do you see
            'જુઓ', 'દેખાવો', 'શું છે',  # Look, show, what is
            'આ શું છે', 'એ શું છે',  # What is this
            'કેમેરા', 'કેમેરાથી જુઓ'  # Camera
        ]
        
        # Check explicit triggers
        for trigger in explicit_triggers:
            if trigger in cmd:
                print(f"✅ Vision trigger matched: '{trigger}'")
                return True
        
        # Questions about visible things
        vision_question_patterns = [
            # People
            'how many people', 'how many person', 'who is', 'who are',
            'is there a person', 'are there people', 'anyone here',
            'कितने लोग', 'कितने व्यक्ति', 'कौन है', 'कोई व्यक्ति',
            'કેટલા લોકો', 'કોણ છે', 'કોઈ વ્યક્તિ',
            
            # Objects
            'what object', 'what is on', 'what is in front',
            'how many object', 'count the', 'objects in',
            'क्या वस्तु', 'कितनी वस्तु', 'कितने चीज',
            'શું વસ્તુ', 'કેટલી વસ્તુ',
            
            # Colors
            'what color', 'what colour', 'color of',
            'क्या रंग', 'रंग कैसा', 'કયો રંગ', 'રંગ શું',
            
            # Location
            'where is', 'where am i', 'what room', 'what place',
            'कहाँ है', 'कहाँ हूँ', 'कौन सा कमरा', 'ક્યાં છે', 'ક્યાં છું',
            
            # Descriptions
            'describe the', 'describe this', 'what is this',
            'tell me about this', 'read this', 'what does it say',
            'बताओ यह', 'यह क्या', 'વર્ણન કરો', 'આ શું',
            
            # Reading
            'read the text', 'what does it say', 'read what',
            'पढ़ो', 'क्या लिखा है', 'વાંચો', 'શું લખ્યું છે'
        ]
        
        # Check patterns
        for pattern in vision_question_patterns:
            if pattern in cmd:
                print(f"✅ Vision pattern matched: '{pattern}'")
                return True
        
        # Check for visual context questions
        visual_nouns = [
            'person', 'people', 'face', 'man', 'woman',
            'object', 'thing', 'item',
            'room', 'wall', 'door', 'window',
            'व्यक्ति', 'लोग', 'वस्तु', 'कमरा', 'दीवार',
            'લોકો', 'વસ્તુ', 'રૂમ', 'દિવાલ'
        ]
        
        question_words = [
            'what', 'how many', 'which', 'where', 'is there',
            'क्या', 'कितने', 'कहाँ', 'કયું', 'કેટલા', 'ક્યાં'
        ]
        
        has_question = any(q in cmd for q in question_words)
        has_visual_noun = any(noun in cmd for noun in visual_nouns)
        
        if has_question and has_visual_noun:
            print(f"✅ Visual question detected: question + visual noun")
            return True
        
        # Fallback: if contains vision-related verbs
        vision_verbs = [
            'see', 'look', 'watch', 'view', 'show',
            'देख', 'दिख', 'दीख', 'दिखा', 'देखो',
            'જુઓ', 'જોવું', 'દેખાવો'
        ]
        
        if any(verb in cmd for verb in vision_verbs):
            # Also check if it's a question or command
            if '?' in cmd or any(w in cmd for w in ['what', 'क्या', 'કયું', 'કેમ']):
                print(f"✅ Vision verb + question detected")
                return True
        
        return False

    
    def process_vision_command(self, command: str, language: str = 'en') -> Optional[str]:
        """Process commands that need vision with smart question generation."""
        
        if not self._needs_vision(command):
            return None
        
        print("📸 Vision required - activating camera")
        
        # Generate smart question for Moondream
        question = self._generate_vision_question(command)
        print(f"👁️  Asking Moondream: '{question}'")
        
        # Get vision analysis
        description = self.vision.see_and_describe(question)
        
        if description:
            import time
            self.vision_context = description
            self.last_vision_time = time.time()
            
            # Translate if needed
            if language != 'en':
                translated_description = self._translate_vision_response(description, language)
            else:
                translated_description = description
            
            # Format response
            if language == 'hi':
                response = f"मैं देख रहा हूं: {translated_description}"
            elif language == 'gu':
                response = f"હું જોઈ રહ્યો છું: {translated_description}"
            else:
                response = f"I can see: {translated_description}"
            
            return response
        else:
            if language == 'hi':
                return "मैं कैमरा एक्सेस नहीं कर पा रहा हूं"
            elif language == 'gu':
                return "હું કેમેરાને ઍક્સેસ કરી શકતો નથી"
            else:
                return "I cannot access the camera right now"

    def _translate_vision_response(self, english_text: str, target_language: str) -> str:
        """
        Translate vision response from English to target language using Llama.
        
        Args:
            english_text: English description from Moondream
            target_language: Target language code ('hi', 'gu')
            
        Returns:
            Translated text
        """
        try:
            if target_language == 'hi':
                prompt = f"""Translate the following English text to Hindi. Only provide the Hindi translation, nothing else.

    English: {english_text}

    Hindi:"""
            elif target_language == 'gu':
                prompt = f"""Translate the following English text to Gujarati. Only provide the Gujarati translation, nothing else.

    English: {english_text}

    Gujarati:"""
            else:
                return english_text
            
            # Use Llama to translate
            payload = {
                "model": self.text_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,  # Lower for more accurate translation
                    "num_predict": 300
                }
            }
            
            print(f"🌐 Translating to {target_language}...")
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            translation = result.get("response", "").strip()
            
            if translation:
                print(f"✅ Translated: {translation[:100]}...")
                return translation
            else:
                # Fallback to English if translation fails
                return english_text
                
        except Exception as e:
            print(f"⚠️ Translation failed: {e}, using English")
            return english_text

    
    def _generate_vision_question(self, command: str) -> str:
        """
        Generate appropriate question for Moondream based on user query.
        Now passes user's actual question when possible.
        """
        cmd = command.lower()
        
        # Time/Clock related
        if any(word in cmd for word in ['time', 'clock', 'watch', 'समय', 'घड़ी', 'સમય', 'ઘડિયાળ']):
            return "What time is shown on any clock, watch, or time display visible in this image? Read the exact time."
        
        # People counting
        if 'how many people' in cmd or 'how many person' in cmd or 'कितने लोग' in cmd or 'કેટલા લોકો' in cmd:
            return "How many people are in this image? Count them carefully."
        
        # Person identification
        if 'who is' in cmd or 'who are' in cmd or 'कौन है' in cmd or 'કોણ છે' in cmd:
            return "Describe the people in this image. Who do you see?"
        
        # Object counting
        if 'how many object' in cmd or 'count' in cmd or 'कितने' in cmd or 'કેટલા' in cmd:
            return "Count and list all the objects you can see in this image."
        
        # Color questions
        if 'what color' in cmd or 'what colour' in cmd or 'रंग' in cmd or 'રંગ' in cmd:
            return "What colors do you see in this image? Describe them in detail."
        
        # Location questions
        if 'where am i' in cmd or 'what room' in cmd or 'what place' in cmd or 'कहाँ' in cmd or 'ક્યાં' in cmd:
            return "Describe this location. What kind of room or place is this? What can you see?"
        
        # Reading text - ANY text in image
        if any(word in cmd for word in ['read', 'text', 'written', 'पढ़', 'लिखा', 'વાંચ', 'લખ્યું']):
            return "Read all the text visible in this image. What does it say?"
        
        # Object identification
        if 'what is this' in cmd or 'what is on' in cmd or 'what is in' in cmd:
            return "Describe the main object or item in this image in detail."
        
        # Weather/Temperature
        if 'weather' in cmd or 'temperature' in cmd or 'मौसम' in cmd or 'હવામાન' in cmd:
            return "If there's a weather display or temperature reading visible, what does it show?"
        
        # Price/Money
        if 'price' in cmd or 'cost' in cmd or 'how much' in cmd or 'कीमत' in cmd or 'કિંમત' in cmd:
            return "If there are any prices or monetary values visible, what are they?"
        
        # Screen/Display content
        if any(word in cmd for word in ['screen', 'monitor', 'display', 'phone', 'स्क्रीन', 'સ્ક્રીન']):
            return "What is displayed on the screen or monitor in this image? Describe what you see."
        
        # Signs/Labels
        if 'sign' in cmd or 'label' in cmd or 'साइन' in cmd or 'લેબલ' in cmd:
            return "What signs, labels, or text are visible in this image? Read them."
        
        # General "what do you see" - be comprehensive
        if any(phrase in cmd for phrase in ['what do you see', 'what can you see', 'describe', 
                                            'दिख रहा', 'देख रहा', 'જુઓ છો']):
            return "Describe everything visible in this image in detail - including people, objects, text, numbers, colors, and any information displayed."
        
        # If none of the above, try to extract the actual question
        # This allows flexible questions like "What's written on the paper?" or "How many chairs?"
        
        # Clean up the command for Moondream
        question = command.strip()
        
        # If it starts with question words, use it directly
        question_words = ['what', 'how', 'where', 'when', 'why', 'who', 'which',
                        'क्या', 'कैसे', 'कहाँ', 'कब', 'क्यों', 'कौन',
                        'શું', 'કેમ', 'ક્યાં', 'ક્યારે', 'કેમ', 'કોણ']
        
        if any(question.lower().startswith(qw) for qw in question_words):
            # Pass the user's question directly to Moondream
            return f"Answer this question about the image: {question}"
        
        # Default: comprehensive description
        return "Describe everything you see in this image in detail, including any text, numbers, people, objects, colors, and the setting. Be specific and thorough."

    
    def generate_with_vision_context(self, user_input: str, language: str = 'en') -> Optional[str]:
        """Generate response using vision context if available."""
        try:
            # Build prompt with vision context
            prompt_parts = []
            
            # System instruction
            if language == 'hi':
                prompt_parts.append("तुम एक सहायक AI हो जो दृश्य जानकारी को समझ सकता है।\n\n")
            elif language == 'gu':
                prompt_parts.append("તમે એક સહાયક AI છો જે દ્રશ્ય માહિતી સમજી શકે છે.\n\n")
            else:
                prompt_parts.append("You are a helpful AI assistant with access to visual information.\n\n")
            
            # Add vision context if available
            if self.vision_context:
                import time
                # Only use vision context if it's recent (within 60 seconds)
                if time.time() - self.last_vision_time < 60:
                    if language == 'hi':
                        prompt_parts.append(f"दृश्य जानकारी (कैमरा): {self.vision_context}\n\n")
                    elif language == 'gu':
                        prompt_parts.append(f"દ્રશ્ય માહિતી (કેમેરા): {self.vision_context}\n\n")
                    else:
                        prompt_parts.append(f"Visual information (from camera): {self.vision_context}\n\n")
            
            # Add conversation history
            for msg in self.conversation_history[-4:]:
                if msg['role'] == 'user':
                    prompt_parts.append(f"User: {msg['content']}\n")
                else:
                    prompt_parts.append(f"Assistant: {msg['content']}\n")
            
            # Add current question
            prompt_parts.append(f"User: {user_input}\n")
            prompt_parts.append("Assistant: ")
            
            prompt = "".join(prompt_parts)
            
            # Generate response
            payload = {
                "model": self.text_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 200
                }
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            assistant_response = result.get("response", "").strip()
            
            if assistant_response:
                # Update conversation history
                self.conversation_history.append({
                    'role': 'user',
                    'content': user_input,
                    'language': language
                })
                self.conversation_history.append({
                    'role': 'assistant',
                    'content': assistant_response,
                    'language': language
                })
                
                # Keep last 10 messages
                if len(self.conversation_history) > 10:
                    self.conversation_history = self.conversation_history[-10:]
                
                return assistant_response
            
            return None
            
        except Exception as e:
            print(f"❌ Response generation failed: {e}")
            return None
    
    def clear_vision_context(self):
        """Clear vision context."""
        self.vision_context = None
        self.last_vision_time = 0
        print("🔄 Vision context cleared")
