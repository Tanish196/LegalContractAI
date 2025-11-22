"""Compliance Service - Multi-Agent Pipeline for Compliance Checking
SYSTEM 2: Compliance Multi-Agent System

Flow:
User Input → ingestion_agent → clause_agent → compliance_agent (dummy RAG) → risk_agent → Output

Output:
{
  "drafted_contract": null,
  "compliance_report": [
    {
      "clause": "...",
      "risk_level": "high|medium|low",
      "fix": "Missing required clause",
      "citations": ["Dummy_Data_v1"]
    }
  ]
}
"""

import logging
from typing import Dict, Any, List
from app.agents import clause_agent, compliance_agent, risk_agent
from app.llms import get_gemini_client

logger = logging.getLogger(__name__)

# Hardcoded clause library for dummy RAG
CLAUSE_LIBRARY = {
    "Payment_Terms": {
        "text": "Payment shall be made within 30 days of invoice date.",
        "rules": ["Must specify schedule", "Must define late fees", "Must include payment method"]
    },
    "Confidentiality": {
        "text": "All confidential information must be protected and not disclosed to third parties.",
        "rules": ["Must define confidential info", "Must allow whistleblowing", "Must specify return of materials"]
    },
    "Termination": {
        "text": "Either party may terminate this agreement with 30 days written notice.",
        "rules": ["Must specify notice period", "Must define termination procedures", "Must address post-termination obligations"]
    },
    "Liability": {
        "text": "Liability shall be limited to the amount paid under this agreement.",
        "rules": ["Must define liability caps", "Must address indemnification", "Must exclude consequential damages"]
    },
    "Non_Competition": {
        "text": "Party shall not compete in the same market during the term and for 1 year after.",
        "rules": ["Must define scope", "Must specify duration", "Must be reasonable in geography"]
    },
    "Dispute_Resolution": {
        "text": "Disputes shall be resolved through binding arbitration.",
        "rules": ["Must specify forum", "Must define arbitration rules", "Must address costs"]
    }
}


async def check_compliance(contract_text: str, jurisdiction: str = "United States") -> Dict[str, Any]:
    """Run the complete compliance checking multi-agent pipeline.

    Args:
        contract_text: Full contract text to analyze
        jurisdiction: Legal jurisdiction for compliance

    Returns:
        {
            "drafted_contract": null,
            "compliance_report": [...]
        }
    """
    try:
        logger.info("=" * 60)
        logger.info("COMPLIANCE PIPELINE - Starting multi-agent flow")
        logger.info("=" * 60)

        # Step 1: clause_agent - Split contract into clauses
        logger.info("Step 1/3: Running clause_agent...")
        clause_result = await clause_agent.run(contract_text)
        clauses = clause_result.get("clauses", [])
        logger.info(f"✓ Clause extraction complete - {len(clauses)} clause(s) found")

        if not clauses:
            logger.warning("No clauses extracted from contract")
            return {
                "drafted_contract": None,
                "compliance_report": []
            }

        # Get LLM client for compliance analysis
        llm_client = get_gemini_client()

        compliance_report = []

        # Step 2-3: For each clause, run compliance_agent → risk_agent
        for i, clause in enumerate(clauses, 1):
            logger.info(f"Processing clause {i}/{len(clauses)}")

            # Step 2: compliance_agent - Dummy RAG analysis
            logger.info(f"  Step 2: Running compliance_agent (dummy RAG)...")
            compliance_result = await compliance_agent.run(
                clause=clause,
                jurisdiction=jurisdiction,
                llm_client=llm_client
            )

            parsed = compliance_result.get("parsed", {})

            # Step 3: risk_agent - Classify risk level
            logger.info(f"  Step 3: Running risk_agent...")
            risk_result = await risk_agent.run(parsed)

            # Build compliance issue
            issue = {
                "clause": clause[:200] + "..." if len(clause) > 200 else clause,
                "risk_level": risk_result.get("risk_level", "medium"),
                "fix": risk_result.get("fix", "Review clause for compliance"),
                "citations": risk_result.get("citations", ["Dummy_Data_v1"])
            }

            compliance_report.append(issue)
            logger.info(f"  ✓ Clause {i} analyzed - Risk: {issue['risk_level']}")

        logger.info("=" * 60)
        logger.info(f"COMPLIANCE PIPELINE - Complete - {len(compliance_report)} issues found")
        logger.info("=" * 60)

        return {
            "drafted_contract": None,
            "compliance_report": compliance_report
        }

    except Exception as e:
        logger.error(f"Error in compliance pipeline: {e}", exc_info=True)
        raise


def get_relevant_clauses(issues: List[str]) -> List[Dict[str, Any]]:
    """Get relevant clauses from library based on identified issues.

    Args:
        issues: List of issue types (e.g., ["Payment", "Confidentiality"])

    Returns:
        List of clause dictionaries with text and rules
    """
    relevant = []

    for issue in issues:
        issue_normalized = issue.replace(" ", "_")
        for clause_type, clause_data in CLAUSE_LIBRARY.items():
            if issue_normalized.lower() in clause_type.lower():
                relevant.append({
                    "type": clause_type,
                    "text": clause_data["text"],
                    "rules": clause_data["rules"]
                })
                break

    # If no specific matches, return all clauses
    if not relevant:
        for clause_type, clause_data in CLAUSE_LIBRARY.items():
            relevant.append({
                "type": clause_type,
                "text": clause_data["text"],
                "rules": clause_data["rules"]
            })

    return relevant
