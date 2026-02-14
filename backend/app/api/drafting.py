"""
Contract Drafting API Endpoint
Uses: ingestion_agent + LLM (no other agents)
"""

import logging
from fastapi import APIRouter, HTTPException, Response, status
from app.schemas import ContractDraftRequest
from app.services.draft_service import generate_draft

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/drafting",
    tags=["Contract Drafting"]
)


@router.post(
    "/draft",
    summary="Draft a new contract",
    description="Generate a professional contract using Agentic Drafting Orchestrator"
)
async def draft_contract(request: ContractDraftRequest):
    """Draft a new contract using the Agentic Drafting Orchestrator.

    **Service Flow:**
    1. Orchestrator initializes
    2. Intent Analysis -> Policy Check -> Template Selection -> Generation -> Review
    3. Returns drafted contract text
    """
    try:
        logger.info("Starting agentic contract drafting request")

        # Map ContractDraftRequest to metadata
        data = request.model_dump()
        
        # Build parties list
        parties = []
        if data.get("parties"):
            for p in data.get("parties"):
                if isinstance(p, dict):
                    name = p.get("name")
                else:
                    name = getattr(p, "name", None)
                if name:
                    parties.append(name)
        else:
            if data.get("party_a"):
                parties.append(data.get("party_a"))
            if data.get("party_b"):
                parties.append(data.get("party_b"))

        requirements_text = data.get("requirements", "")
        # Add key terms and other context to requirements if simple string input
        if data.get("key_terms"):
             requirements_text += f"\n\nKey Terms:\n{data.get('key_terms')}"
        if data.get("purpose"):
             requirements_text += f"\n\nPurpose:\n{data.get('purpose')}"

        metadata = {
            "contract_type": data.get("contract_type") or data.get("purpose") or "General",
            "jurisdiction": data.get("jurisdiction") or "",
            "parties": parties,
            "term": data.get("term") or ""
        }

        # Run Agentic Pipeline
        from app.agents.drafting import DraftingOrchestrator
        orchestrator = DraftingOrchestrator()
        
        final_state = await orchestrator.run(
            raw_requirements=requirements_text, 
            metadata=metadata,
            provider=data.get("provider")
        )
        
        # Return only the contract text (plain text response)
        return Response(content=final_state.final_contract, media_type="text/plain", status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error in agentic draft_contract: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
