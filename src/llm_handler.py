"""Ollama LLM integration with web search support."""

import requests
import json
from typing import Optional
from . import config
from .web_search import WebSearchHandler


class OllamaHandler:
    """Handles communication with Ollama API with web search capability."""
    
    def __init__(self):
        self.base_url = config.OLLAMA_BASE_URL
        self.model = config.OLLAMA_MODEL
        self.api_endpoint = config.OLLAMA_API_ENDPOINT
        self.conversation_history = []
        self.current_language = "en"
        
        # Initialize web search
        self.web_search = WebSearchHandler()
        
        # Verify Ollama is running
        self._check_connection()
    
    def _check_connection(self):
        """Check if Ollama is running and model is available."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models]
            
            if self.model not in model_names:
                print(f"⚠️ Warning: Model '{self.model}' not found")
                print(f"Available models: {', '.join(model_names)}")
            else:
                print(f"✅ Connected to Ollama - Using model: {self.model}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to Ollama: {e}")
            print("Make sure Ollama is running: ollama serve")
            raise
    
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

    def generate_response(self, user_input: str, language: str = "en") -> Optional[str]:
        """Generate response with intelligent source selection."""
        try:
            self.current_language = language
            web_context = ""
            
            if config.ENABLE_WEB_SEARCH:
                # Determine search type
                is_news = self._needs_web_search(user_input) and any(
                    word in user_input.lower() 
                    for word in ['news', 'latest', 'recent', 'समाचार', 'સમાચાર']
                )
                
                is_knowledge = self._is_knowledge_query(user_input)
                
                if is_news:
                    # News search
                    print("📰 Searching for news...")
                    search_results = self.web_search.search_news(user_input, max_results=5)
                elif is_knowledge:
                    # Try Wikipedia first for knowledge queries
                    print("📚 Checking Wikipedia...")
                    search_results = self.web_search._search_wikipedia(user_input, language)
                    
                    # If Wikipedia has no results, try web search
                    if not search_results:
                        print("🔍 Wikipedia not found, trying web search...")
                        search_results = self.web_search.search(user_input, max_results=5)
                elif self._needs_web_search(user_input):
                    # Regular web search
                    print("🌐 Searching web...")
                    search_results = self.web_search.search(user_input, max_results=5)
                else:
                    search_results = []
                
                if search_results:
                    web_context = self.web_search.format_search_results(
                        search_results,
                        language
                    )
                    print(f"✅ Using {len(search_results)} search results")
                else:
                    print("⚠️ No search results, using general knowledge")
            
            # Build prompt and generate response
            prompt = self._build_prompt(user_input, language, web_context)
            
            # API request payload
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 200
                }
            }
            
            print("🤔 Thinking...")
            
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
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
                
                # Keep only last 6 exchanges
                if len(self.conversation_history) > 12:
                    self.conversation_history = self.conversation_history[-12:]
                
                print(f"💬 Assistant: {assistant_response}")
                return assistant_response
            else:
                print("⚠️ Empty response from model")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ API error: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            return None

    
    def _build_prompt(self, user_input: str, language: str, web_context: str = "") -> str:
        """Build prompt with language instruction, web context, and conversation history."""
        
        assistant_name = config.ASSISTANT_NAME
        assistant_name_hi = config.ASSISTANT_NAME_HI
        assistant_name_gu = config.ASSISTANT_NAME_GU
        
        # Enhanced language-specific system prompts with web search capability
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
        
        # Add web search context if available
        if web_context:
            prompt_parts.append(web_context)
            prompt_parts.append("\n\nUse the above web search information to answer the question.\n\n")
        
        # Add conversation history
        for message in self.conversation_history[-6:]:
            if message.get("language") == language:
                role = message["role"]
                content = message["content"]
                
                if role == "user":
                    prompt_parts.append(f"User: {content}\n")
                else:
                    prompt_parts.append(f"{assistant_name}: {content}\n")
        
        # Add current user input
        prompt_parts.append(f"User: {user_input}\n")
        
        if language == "hi":
            prompt_parts.append(f"{assistant_name_hi} (हिंदी में उत्तर दें): ")
        elif language == "gu":
            prompt_parts.append(f"{assistant_name_gu} (ગુજરાતીમાં જવાબ આપો): ")
        else:
            prompt_parts.append(f"{assistant_name}: ")
        
        return "".join(prompt_parts)
    
    def reset_conversation(self):
        """Clear conversation history."""
        self.conversation_history = []
        self.current_language = "en"
        print("🔄 Conversation history cleared")
