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
    description="Analyze contract for compliance issues using multi-agent pipeline (ComplianceOrchestrator)"
)
async def check_compliance_endpoint(request: ComplianceCheckRequest):
    """
    Check contract compliance using the Agentic Compliance Orchestrator.
    
    **Service Flow:**
    1. Orchestrator initializes ContractState
    2. Ingestion -> Jurisdiction -> Extraction -> Retrieval -> Reasoning -> Remediation -> Risk Scoring
    3. Returns structured compliance report
    """
    try:
        logger.info("Starting compliance check request via ComplianceOrchestrator")
        
        contract_text = request.contract_text
        jurisdiction = request.jurisdiction or "United States"
        
        # Validate input
        if len(contract_text.strip()) < 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contract text too short (minimum 50 characters)"
            )
        
        # Run Agentic Pipeline
        from app.agents.compliance import ComplianceOrchestrator
        orchestrator = ComplianceOrchestrator()
        
        metadata = {
            "jurisdiction": jurisdiction,
            "request_source": "api"
        }
        
        final_state = await orchestrator.run(raw_text=contract_text, metadata=metadata)
        
        # Map findings to response format
        compliance_report = []
        for clause_id, finding in final_state.compliance_findings.items():
            # Find the clause text
            clause_text = next((c["text"] for c in final_state.clauses if c["id"] == clause_id), "")
            
            compliance_report.append(ComplianceIssue(
                clause=clause_text,
                heading=f"Clause {clause_id}",
                risk_level=finding.get("risk_level", "low").lower(),
                fix=finding.get("suggested_fix", "No fix recommended"),
                issue_summary=finding.get("reason", "Analyzed for compliance"),
                citations=finding.get("citations", [])
            ))

        summary = final_state.risk_summary
        
        # If risk summary is empty/basic, ensure it has the required fields
        if not summary.get("overall_score"):
             # Fallback logic if agent didn't populate it fully (e.g. error)
             high_count = sum(1 for issue in compliance_report if issue.risk_level == "high")
             summary = {
                "overall_score": 100 - (high_count * 10),
                "risk_level": "High" if high_count > 0 else "Low",
                 "breakdown": {"high": high_count}
             }

        response = ComplianceCheckResponse(
            drafted_contract=final_state.final_contract or contract_text,
            compliance_report=compliance_report,
            summary=summary,
            insights={
                "analysis_logs": [log.get("details") for log in final_state.audit_log if log.get("action") == "Analyze"],
                "total_issues": len(compliance_report)
            },
            report_markdown=f"# Compliance Report\n\nOverall Risk: {summary.get('risk_level')}\n\n..."
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
