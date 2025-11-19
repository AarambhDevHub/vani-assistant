"""Web search integration with Wikipedia support for real-time information retrieval."""

from duckduckgo_search import DDGS
from typing import Optional, List, Dict
import asyncio
from datetime import datetime
import wikipediaapi
from .logger import logger

class WebSearchHandler:
    """Handles web searches with Wikipedia integration (Async)."""
    
    def __init__(self):
        self.ddgs = DDGS(timeout=20)
        self.timeout = 10
        
        # Initialize Wikipedia API for different languages
        self.wiki_en = wikipediaapi.Wikipedia('Vani-Assistant/1.0', 'en')
        self.wiki_hi = wikipediaapi.Wikipedia('Vani-Assistant/1.0', 'hi')
        self.wiki_gu = wikipediaapi.Wikipedia('Vani-Assistant/1.0', 'gu')
        
        logger.info("✅ Web search enabled (DuckDuckGo + Wikipedia)")
    
    async def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Search the web for information with Wikipedia fallback.
        """
        try:
            logger.info(f"🔍 Searching web: {query}")
            
            # Run blocking DDGS in executor
            loop = asyncio.get_event_loop()
            
            try:
                # DuckDuckGo Search
                search_results = await loop.run_in_executor(
                    None, 
                    lambda: list(self.ddgs.text(
                        query, 
                        region='in-en',
                        safesearch='moderate',
                        timelimit='m',
                        max_results=max_results
                    ))
                )
                
                results = []
                for result in search_results:
                    results.append({
                        'title': result.get('title', ''),
                        'snippet': result.get('body', ''),
                        'url': result.get('href', ''),
                        'source': 'DuckDuckGo'
                    })
                
                if results:
                    logger.info(f"✅ Found {len(results)} results (DuckDuckGo)")
                    return results
                    
            except Exception as e:
                logger.warning(f"⚠️ DuckDuckGo search failed: {str(e)[:100]}")
            
            # If DuckDuckGo fails or no results, try Wikipedia
            logger.info("📚 Trying Wikipedia...")
            wiki_results = await self._search_wikipedia(query)
            
            if wiki_results:
                logger.info(f"✅ Found Wikipedia article")
                return wiki_results
            
            logger.warning("⚠️ No results found")
            return []
            
        except Exception as e:
            logger.error(f"❌ Search error: {e}")
            return []
    
    async def _search_wikipedia(self, query: str, language: str = 'en') -> List[Dict[str, str]]:
        """Search Wikipedia for detailed information (Async wrapper)."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._search_wikipedia_sync, query, language)

    def _search_wikipedia_sync(self, query: str, language: str = 'en') -> List[Dict[str, str]]:
        """Synchronous Wikipedia search logic."""
        try:
            # Select appropriate Wikipedia instance
            if language == 'hi':
                wiki = self.wiki_hi
            elif language == 'gu':
                wiki = self.wiki_gu
            else:
                wiki = self.wiki_en
            
            # Clean query
            clean_query = query.lower()
            question_patterns = [
                'what is ', 'what are ', 'who is ', 'who are ',
                'tell me about ', 'explain ', 'describe ',
                'definition of ', 'meaning of ', 'history of ',
                'क्या है ', 'कौन है ', 'बताओ ', 'के बारे में ',
                'શું છે ', 'કોણ છે ', 'વિશે જણાવો '
            ]
            
            for pattern in question_patterns:
                clean_query = clean_query.replace(pattern, '')
            
            clean_query = clean_query.strip().rstrip('?').strip().title()
            
            logger.info(f"📚 Searching Wikipedia for: '{clean_query}'")
            
            # Try exact match
            page = wiki.page(clean_query)
            if page.exists():
                return [self._format_wiki_page(page)]
            
            # Try variations
            variations = [
                clean_query,
                clean_query.lower(),
                clean_query.replace(' ', '_'),
                clean_query.split()[0] if ' ' in clean_query else clean_query
            ]
            
            for variation in variations:
                try:
                    page = wiki.page(variation)
                    if page.exists():
                        logger.info(f"✅ Found Wikipedia article: {page.title}")
                        return [self._format_wiki_page(page)]
                except:
                    continue
            
            logger.warning(f"⚠️ No Wikipedia article found for '{clean_query}'")
            return []
            
        except Exception as e:
            logger.error(f"❌ Wikipedia search error: {str(e)[:100]}")
            return []

    def _format_wiki_page(self, page) -> Dict[str, str]:
        """Helper to format wiki page result."""
        summary = page.summary
        sentences = [s.strip() for s in summary.split('.') if s.strip()]
        short_summary = '. '.join(sentences[:4]) + '.'
        
        return {
            'title': page.title,
            'snippet': short_summary,
            'url': page.fullurl,
            'source': 'Wikipedia'
        }
    
    async def search_news(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """Search for recent news articles (Async)."""
        try:
            logger.info(f"📰 Searching news: {query}")
            
            loop = asyncio.get_event_loop()
            
            news_results = await loop.run_in_executor(
                None,
                lambda: list(self.ddgs.news(
                    query,
                    region='in-en',
                    safesearch='moderate',
                    timelimit='w',
                    max_results=max_results
                ))
            )
            
            results = []
            for result in news_results:
                results.append({
                    'title': result.get('title', ''),
                    'snippet': result.get('body', ''),
                    'url': result.get('url', ''),
                    'date': result.get('date', ''),
                    'source': result.get('source', 'News')
                })
            
            if results:
                logger.info(f"✅ Found {len(results)} news articles")
                return results
                
            return []
            
        except Exception as e:
            logger.error(f"❌ News search error: {e}")
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
            if result.get('title'):
                formatted.append(f"\n{i}. {result['title']}")
            
            if result.get('snippet'):
                snippet = result['snippet'][:400]
                formatted.append(f"   {snippet}...")
            
            metadata = []
            if result.get('date'):
                metadata.append(f"📅 {result['date']}")
            if result.get('source'):
                metadata.append(f"📚 Source: {result['source']}")
            
            if metadata:
                formatted.append(f"   {' | '.join(metadata)}")
        
        formatted.append("\n\n📝 Use this information to provide an accurate answer.\n")
        return "\n".join(formatted)
