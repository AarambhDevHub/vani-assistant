"""Multi-model handler for vision + conversation with smart detection (Async)."""

from typing import Optional
from .vision_handler import VisionHandler
from . import config
import aiohttp
import asyncio
import time
from .logger import logger

class MultiModelHandler:
    """Handle conversations using both vision (Moondream) and text (Llama) models (Async)."""
    
    def __init__(self):
        self.vision = VisionHandler()
        self.text_model = config.OLLAMA_MODEL
        self.ollama_url = config.OLLAMA_BASE_URL
        self.conversation_history = []
        self.vision_context = None
        self.last_vision_time = 0
        
        logger.info("✅ Multi-model system ready (Moondream + Llama)")

    async def initialize(self):
        """Initialize vision system."""
        await self.vision.initialize()
    
    def _needs_vision(self, command: str) -> bool:
        """Intelligently detect if query needs vision/camera."""
        cmd = command.lower()
        
        # Explicit vision triggers
        explicit_triggers = [
            'what do you see', 'what can you see', 'look at', 'describe what you see',
            'tell me what you see', 'camera', 'take a look', 'show me',
            'क्या दिख रहा है', 'क्या देख रहा है', 'क्या दीख रहा है',
            'देखो', 'दिखाओ', 'देख', 'क्या है',
            'यह क्या है', 'ये क्या है',
            'कैमरा', 'कैमरे से देखो',
            'તમે શું જુઓ છો', 'શું દેખાય છે', 'શું જોવા મળે છે',
            'જુઓ', 'દેખાવો', 'શું છે',
            'આ શું છે', 'એ શું છે',
            'કેમેરા', 'કેમેરાથી જુઓ'
        ]
        
        for trigger in explicit_triggers:
            if trigger in cmd:
                logger.info(f"✅ Vision trigger matched: '{trigger}'")
                return True
        
        # Questions about visible things
        vision_question_patterns = [
            'how many people', 'how many person', 'who is', 'who are',
            'is there a person', 'are there people', 'anyone here',
            'कितने लोग', 'कितने व्यक्ति', 'कौन है', 'कोई व्यक्ति',
            'કેટલા લોકો', 'કોણ છે', 'કોઈ વ્યક્તિ',
            'what object', 'what is on', 'what is in front',
            'how many object', 'count the', 'objects in',
            'क्या वस्तु', 'कितनी वस्तु', 'कितने चीज',
            'શું વસ્તુ', 'કેટલી વસ્તુ',
            'what color', 'what colour', 'color of',
            'क्या रंग', 'रंग कैसा', 'કયો રંગ', 'રંગ શું',
            'where is', 'where am i', 'what room', 'what place',
            'कहाँ है', 'कहाँ हूँ', 'कौन सा कमरा', 'ક્યાં છે', 'ક્યાં છું',
            'describe the', 'describe this', 'what is this',
            'tell me about this', 'read this', 'what does it say',
            'बताओ यह', 'यह क्या', 'વર્ણન કરો', 'આ શું',
            'read the text', 'what does it say', 'read what',
            'पढ़ो', 'क्या लिखा है', 'વાંચો', 'શું લખ્યું છે'
        ]
        
        for pattern in vision_question_patterns:
            if pattern in cmd:
                logger.info(f"✅ Vision pattern matched: '{pattern}'")
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
            logger.info(f"✅ Visual question detected: question + visual noun")
            return True
        
        # Fallback: if contains vision-related verbs
        vision_verbs = [
            'see', 'look', 'watch', 'view', 'show',
            'देख', 'दिख', 'दीख', 'दिखा', 'देखो',
            'જુઓ', 'જોવું', 'દેખાવો'
        ]
        
        if any(verb in cmd for verb in vision_verbs):
            if '?' in cmd or any(w in cmd for w in ['what', 'क्या', 'કયું', 'કેમ']):
                logger.info(f"✅ Vision verb + question detected")
                return True
        
        return False

    async def process_vision_command(self, command: str, language: str = 'en') -> Optional[str]:
        """Process commands that need vision with smart question generation (Async)."""
        
        if not self._needs_vision(command):
            return None
        
        logger.info("📸 Vision required - activating camera")
        
        question = self._generate_vision_question(command)
        logger.info(f"👁️  Asking Moondream: '{question}'")
        
        # Await the async vision call
        description = await self.vision.see_and_describe(question)
        
        if description:
            self.vision_context = description
            self.last_vision_time = time.time()
            
            if language != 'en':
                translated_description = await self._translate_vision_response(description, language)
            else:
                translated_description = description
            
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

    async def _translate_vision_response(self, english_text: str, target_language: str) -> str:
        """Translate vision response from English to target language using Llama (Async)."""
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
            
            payload = {
                "model": self.text_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 300
                }
            }
            
            logger.info(f"🌐 Translating to {target_language}...")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.ollama_url}/api/generate",
                    json=payload,
                    timeout=30
                ) as response:
                    if response.status != 200:
                        logger.error(f"❌ Translation failed: {response.status}")
                        return english_text
                        
                    result = await response.json()
                    translation = result.get("response", "").strip()
            
            if translation:
                logger.info(f"✅ Translated: {translation[:100]}...")
                return translation
            else:
                return english_text
                
        except Exception as e:
            logger.warning(f"⚠️ Translation failed: {e}, using English")
            return english_text
    
    def _generate_vision_question(self, command: str) -> str:
        """Generate appropriate question for Moondream based on user query."""
        cmd = command.lower()
        
        if any(word in cmd for word in ['time', 'clock', 'watch', 'समय', 'घड़ी', 'સમય', 'ઘડિયાળ']):
            return "What time is shown on any clock, watch, or time display visible in this image? Read the exact time."
        
        if 'how many people' in cmd or 'how many person' in cmd or 'कितने लोग' in cmd or 'કેટલા લોકો' in cmd:
            return "How many people are in this image? Count them carefully."
        
        if 'who is' in cmd or 'who are' in cmd or 'कौन है' in cmd or 'કોણ છે' in cmd:
            return "Describe the people in this image. Who do you see?"
        
        if 'how many object' in cmd or 'count' in cmd or 'कितने' in cmd or 'કેટલા' in cmd:
            return "Count and list all the objects you can see in this image."
        
        if 'what color' in cmd or 'what colour' in cmd or 'रंग' in cmd or 'રંગ' in cmd:
            return "What colors do you see in this image? Describe them in detail."
        
        if 'where am i' in cmd or 'what room' in cmd or 'what place' in cmd or 'कहाँ' in cmd or 'ક્યાં' in cmd:
            return "Describe this location. What kind of room or place is this? What can you see?"
        
        if any(word in cmd for word in ['read', 'text', 'written', 'पढ़', 'लिखा', 'વાંચ', 'લખ્યું']):
            return "Read all the text visible in this image. What does it say?"
        
        if 'what is this' in cmd or 'what is on' in cmd or 'what is in' in cmd:
            return "Describe the main object or item in this image in detail."
        
        if 'weather' in cmd or 'temperature' in cmd or 'मौसम' in cmd or 'હવામાન' in cmd:
            return "If there's a weather display or temperature reading visible, what does it show?"
        
        if 'price' in cmd or 'cost' in cmd or 'how much' in cmd or 'कीमत' in cmd or 'કિંમત' in cmd:
            return "If there are any prices or monetary values visible, what are they?"
        
        if any(word in cmd for word in ['screen', 'monitor', 'display', 'phone', 'स्क्रीन', 'સ્ક્રીન']):
            return "What is displayed on the screen or monitor in this image? Describe what you see."
        
        if 'sign' in cmd or 'label' in cmd or 'साइन' in cmd or 'લેબલ' in cmd:
            return "What signs, labels, or text are visible in this image? Read them."
        
        if any(phrase in cmd for phrase in ['what do you see', 'what can you see', 'describe', 
                                            'दिख रहा', 'देख रहा', 'જુઓ છો']):
            return "Describe everything visible in this image in detail - including people, objects, text, numbers, colors, and any information displayed."
        
        question = command.strip()
        question_words = ['what', 'how', 'where', 'when', 'why', 'who', 'which',
                        'क्या', 'कैसे', 'कहाँ', 'कब', 'क्यों', 'कौन',
                        'શું', 'કેમ', 'ક્યાં', 'ક્યારે', 'કેમ', 'કોણ']
        
        if any(question.lower().startswith(qw) for qw in question_words):
            return f"Answer this question about the image: {question}"
        
        return "Describe everything you see in this image in detail, including any text, numbers, people, objects, colors, and the setting. Be specific and thorough."

    async def generate_with_vision_context(self, user_input: str, language: str = 'en') -> Optional[str]:
        """Generate response using vision context if available (Async)."""
        try:
            prompt_parts = []
            
            if language == 'hi':
                prompt_parts.append("तुम एक सहायक AI हो जो दृश्य जानकारी को समझ सकता है।\n\n")
            elif language == 'gu':
                prompt_parts.append("તમે એક સહાયક AI છો જે દ્રશ્ય માહિતી સમજી શકે છે.\n\n")
            else:
                prompt_parts.append("You are a helpful AI assistant with access to visual information.\n\n")
            
            if self.vision_context:
                if time.time() - self.last_vision_time < 60:
                    if language == 'hi':
                        prompt_parts.append(f"दृश्य जानकारी (कैमरा): {self.vision_context}\n\n")
                    elif language == 'gu':
                        prompt_parts.append(f"દ્રશ્ય માહિતી (કેમેરા): {self.vision_context}\n\n")
                    else:
                        prompt_parts.append(f"Visual information (from camera): {self.vision_context}\n\n")
            
            for msg in self.conversation_history[-4:]:
                if msg['role'] == 'user':
                    prompt_parts.append(f"User: {msg['content']}\n")
                else:
                    prompt_parts.append(f"Assistant: {msg['content']}\n")
            
            prompt_parts.append(f"User: {user_input}\n")
            prompt_parts.append("Assistant: ")
            
            prompt = "".join(prompt_parts)
            
            payload = {
                "model": self.text_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 200
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.ollama_url}/api/generate",
                    json=payload,
                    timeout=60
                ) as response:
                    if response.status != 200:
                        logger.error(f"❌ Response generation failed: {response.status}")
                        return None
                        
                    result = await response.json()
                    assistant_response = result.get("response", "").strip()
            
            if assistant_response:
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
                
                if len(self.conversation_history) > 10:
                    self.conversation_history = self.conversation_history[-10:]
                
                return assistant_response
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Response generation failed: {e}")
            return None
    
    def clear_vision_context(self):
        """Clear vision context."""
        self.vision_context = None
        self.last_vision_time = 0
        logger.info("🔄 Vision context cleared")
