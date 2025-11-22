"""
Compliance Check API Endpoint
SYSTEM 2: Uses compliance_service with multi-agent pipeline
"""

import logging
from fastapi import APIRouter, HTTPException, status
from app.schemas import ComplianceCheckRequest, ComplianceCheckResponse, ComplianceIssue, ErrorResponse
from app.services.compliance_service import check_compliance as run_compliance_pipeline

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/compliance",
    tags=["Compliance Check"]
)


@router.post(
    "/check",
    response_model=ComplianceCheckResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Check contract compliance",
    description="Analyze contract for compliance issues using multi-agent pipeline with dummy RAG logic"
)
async def check_compliance_endpoint(request: ComplianceCheckRequest):
    """
    Check contract compliance using multi-agent pipeline.
    
    **Service Flow:**
    1. Split contract into clauses (clause_agent)
    2. For each clause:
       - Analyze compliance with dummy RAG rules (compliance_agent)
       - Classify risk level (risk_agent)
    3. Return compliance report
    
    **Multi-Agent Pipeline: clause_agent → compliance_agent → risk_agent**
    """
    try:
        logger.info("Starting compliance check request via multi-agent pipeline")
        
        contract_text = request.contract_text
        jurisdiction = request.jurisdiction or "United States"
        
        # Validate input
        if len(contract_text.strip()) < 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contract text too short (minimum 50 characters)"
            )
        
        # Run compliance pipeline (clause_agent → compliance_agent → risk_agent)
        result = await run_compliance_pipeline(contract_text, jurisdiction)
        
        compliance_report = result.get("compliance_report", [])
        
        # Generate summary
        high_count = sum(1 for issue in compliance_report if issue.get("risk_level") == "high")
        medium_count = sum(1 for issue in compliance_report if issue.get("risk_level") == "medium")
        low_count = sum(1 for issue in compliance_report if issue.get("risk_level") == "low")
        
        summary = {
            "total_clauses": len(compliance_report),
            "high_risk": high_count,
            "medium_risk": medium_count,
            "low_risk": low_count,
            "overall_assessment": "CRITICAL" if high_count > 0 else "REVIEW NEEDED" if medium_count > 0 else "ACCEPTABLE"
        }
        
        # Build response
        response = ComplianceCheckResponse(
            drafted_contract=contract_text,
            compliance_report=[ComplianceIssue(**issue) for issue in compliance_report],
            summary=summary
        )
        
        logger.info(f"Compliance check completed: {len(compliance_report)} issues found")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in check_compliance: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
