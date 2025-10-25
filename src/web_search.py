"""Web search integration with Wikipedia support for real-time information retrieval."""

from duckduckgo_search import DDGS
from typing import Optional, List, Dict
import requests
from datetime import datetime
import wikipediaapi


class WebSearchHandler:
    """Handles web searches with Wikipedia integration."""
    
    def __init__(self):
        self.ddgs = DDGS(timeout=20)  # Increased timeout
        self.timeout = 10
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        }
        
        # Initialize Wikipedia API for different languages
        self.wiki_en = wikipediaapi.Wikipedia('Vani-Assistant/1.0', 'en')
        self.wiki_hi = wikipediaapi.Wikipedia('Vani-Assistant/1.0', 'hi')
        self.wiki_gu = wikipediaapi.Wikipedia('Vani-Assistant/1.0', 'gu')
        
        print("✅ Web search enabled (DuckDuckGo + Wikipedia)")
    
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Search the web for information with Wikipedia fallback.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with title, snippet, and url
        """
        try:
            print(f"🔍 Searching web: {query}")
            
            # First try DuckDuckGo
            results = []
            
            try:
                search_results = list(self.ddgs.text(
                    query, 
                    region='in-en',
                    safesearch='moderate',
                    timelimit='m',
                    max_results=max_results
                ))
                
                for result in search_results:
                    results.append({
                        'title': result.get('title', ''),
                        'snippet': result.get('body', ''),
                        'url': result.get('href', ''),
                        'source': 'DuckDuckGo'
                    })
                
                if results:
                    print(f"✅ Found {len(results)} results (DuckDuckGo)")
                    return results
                    
            except Exception as e:
                print(f"⚠️ DuckDuckGo search failed: {str(e)[:100]}")
            
            # If DuckDuckGo fails or no results, try Wikipedia
            print("📚 Trying Wikipedia...")
            wiki_results = self._search_wikipedia(query)
            
            if wiki_results:
                print(f"✅ Found Wikipedia article")
                return wiki_results
            
            print("⚠️ No results found")
            return []
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []
    
    def _search_wikipedia(self, query: str, language: str = 'en') -> List[Dict[str, str]]:
        """
        Search Wikipedia for detailed information.
        
        Args:
            query: Search query
            language: Language code ('en', 'hi', 'gu')
            
        Returns:
            List with Wikipedia article information
        """
        try:
            # Select appropriate Wikipedia instance
            if language == 'hi':
                wiki = self.wiki_hi
            elif language == 'gu':
                wiki = self.wiki_gu
            else:
                wiki = self.wiki_en
            
            # Clean query - remove question words
            clean_query = query.lower()
            
            # Remove common question patterns
            question_patterns = [
                'what is ', 'what are ', 'who is ', 'who are ',
                'tell me about ', 'explain ', 'describe ',
                'definition of ', 'meaning of ', 'history of ',
                'क्या है ', 'कौन है ', 'बताओ ', 'के बारे में ',
                'શું છે ', 'કોણ છે ', 'વિશે જણાવો '
            ]
            
            for pattern in question_patterns:
                clean_query = clean_query.replace(pattern, '')
            
            # Remove punctuation
            clean_query = clean_query.strip().rstrip('?').strip()
            
            # Capitalize first letter for better Wikipedia matching
            clean_query = clean_query.title()
            
            print(f"📚 Searching Wikipedia for: '{clean_query}'")
            
            # Try exact match first
            page = wiki.page(clean_query)
            
            if page.exists():
                summary = page.summary
                
                # Get first 4 sentences for a good summary
                sentences = [s.strip() for s in summary.split('.') if s.strip()]
                short_summary = '. '.join(sentences[:4]) + '.'
                
                return [{
                    'title': page.title,
                    'snippet': short_summary,
                    'url': page.fullurl,
                    'source': 'Wikipedia'
                }]
            
            # If exact match fails, try common variations
            variations = [
                clean_query,
                clean_query.lower(),
                clean_query.replace(' ', '_'),
                clean_query.split()[0] if ' ' in clean_query else clean_query  # First word
            ]
            
            for variation in variations:
                try:
                    page = wiki.page(variation)
                    if page.exists():
                        summary = page.summary
                        sentences = [s.strip() for s in summary.split('.') if s.strip()]
                        short_summary = '. '.join(sentences[:4]) + '.'
                        
                        print(f"✅ Found Wikipedia article: {page.title}")
                        
                        return [{
                            'title': page.title,
                            'snippet': short_summary,
                            'url': page.fullurl,
                            'source': 'Wikipedia'
                        }]
                except:
                    continue
            
            print(f"⚠️ No Wikipedia article found for '{clean_query}'")
            return []
            
        except Exception as e:
            print(f"❌ Wikipedia search error: {str(e)[:100]}")
            return []

    
    def get_wikipedia_summary(self, topic: str, language: str = 'en', sentences: int = 3) -> Optional[str]:
        """
        Get detailed Wikipedia summary for a topic.
        
        Args:
            topic: Topic to search
            language: Language code
            sentences: Number of sentences to return
            
        Returns:
            Summary text or None
        """
        try:
            # Select Wikipedia instance
            if language == 'hi':
                wiki = self.wiki_hi
            elif language == 'gu':
                wiki = self.wiki_gu
            else:
                wiki = self.wiki_en
            
            page = wiki.page(topic)
            
            if page.exists():
                summary = page.summary
                summary_sentences = summary.split('.')
                return '. '.join(summary_sentences[:sentences]) + '.'
            
            return None
            
        except Exception as e:
            print(f"⚠️ Wikipedia summary error: {e}")
            return None
    
    def search_news(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """Search for recent news articles."""
        try:
            print(f"📰 Searching news: {query}")
            
            results = []
            
            try:
                news_results = list(self.ddgs.news(
                    query,
                    region='in-en',
                    safesearch='moderate',
                    timelimit='w',
                    max_results=max_results
                ))
                
                for result in news_results:
                    results.append({
                        'title': result.get('title', ''),
                        'snippet': result.get('body', ''),
                        'url': result.get('url', ''),
                        'date': result.get('date', ''),
                        'source': result.get('source', 'News')
                    })
                
                if results:
                    print(f"✅ Found {len(results)} news articles")
                    return results
                    
            except Exception as e:
                print(f"⚠️ News search error: {str(e)[:100]}")
            
            return []
            
        except Exception as e:
            print(f"❌ News search error: {e}")
            return []
    
    def format_search_results(self, results: List[Dict[str, str]], language: str = 'en') -> str:
        """Format search results for LLM context."""
        if not results:
            return ""
        
        formatted = []
        
        # Header based on language
        if language == 'hi':
            formatted.append("🌐 इंटरनेट खोज परिणाम:\n")
        elif language == 'gu':
            formatted.append("🌐 ઇન્ટરનેટ શોધ પરિણામો:\n")
        else:
            formatted.append("🌐 Search Results:\n")
        
        for i, result in enumerate(results, 1):
            # Title
            if result.get('title'):
                formatted.append(f"\n{i}. {result['title']}")
            
            # Snippet
            if result.get('snippet'):
                snippet = result['snippet'][:400]  # Limit length
                formatted.append(f"   {snippet}...")
            
            # Metadata
            metadata = []
            if result.get('date'):
                metadata.append(f"📅 {result['date']}")
            if result.get('source'):
                metadata.append(f"📚 Source: {result['source']}")
            
            if metadata:
                formatted.append(f"   {' | '.join(metadata)}")
        
        formatted.append("\n\n📝 Use this information to provide an accurate answer.\n")
        
        return "\n".join(formatted)
    
    def get_current_time(self) -> str:
        """Get current date and time."""
        from datetime import datetime
        now = datetime.now()
        return now.strftime('%I:%M %p, %A, %B %d, %Y')
