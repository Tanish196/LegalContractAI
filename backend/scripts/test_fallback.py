
import asyncio
import logging
import sys
import os

# Ensure backend directory is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.llms.hybrid_client import HybridLLMClient
from app.utils.rate_limiter import RateLimiter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set dummy env vars for testing
os.environ["OPENAI_API_KEY"] = "sk-test-key"
os.environ["GEMINI_API_KEY"] = "google-test-key"

from app.llms.hybrid_client import HybridLLMClient
from app.utils.rate_limiter import RateLimiter

async def mock_generate(self, prompt, *args, **kwargs):
    return f"Mocked Response from {self.__class__.__name__}"

async def test_fallback():
    print("--- Starting Hybrid Client Fallback Test ---")
    
    # Mock clients to avoid real API calls and simulate rate limits
    client = HybridLLMClient()
    
    # 1. Test Primary Success
    print("\nTest 1: Primary Success")
    if client.openai_client:
        client.openai_client.generate = lambda p, *a, **k: mock_generate(client.openai_client, p)
        res = await client.generate("Hello")
        print(f"Result: {res}")
        assert "OpenAIClient" in res
    else:
        print("Skipping Test 1 (OpenAI not available)")

    # 2. Test Rate Limit Fallback (Simulated 429)
    print("\nTest 2: Rate Limit Fallback (Exception)")
    if client.openai_client and client.gemini_client:
        async def raise_ratelimit(*args, **kwargs):
            raise Exception("429 Too Many Requests")
        
        client.openai_client.generate = raise_ratelimit
        client.gemini_client.generate = lambda p, *a, **k: mock_generate(client.gemini_client, p)
        
        res = await client.generate("Hello")
        print(f"Result: {res}")
        assert "GeminiClient" in res
    else:
         print("Skipping Test 2 (Clients missing)")

    # 3. Test Rate Limiter Block (try_acquire = False)
    print("\nTest 3: Rate Limiter Block (Local)")
    if client.openai_client and client.gemini_client:
        # Manually exhaust rate limiter
        client.openai_client.rate_limiter.rpm_tokens = 0
        
        # Reset gemini mock
        client.gemini_client.generate = lambda p, *a, **k: mock_generate(client.gemini_client, p)

        res = await client.generate("Hello")
        print(f"Result: {res}")
        assert "GeminiClient" in res
    else:
         print("Skipping Test 3 (Clients missing)")
         
    print("\n--- Test Complete ---")

if __name__ == "__main__":
    asyncio.run(test_fallback())
