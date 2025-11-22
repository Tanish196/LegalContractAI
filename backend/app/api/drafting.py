"""
Contract Drafting API Endpoint
Uses: ingestion_agent + LLM (no other agents)
"""

import logging
from fastapi import APIRouter, HTTPException, status
from app.schemas import ContractDraftRequest, ContractDraftResponse, ErrorResponse
from app.agents import ingestion_agent
from app.llms import get_gemini_client

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/drafting",
    tags=["Contract Drafting"]
)


@router.post(
    "/draft",
    response_model=ContractDraftResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Draft a new contract",
    description="Generate a professional contract using AI based on provided requirements and metadata"
)
async def draft_contract(request: ContractDraftRequest):
    """
    Draft a new contract using ingestion_agent + LLM.
    
    **Service Flow:**
    1. Normalize input data with ingestion_agent
    2. Generate contract with LLM
    3. Return contract with empty compliance_report
    
    **No other agents involved (no clause, compliance, risk, or merge agents)**
    """
    try:
        logger.info("Starting contract drafting request")
        
        # Step 1: Prepare data for ingestion agent
        input_data = request.model_dump()
        
        # Step 2: Normalize input data with ingestion_agent
        logger.info("Normalizing input data with ingestion_agent")
        normalized = await ingestion_agent.run(input_data)
        metadata = normalized["meta"]
        
        logger.info(f"Extracted metadata: {metadata}")
        
        # Step 3: Generate contract with LLM
        logger.info("Generating contract with LLM")
        try:
            llm_client = get_gemini_client()
            
            # Use requirements from request
            requirements = request.requirements
            if request.key_terms:
                requirements += f"\n\nKey Terms:\n{request.key_terms}"
            
            drafted_contract = await llm_client.generate_contract(
                metadata=metadata,
                requirements=requirements
            )
            
            logger.info(f"Contract generated successfully ({len(drafted_contract)} chars)")
            
        except Exception as llm_error:
            logger.error(f"LLM generation failed: {str(llm_error)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate contract: {str(llm_error)}"
            )
        
        # Step 4: Return response
        response = ContractDraftResponse(
            drafted_contract=drafted_contract,
            compliance_report=[],  # Empty for drafting service
            metadata=metadata
        )
        
        logger.info("Contract drafting completed successfully")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in draft_contract: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
