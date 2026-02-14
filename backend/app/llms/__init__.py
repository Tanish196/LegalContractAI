
import os
from .gemini_client import GeminiClient, get_gemini_client
from .openai_client import OpenAIClient, get_openai_client

def get_llm_client(provider: str = None, use_fast: bool = False):
    """
    Factory to get the appropriate LLM client.
    Prioritizes passed provider, then OpenAI, then Gemini.
    
    Args:
        provider: 'openai' or 'google'
        use_fast: If True, uses lighter/faster models (gpt-4o-mini, gemini-1.5-flash)
    """
    # Define fast model mappings
    OPENAI_FAST = "gpt-4.1-nano"
    GEMINI_FAST = "gemini-2.5-flash"
    
    selected_model = None
    if use_fast:
        if provider == "openai" or (not provider and os.getenv("OPENAI_API_KEY")):
            selected_model = OPENAI_FAST
        elif provider == "google" or (not provider and (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))):
            selected_model = GEMINI_FAST

    if provider == "openai" and os.getenv("OPENAI_API_KEY"):
        return get_openai_client(model=selected_model)
    elif provider == "google" and (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
        return get_gemini_client(model=selected_model)

    if os.getenv("OPENAI_API_KEY"):
        return get_openai_client(model=selected_model)
    elif os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
        return get_gemini_client(model=selected_model)
    else:
        return get_openai_client(model=selected_model)

__all__ = ['GeminiClient', 'OpenAIClient', 'get_llm_client', 'get_gemini_client', 'get_openai_client']
