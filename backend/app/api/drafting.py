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
    description="Generate a professional contract using AI based on provided requirements and PDF templates"
)
async def draft_contract(request: ContractDraftRequest):
    """Draft a new contract using the PDF-template-aware draft service.

    This endpoint preserves the existing frontend route `/api/drafting/draft` and
    accepts the original `ContractDraftRequest` schema. It returns ONLY the
    drafted contract text (plain text) in the response body.
    """
    try:
        logger.info("Starting template-based contract drafting request")

        # Map ContractDraftRequest to the simple payload expected by generate_draft
        data = request.model_dump()

        # Build parties list: prefer structured parties, fallback to party_a/party_b
        parties = []
        if data.get("parties"):
            # parties may be list of dicts (PartyInput); extract names
            for p in data.get("parties"):
                if isinstance(p, dict):
                    name = p.get("name")
                else:
                    # Pydantic may return BaseModel instances
                    name = getattr(p, "name", None)
                if name:
                    parties.append(name)
        else:
            if data.get("party_a"):
                parties.append(data.get("party_a"))
            if data.get("party_b"):
                parties.append(data.get("party_b"))

        payload = {
            "parties": parties,
            "jurisdiction": data.get("jurisdiction") or "",
            "agreement_type": data.get("contract_type") or data.get("purpose") or "Agreement",
            "purpose": data.get("purpose") or "",
            "term": data.get("term") or "",
            "effective_date": None,
            "additional_requirements": data.get("requirements", "")
        }

        # Add key_terms to additional_requirements if present
        if data.get("key_terms"):
            payload["additional_requirements"] += f"\n\nKey Terms:\n{data.get('key_terms')}"

        # Call draft service which uses PDF templates and Gemini
        result = await generate_draft(payload)

        contract_text = result.get("drafted_contract", "") if isinstance(result, dict) else str(result)

        # Return only the contract text (plain text response)
        return Response(content=contract_text, media_type="text/plain", status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error in template-based draft_contract: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
