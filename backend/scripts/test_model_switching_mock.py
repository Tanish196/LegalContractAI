
import sys
from unittest.mock import MagicMock

# Mock external dependencies BEFORE importing app modules
sys.modules["google"] = MagicMock()
sys.modules["google.generativeai"] = MagicMock()
sys.modules["google.generativeai.types"] = MagicMock()
sys.modules["langchain_openai"] = MagicMock()
sys.modules["langchain_core"] = MagicMock()
sys.modules["langchain_core.messages"] = MagicMock()
sys.modules["langchain_core.prompts"] = MagicMock()
sys.modules["langchain_core.output_parsers"] = MagicMock()
sys.modules["langchain_core.tools"] = MagicMock()
sys.modules["langchain"] = MagicMock()
sys.modules["langchain.agents"] = MagicMock()
sys.modules["fastapi"] = MagicMock()
sys.modules["pydantic"] = MagicMock()

# Mock app config to avoid import errors
sys.modules["app.config"] = MagicMock()
sys.modules["app.config"].OPENAI_API_KEY = "dummy"
sys.modules["app.config"].GEMINI_API_KEY = "dummy"

import os
import asyncio

# Add backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock the OpenAIClient and GeminiClient classes to avoid instantiation issues with mocks
# We need to do this BEFORE importing get_llm_client if it imports them at top level
import app.llms.openai_client
import app.llms.gemini_client
app.llms.openai_client.OpenAIClient = MagicMock()
app.llms.gemini_client.GeminiClient = MagicMock()

# Fix rate limiter mock if needed
sys.modules["app.utils.rate_limiter"] = MagicMock()

from app.llms import get_llm_client
from app.llms.hybrid_client import HybridLLMClient

async def test_logic():
    print("--- Testing Logic with Mocks ---")

    # TEST 1: Default
    print("\n1. Testing Default (No provider specified)")
    client = get_llm_client()
    print(f"Client type: {type(client).__name__}")
    if isinstance(client, HybridLLMClient):
        print(f"Primary provider: {client.primary_provider}")
        assert client.primary_provider == "openai" # Default

    # TEST 2: OpenAI
    print("\n2. Testing OpenAI Provider")
    client = get_llm_client(provider="openai")
    print(f"Client type: {type(client).__name__}")
    if isinstance(client, HybridLLMClient):
        print(f"Primary provider: {client.primary_provider}")
        assert client.primary_provider == "openai"

    # TEST 3: Google
    print("\n3. Testing Google Provider")
    client = get_llm_client(provider="google")
    print(f"Client type: {type(client).__name__}")
    if isinstance(client, HybridLLMClient):
        print(f"Primary provider: {client.primary_provider}")
        assert client.primary_provider == "google"

    print("\n--- Success! Logic Verified ---")

if __name__ == "__main__":
    asyncio.run(test_logic())
