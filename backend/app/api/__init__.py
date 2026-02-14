"""
API Package - REST Endpoints
"""

from .drafting import router as drafting_router
from .compliance import router as compliance_router
from .health import router as health_router
from .reports import router as reports_router
from .analysis import router as analysis_router
from .research import router as research_router
from .summarization import router as summarization_router
from .chat import router as chat_router

__all__ = ['drafting_router', 'compliance_router', 'health_router', 'reports_router', 
           'analysis_router', 'research_router', 'summarization_router', 'chat_router']
