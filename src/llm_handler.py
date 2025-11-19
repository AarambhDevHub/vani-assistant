"""Ollama LLM integration with web search support (Async)."""

import aiohttp
import json
import asyncio
from typing import Optional
from . import config
from .web_search import WebSearchHandler
from .desktop_automation import DesktopAutomation
from .multi_model_handler import MultiModelHandler
from .logger import logger

class OllamaHandler:
    """Handles communication with Ollama API with web search capability (Async)."""
    
    def __init__(self):
        self.base_url = config.OLLAMA_BASE_URL
        self.model = config.OLLAMA_MODEL
        self.api_endpoint = config.OLLAMA_API_ENDPOINT
        self.conversation_history = []
        self.current_language = "en"
        
        # Initialize web search
        self.web_search = WebSearchHandler()
        
        # Desktop automation
        self.desktop = DesktopAutomation()

        # Multi-model system (vision + text)
        self.multi_model = MultiModelHandler()
        
    async def initialize(self):
        """Async initialization to check connection."""
        await self._check_connection()
        await self.multi_model.initialize()
    
    async def _check_connection(self):
        """Check if Ollama is running and model is available."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/tags", timeout=5) as response:
                    if response.status != 200:
                        raise Exception(f"Ollama returned status {response.status}")
                    
                    data = await response.json()
                    models = data.get("models", [])
                    model_names = [m["name"] for m in models]
                    
                    if self.model not in model_names:
                        logger.warning(f"⚠️ Warning: Model '{self.model}' not found")
                        logger.info(f"Available models: {', '.join(model_names)}")
                    else:
                        logger.info(f"✅ Connected to Ollama - Using model: {self.model}")
                        
        except Exception as e:
            logger.error(f"❌ Cannot connect to Ollama: {e}")
            logger.info("Make sure Ollama is running: ollama serve")
            # Don't raise, just log error to allow partial functionality
    
    def _needs_web_search(self, query: str) -> bool:
        """Determine if query needs web search for current information."""
        query_lower = query.lower()
        
        # Explicit search keywords
        explicit_search = [
            'search', 'find', 'look up', 'google', 'search for',
            'खोजें', 'ढूंढें', 'सर्च',
            'શોધો', 'શોધ'
        ]
        if any(keyword in query_lower for keyword in explicit_search):
            return True
        
        # News-related queries
        news_keywords = [
            'news', 'latest', 'recent', 'update', 'happening', 'today',
            'समाचार', 'ख़बर', 'ताज़ा', 'आज',
            'સમાચાર', 'તાજા', 'આજે'
        ]
        if any(keyword in query_lower for keyword in news_keywords):
            return True
        
        # Time-sensitive queries
        time_sensitive = [
            'weather', 'temperature', 'forecast',
            'price', 'cost', 'value', 'worth',
            'stock', 'market', 'rate',
            'score', 'match', 'game', 'result',
            'event', 'concert', 'show',
            'मौसम', 'तापमान', 'कीमत', 'स्टॉक',
            'હવામાન', 'કિંમત', 'સ્ટોક'
        ]
        if any(keyword in query_lower for keyword in time_sensitive):
            return True
        
        # Question words that often need current info
        current_info_patterns = [
            'what is happening', 'what happened', 'who won', 'who is',
            'where is', 'when is', 'how much', 'current',
            'क्या हो रहा', 'क्या हुआ', 'कौन है', 'वर्तमान',
            'શું થઈ રહ્યું', 'શું થયું', 'કોણ છે', 'વર્તમાન'
        ]
        if any(pattern in query_lower for pattern in current_info_patterns):
            return True
        
        return False

    def _is_knowledge_query(self, query: str) -> bool:
        """Detect if query is asking for factual knowledge (good for Wikipedia)."""
        knowledge_patterns = [
            'what is', 'who is', 'what are', 'who are',
            'tell me about', 'explain', 'describe',
            'definition of', 'meaning of', 'history of',
            'क्या है', 'कौन है', 'बताओ', 'समझाओ',
            'શું છે', 'કોણ છે', 'જણાવો', 'સમજાવો'
        ]
        query_lower = query.lower()
        return any(pattern in query_lower for pattern in knowledge_patterns)

    async def generate_response(self, user_input: str, language: str = "en") -> Optional[str]:
        """Generate response with intelligent source selection (Async)."""
        try:
            self.current_language = language

            # 1. Check for vision commands
            vision_response = await self.multi_model.process_vision_command(user_input, language)
            if vision_response:
                logger.info(f"👁️  {vision_response}")
                return vision_response

            # 2. Try desktop command (TODO: Make async)
            desktop_response = await self.desktop.execute(user_input, language)
            if desktop_response:
                logger.info(f"🖥️  {desktop_response}")
                return desktop_response
            
            web_context = ""
            if config.ENABLE_WEB_SEARCH:
                is_news = self._needs_web_search(user_input) and any(
                    word in user_input.lower() 
                    for word in ['news', 'latest', 'recent', 'समाचार', 'સમાચાર']
                )
                is_knowledge = self._is_knowledge_query(user_input)
                
                search_results = []
                if is_news:
                    logger.info("📰 Searching for news...")
                    search_results = await self.web_search.search_news(user_input, max_results=5)
                elif is_knowledge:
                    logger.info("📚 Checking Wikipedia...")
                    search_results = await self.web_search._search_wikipedia(user_input, language)
                    if not search_results:
                        logger.info("🔍 Wikipedia not found, trying web search...")
                        search_results = await self.web_search.search(user_input, max_results=5)
                elif self._needs_web_search(user_input):
                    logger.info("🌐 Searching web...")
                    search_results = await self.web_search.search(user_input, max_results=5)
                
                if search_results:
                    web_context = self.web_search.format_search_results(search_results, language)
                    logger.info(f"✅ Using {len(search_results)} search results")
                else:
                    if is_news or self._needs_web_search(user_input):
                        logger.warning("⚠️ No search results, using general knowledge")
            
            # Build prompt
            prompt = self._build_prompt(user_input, language, web_context)
            
            # API request payload
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 500
                }
            }
            
            logger.info("🤔 Thinking...")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_endpoint, json=payload, timeout=60) as response:
                    if response.status != 200:
                        logger.error(f"❌ API error: {response.status}")
                        return None
                        
                    result = await response.json()
                    assistant_response = result.get("response", "").strip()
            
            if assistant_response:
                # Update conversation history
                self.conversation_history.append({
                    "role": "user",
                    "content": user_input,
                    "language": language
                })
                self.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_response,
                    "language": language
                })
                
                # Keep only last 20 exchanges
                if len(self.conversation_history) > 20:
                    self.conversation_history = self.conversation_history[-20:]
                
                logger.info(f"💬 Assistant: {assistant_response}")
                return assistant_response
            else:
                logger.warning("⚠️ Empty response from model")
                return None
                
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _build_prompt(self, user_input: str, language: str, web_context: str = "") -> str:
        """Build prompt with language instruction, web context, and conversation history."""
        
        assistant_name = config.ASSISTANT_NAME
        assistant_name_hi = config.ASSISTANT_NAME_HI
        assistant_name_gu = config.ASSISTANT_NAME_GU
        
        language_instructions = {
            "en": f"""You are {assistant_name}, a helpful AI voice assistant with web search capability.
