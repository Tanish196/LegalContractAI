from app.agents.state import ContractState
from app.llms import get_llm_client
import logging
import json

logger = logging.getLogger(__name__)

class TemplateSelectionAgent:
    """Selects the best contract template structure using LLM analysis."""

    # Standard template structures for different contract types
    TEMPLATE_STRUCTURES = {
        "nda": "NDA_Standard_v1",
        "non-disclosure": "NDA_Standard_v1",
        "service": "ServiceAgreement_Standard_v1",
        "service agreement": "ServiceAgreement_Standard_v1",
        "employment": "Employment_Standard_v1",
        "lease": "Lease_Standard_v1",
        "purchase": "Purchase_Standard_v1",
        "consulting": "Consulting_Standard_v1",
        "partnership": "Partnership_Standard_v1",
        "licensing": "Licensing_Standard_v1",
    }

    async def process(self, state: ContractState):
        logger.info("TemplateSelectionAgent: Selecting template via LLM")

        contract_type = state.metadata.get("contract_type", "General")
        detected_intent = state.metadata.get("detected_intent", contract_type)
        jurisdiction = state.metadata.get("jurisdiction", "United States")

        llm = get_llm_client()

        prompt = f"""Based on this contract request, determine the best template structure.

**Detected Intent:** {detected_intent}
**Contract Type:** {contract_type}
**Jurisdiction:** {jurisdiction}
**User Requirements:** {state.raw_text[:500]}

Available template types: {list(self.TEMPLATE_STRUCTURES.keys())}

Respond in valid JSON only (no markdown fences):
{{
  "selected_template_key": "<best matching key from the available types, or 'general' if none fit>",
  "required_sections": ["<ordered list of sections that MUST be in this contract>"],
  "optional_sections": ["<sections that would be beneficial but not mandatory>"],
  "jurisdiction_specific_notes": "<any jurisdiction-specific requirements>"
}}"""

        try:
            response = await llm.generate(prompt, temperature=0.1, max_tokens=1000)

            clean = response.strip()
            if clean.startswith("```"):
                clean = clean.split("\n", 1)[1] if "\n" in clean else clean[3:]
            if clean.endswith("```"):
                clean = clean[:-3]
            clean = clean.strip()

            parsed = json.loads(clean)

            template_key = parsed.get("selected_template_key", "general")
            template_name = self.TEMPLATE_STRUCTURES.get(
                template_key,
                f"{detected_intent.replace(' ', '')}_Custom_v1"
            )

            state.metadata["selected_template"] = template_name
            state.metadata["required_sections"] = parsed.get("required_sections", [])
            state.metadata["optional_sections"] = parsed.get("optional_sections", [])
            state.metadata["jurisdiction_notes"] = parsed.get("jurisdiction_specific_notes", "")

            state.add_audit_log(
                "TemplateSelection", "Select",
                f"Selected: {template_name} with {len(state.metadata['required_sections'])} required sections"
            )
            logger.info(f"TemplateSelectionAgent: Selected {template_name}")

        except json.JSONDecodeError:
            # Fallback: match from metadata
            fallback = self._match_template(detected_intent, contract_type)
            state.metadata["selected_template"] = fallback
            state.add_audit_log("TemplateSelection", "Fallback", f"Used keyword matching: {fallback}")
            logger.warning(f"TemplateSelectionAgent: Parse error, fallback to {fallback}")

        except Exception as e:
            logger.error(f"TemplateSelectionAgent failed: {e}", exc_info=True)
            fallback = self._match_template(detected_intent, contract_type)
            state.metadata["selected_template"] = fallback
            state.add_audit_log("TemplateSelection", "Error", f"LLM failed, fallback: {fallback}")

    def _match_template(self, detected_intent: str, contract_type: str) -> str:
        """Keyword-based fallback template matching."""
        search_text = f"{detected_intent} {contract_type}".lower()
        for key, template in self.TEMPLATE_STRUCTURES.items():
            if key in search_text:
                return template
        return f"{contract_type}_General_v1"
