
from app.agents.state import ContractState
from app.llms import get_llm_client
import logging
import json

logger = logging.getLogger(__name__)

class JurisdictionResolverAgent:
    async def process(self, state: ContractState):
        logger.info("JurisdictionResolverAgent: Determining jurisdiction")
        
        # Simple heuristic or LLM call
        # If user provided jurisdiction in metadata, use that.
        if state.metadata.get("jurisdiction"):
             state.jurisdiction = {"country": "India", "region": state.metadata.get("jurisdiction")} # normalizing
             state.add_audit_log("JurisdictionResolver", "Check", f"Used metadata: {state.jurisdiction}")
             return

        # Else, use LLM to detect

        llm = get_llm_client()
        prompt = f"""
        Analyze the following contract text and identify the governing law and jurisdiction.
        Return JSON with keys: "country", "state" (if applicable), "city" (if applicable).
        
        Text: {state.raw_text[:2000]}...
        """
        
        try:
             # This is a placeholder for actual LLM call which would need structured output parsing
             # defaulting to India for now as per project scope
             state.jurisdiction = {"country": "India", "derived_from": "default"}
             state.add_audit_log("JurisdictionResolver", "Inference", "Defaulted to India (LLM placeholder)")
        except Exception as e:
             logger.error(f"Jurisdiction detection failed: {e}")
             state.jurisdiction = {"country": "India", "error": str(e)}
