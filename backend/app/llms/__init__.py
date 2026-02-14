
import os
from .gemini_client import GeminiClient, get_gemini_client
from .openai_client import OpenAIClient, get_openai_client

def get_llm_client(provider: str = None):
    """
    Factory to get the appropriate LLM client.
    Prioritizes passed provider, then OpenAI, then Gemini.
    """
    if provider == "openai" and os.getenv("OPENAI_API_KEY"):
        return get_openai_client()
    elif provider == "google" and (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
        return get_gemini_client()

    if os.getenv("OPENAI_API_KEY"):
        return get_openai_client()
    elif os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
        return get_gemini_client()
    else:
        return get_openai_client()

__all__ = ['GeminiClient', 'OpenAIClient', 'get_llm_client', 'get_gemini_client', 'get_openai_client']