Respond ONLY in clear, natural English. Keep responses brief and conversational.
If web search results are provided, use them to give accurate, up-to-date information.
Cite sources when using web information.""",
            
            "hi": f"""तुम {assistant_name_hi} हो, एक सहायक AI असिस्टेंट जो वेब खोज कर सकती है।
केवल हिंदी में जवाब दो। संक्षिप्त और स्पष्ट उत्तर दो। अंग्रेजी का प्रयोग बिल्कुल न करें।
अगर वेब खोज परिणाम दिए गए हैं, तो उनका उपयोग करके सटीक जानकारी दें।""",
            
            "gu": f"""તમે {assistant_name_gu} છો, એક સહાયક AI આસિસ્ટન્ટ જે વેબ શોધ કરી શકે છે.
ફક્ત ગુજરાતીમાં જવાબ આપો। સંક્ષિપ્ત અને સ્પષ્ટ જવાબો આપો। અંગ્રેજીનો ઉપયોગ ન કરો।
જો વેબ શોધ પરિણામો આપવામાં આવે છે, તો તેનો ઉપયોગ કરીને સચોટ માહિતી આપો."""
        }
        
        system_instruction = language_instructions.get(
            language,
            f"You are {assistant_name}, a helpful AI assistant with web search. Respond ONLY in {language}."
        )
        
        prompt_parts = [system_instruction, "\n\n"]
        
        if web_context:
            prompt_parts.append(web_context)
            prompt_parts.append("\n\nUse the above web search information to answer the question.\n\n")
        
        for message in self.conversation_history[-6:]:
            if message.get("language") == language:
                role = message["role"]
                content = message["content"]
                if role == "user":
                    prompt_parts.append(f"User: {content}\n")
                else:
                    prompt_parts.append(f"Assistant: {content}\n")
        
        prompt_parts.append(f"User: {user_input}\n")
        prompt_parts.append("Assistant: ")
        
        return "".join(prompt_parts)
    
    def reset_conversation(self):
        """Clear conversation history."""
        self.conversation_history = []
        self.current_language = "en"
        logger.info("🔄 Conversation history cleared")
