"""Drafting Service - Multi-Agent Pipeline for Contract Drafting
SYSTEM 1: Drafting Multi-Agent System

Flow:
User Input → ingestion_agent → template_agent → structure_agent → drafting_agent → Output

Output:
{
  "drafted_contract": "Full NDA agreement...",
  "compliance_report": []
}
"""

import logging
from typing import Dict, Any
from app.agents import ingestion_agent, template_agent, structure_agent, drafting_agent

logger = logging.getLogger(__name__)


async def generate_draft(user_input: Dict[str, Any]) -> Dict[str, Any]:
    """Run the complete drafting multi-agent pipeline.

    Args:
        user_input: Raw user input containing contract requirements

    Returns:
        {
            "drafted_contract": "Full legal agreement text...",
            "compliance_report": []
        }
    """
    try:
        logger.info("=" * 60)
        logger.info("DRAFTING PIPELINE - Starting multi-agent flow")
        logger.info("=" * 60)

        # Step 1: ingestion_agent - Normalize and extract user input
        logger.info("Step 1/4: Running ingestion_agent...")
        ingestion_result = await ingestion_agent.run(user_input)
        draft_request = ingestion_result.get("draft_request", {})
        logger.info(f"✓ Ingestion complete - Agreement type: {draft_request.get('agreement_type', 'N/A')}")

        # Step 2: template_agent - Select PDF templates
        logger.info("Step 2/4: Running template_agent...")
        template_result = await template_agent.run(draft_request)
        selected_templates = template_result.get("selected_templates", [])
        logger.info(f"✓ Template selection complete - {len(selected_templates)} template(s) selected")

        # Step 3: structure_agent - Extract template structure
        logger.info("Step 3/4: Running structure_agent...")
        structure_result = await structure_agent.run(template_result)
        template_style = structure_result.get("template_style", {})
        logger.info(f"✓ Structure analysis complete - {len(template_style.get('must_include_clauses', []))} required clauses")

        # Step 4: drafting_agent - Generate final contract with Gemini
        logger.info("Step 4/4: Running drafting_agent (Gemini + PDF templates)...")
        drafting_result = await drafting_agent.run(structure_result)
        drafted_contract = drafting_result.get("drafted_contract", "")
        logger.info(f"✓ Contract generation complete - {len(drafted_contract)} characters")

        logger.info("=" * 60)
        logger.info("DRAFTING PIPELINE - Complete")
        logger.info("=" * 60)

        return {
            "drafted_contract": drafted_contract,
            "compliance_report": []  # Empty for drafting service
        }

    except Exception as e:
        logger.error(f"Error in drafting pipeline: {e}", exc_info=True)
        raise
