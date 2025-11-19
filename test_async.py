import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.llm_handler import OllamaHandler
from src.web_search import WebSearchHandler
from src.logger import logger

async def test_async_components():
    print("🧪 Testing Async Components...")
    
    # Test Web Search
    print("\n1. Testing Web Search...")
    search = WebSearchHandler()
    results = await search.search("python async programming", max_results=1)
    if results:
        print(f"✅ Web Search Success: {results[0]['title']}")
    else:
        print("❌ Web Search Failed (or no results)")

    # Test LLM
    print("\n2. Testing LLM Connection...")
    llm = OllamaHandler()
    await llm.initialize()
    
    # Simple generation test
    print("   Generating response...")
    response = await llm.generate_response("Hello, are you working?")
    if response:
        print(f"✅ LLM Success: {response}")
    else:
        print("❌ LLM Failed")

if __name__ == "__main__":
    try:
        asyncio.run(test_async_components())
    except Exception as e:
        print(f"❌ Test Failed: {e}")
