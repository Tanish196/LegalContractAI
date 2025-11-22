"""
Compliance Check API Endpoint
Uses: clause_agent, compliance_agent, risk_agent, merge_agent (optional)
"""

import logging
from fastapi import APIRouter, HTTPException, status
from app.schemas import ComplianceCheckRequest, ComplianceCheckResponse, ComplianceIssue, ErrorResponse
from app.agents import clause_agent, compliance_agent, risk_agent, merge_agent
from app.llms import get_gemini_client

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
    description="Analyze contract for compliance issues and provide risk assessment with recommendations"
)
async def check_compliance(request: ComplianceCheckRequest):
    """
    Check contract compliance using multiple agents.
    
    **Service Flow:**
    1. Split contract into clauses (clause_agent)
    2. For each clause:
       - Analyze compliance (compliance_agent)
       - Classify risk (risk_agent)
       - Optionally merge with fixes (merge_agent)
    3. Return compliance report
    
    **Uses: clause_agent, compliance_agent, risk_agent, merge_agent**
    **Does NOT use: ingestion_agent**
    """
    try:
        logger.info("Starting compliance check request")
        
        contract_text = request.contract_text
        jurisdiction = request.jurisdiction or "United States"
        
        # Validate input
        if len(contract_text.strip()) < 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contract text too short (minimum 50 characters)"
            )
        
        # Step 1: Extract clauses from contract
        logger.info("Extracting clauses with clause_agent")
        try:
            clause_result = await clause_agent.run(contract_text)
            clauses = clause_result.get("clauses", [])
            
            if not clauses:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No valid clauses found in contract. Ensure contract has proper structure."
                )
            
            logger.info(f"Extracted {len(clauses)} clauses")
            
        except Exception as clause_error:
            logger.error(f"Clause extraction failed: {str(clause_error)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to extract clauses: {str(clause_error)}"
            )
        
        # Step 2-4: Process each clause
        compliance_report = []
        
        try:
            # Get LLM client for compliance analysis
            llm_client = get_gemini_client()
            
            for i, clause in enumerate(clauses, 1):
                logger.info(f"Processing clause {i}/{len(clauses)}")
                
                try:
                    # Step 2: Perform compliance analysis
                    compliance_result = await compliance_agent.run(
                        clause=clause,
                        jurisdiction=jurisdiction,
                        llm_client=llm_client
                    )
                    
                    parsed = compliance_result.get("parsed", {})
                    
                    # Step 3: Classify risk level
                    risk_result = await risk_agent.run(parsed)
                    
                    # Step 4: Optional - merge clause with fixes (not used in response, but available)
                    # merge_result = await merge_agent.run(clause, risk_result)
                    
                    # Add to compliance report
                    issue = ComplianceIssue(
                        clause=clause,
                        risk_level=risk_result.get("risk_level", "medium"),
                        fix=risk_result.get("fix", "No fix suggested"),
                        citations=risk_result.get("citations", [])
                    )
                    
                    compliance_report.append(issue)
                    
                    logger.info(f"Clause {i} processed: {risk_result.get('risk_level')} risk")
                    
                except Exception as clause_process_error:
                    logger.error(f"Error processing clause {i}: {str(clause_process_error)}")
                    # Add error entry to report
                    issue = ComplianceIssue(
                        clause=clause,
                        risk_level="unknown",
                        fix=f"Error processing clause: {str(clause_process_error)}",
                        citations=[]
                    )
                    compliance_report.append(issue)
        
        except Exception as llm_error:
            logger.error(f"LLM client error: {str(llm_error)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to analyze compliance: {str(llm_error)}"
            )
        
        # Step 5: Generate summary
        high_count = sum(1 for issue in compliance_report if issue.risk_level == "high")
        medium_count = sum(1 for issue in compliance_report if issue.risk_level == "medium")
        low_count = sum(1 for issue in compliance_report if issue.risk_level == "low")
        
        summary = {
            "total_clauses": len(clauses),
            "high_risk": high_count,
            "medium_risk": medium_count,
            "low_risk": low_count,
            "overall_assessment": "CRITICAL" if high_count > 0 else "REVIEW NEEDED" if medium_count > 0 else "ACCEPTABLE"
        }
        
        # Step 6: Build response
        response = ComplianceCheckResponse(
            drafted_contract=contract_text,
            compliance_report=compliance_report,
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
