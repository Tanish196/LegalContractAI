"""
Agents Package - LegalContractAI Backend

This package contains all agent modules for the LegalContractAI backend:

- ingestion_agent: Data normalization and extraction (used in drafting service)
- clause_agent: Contract clause extraction (used in compliance service)
- compliance_agent: Legal snippet search and LLM analysis (used in compliance service)
- risk_agent: Risk level classification (used in compliance service)
- merge_agent: Clause enhancement with fixes (optional, used in compliance service)

Each agent is independent and can be imported individually:
    from app.agents import ingestion_agent, clause_agent, compliance_agent, risk_agent, merge_agent

Or run directly:
    result = await ingestion_agent.run(data)
"""

from . import ingestion_agent
from . import clause_agent
from . import compliance_agent
from . import risk_agent
from . import merge_agent

__all__ = [
    'ingestion_agent',
    'clause_agent',
    'compliance_agent',
    'risk_agent',
    'merge_agent'
]

