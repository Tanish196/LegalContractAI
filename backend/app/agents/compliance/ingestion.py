from app.agents.state import ContractState
import logging

logger = logging.getLogger(__name__)

class IngestionAgent:
    async def process(self, state: ContractState):
        logger.info("IngestionAgent: Processing input text")
        # In a real app, this might handle PDF parsing, OCR, etc.
        # For now, we assume raw_text is populated.
        
        # Basic cleanup
        if not state.raw_text:
            logger.warning("No text provided to IngestionAgent")
            return

        state.add_audit_log("IngestionAgent", "Process", f"Processed input of length {len(state.raw_text)}")
