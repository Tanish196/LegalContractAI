"""
Health Check and Utility Endpoints
"""

import logging
from fastapi import APIRouter
from app.schemas import HealthResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["Health"]
)


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check if the API and all services are running properly"
)
async def health_check():
    """
    Health check endpoint.
    Verifies that agents and LLM client are properly loaded.
    """
    agents_loaded = False
    llm_available = False
    
    try:
        # Check if agents can be imported
        from app.agents import ingestion_agent, clause_agent, compliance_agent, risk_agent, merge_agent
        agents_loaded = True
    except Exception as e:
        logger.error(f"Failed to load agents: {str(e)}")
    
    try:
        # Check if LLM client is available
        from app.llms import get_gemini_client
        client = get_gemini_client()
        llm_available = True
    except Exception as e:
        logger.error(f"Failed to load LLM client: {str(e)}")
    
    return HealthResponse(
        status="healthy" if (agents_loaded and llm_available) else "degraded",
        version="1.0.0",
        agents_loaded=agents_loaded,
        llm_available=llm_available
    )
