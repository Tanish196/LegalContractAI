
import os
from typing import Optional
from .gemini_client import GeminiClient, get_gemini_client
from .openai_client import OpenAIClient, get_openai_client
from .hybrid_client import HybridLLMClient, get_hybrid_client

def get_llm_client(provider: Optional[str] = None, use_fast: bool = False):
    """
    Factory to get the appropriate LLM client.
    Prioritizes passed provider, then OpenAI, then Gemini.
    
    Args:
        provider: 'openai' or 'google'
        use_fast: If True, uses lighter/faster models (gpt-4.1-nano, gemini-3-flash-preview)
    """
    # Define fast model mappings
    OPENAI_FAST = "gpt-4.1-nano"
    GEMINI_FAST = "gemini-3-flash-preview"
    
    selected_model = None
    if use_fast:
        if provider == "openai" or (not provider and os.getenv("OPENAI_API_KEY")):
            selected_model = OPENAI_FAST
        elif provider == "google" or (not provider and (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))):
            selected_model = GEMINI_FAST

    # If a specific provider is requested, we use HybridClient but set that provider as primary
    # This ensures we still have fallback capabilities if the primary fails
    if provider == "openai":
        return HybridLLMClient(primary_provider="openai", model=selected_model)
    elif provider == "google":
        return HybridLLMClient(primary_provider="google", model=selected_model)

    # Default to Hybrid Client (defaults to OpenAI primary)
    return get_hybrid_client()

    # Default to Hybrid Client for fallback behavior
    return get_hybrid_client()

__all__ = ['GeminiClient', 'OpenAIClient', 'HybridLLMClient', 'get_llm_client', 'get_gemini_client', 'get_openai_client', 'get_hybrid_client']
