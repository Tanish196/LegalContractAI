"""
Compliance Check API Endpoint
SYSTEM 2: Uses compliance_service with multi-agent pipeline
"""

import logging
from fastapi import APIRouter, HTTPException, status
from app.schemas import ComplianceCheckRequest, ComplianceCheckResponse, ComplianceIssue, ErrorResponse
# from app.services.compliance_service import check_compliance as run_compliance_pipeline

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
            "request_source": "api",
            "provider": request.provider or "google"
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

        # 1. Detailed Summary Metrics
        high_count = sum(1 for issue in compliance_report if issue.risk_level == "high")
        med_count = sum(1 for issue in compliance_report if issue.risk_level == "medium")
        low_count = sum(1 for issue in compliance_report if issue.risk_level == "low")
        
        summary = {
            "total_clauses": len(final_state.clauses or []),
            "high_risk": high_count,
            "medium_risk": med_count,
            "low_risk": low_count,
            "risk_level": final_state.risk_summary.get("risk_level", "Low"),
            "overall_score": final_state.risk_summary.get("overall_score", 100)
        }
        
        # 2. Action Items for Insights
        action_items = []
        for issue in compliance_report:
            if issue.risk_level in ["high", "medium"]:
                action_items.append({
                    "title": issue.heading or "Compliance Issue",
                    "risk_level": issue.risk_level,
                    "actions": [issue.fix]
                })

        # 3. Dynamic Markdown Generation
        report_md = f"# Compliance Analysis Report\n\n"
        report_md += f"**Jurisdiction:** {jurisdiction}\n"
        report_md += f"**Overall Risk Level:** {summary['risk_level']}\n\n"
        
        if compliance_report:
            report_md += "## Identified Issues\n\n"
            for issue in compliance_report:
                icon = "🔴" if issue.risk_level == "high" else "🟡" if issue.risk_level == "medium" else "🟢"
                report_md += f"### {icon} {issue.heading}\n"
                report_md += f"**Clause:** *\"{issue.clause[:200]}...\"*\n\n"
                report_md += f"**Issue:** {issue.issue_summary}\n\n"
                report_md += f"**Suggested Fix:** {issue.fix}\n\n"
                if issue.citations:
                    report_md += f"**Citations:** {', '.join(issue.citations)}\n\n"
                report_md += "---\n\n"
        else:
            report_md += "✅ No major compliance issues were identified in this document."

        response = ComplianceCheckResponse(
            drafted_contract=final_state.final_contract or contract_text,
            compliance_report=compliance_report,
            summary=summary,
            insights={
                "action_items": action_items,
                "analysis_logs": [log.get("details") for log in final_state.audit_log if log.get("action") == "Analyze"]
            },
            report_markdown=report_md
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
