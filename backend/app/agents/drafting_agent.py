"""Drafting Agent - Final Contract Generation with Gemini + PDFs
Used in: Drafting Multi-Agent System

Purpose:
- Take all processed data from previous agents
- Integrate with Gemini 1.5 API
- Send [system_prompt, user_prompt, PDF files]
- Generate final legal agreement
"""

import logging
from typing import Dict, List, Any
from pathlib import Path

from app.llms import get_llm_client

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DraftingAgent:
    """Generates final contract using Gemini API with PDF templates."""

    def __init__(self):
        """Initialize drafting agent."""
        logger.info("DraftingAgent initialized")

    async def run(self, agent_data: Dict[str, Any]) -> Dict[str, str]:
        """Generate final contract using Gemini with PDF templates.

        Args:
            agent_data: Output from structure_agent containing:
                - template_style
                - draft_request
                - selected_templates

        Returns:
            {
                "drafted_contract": "Full legal agreement text..."
            }
        """
        try:
            draft_request = agent_data.get("draft_request", {})
            template_style = agent_data.get("template_style", {})
            selected_templates = agent_data.get("selected_templates", [])

            logger.info("Generating contract with Gemini + PDF templates")

            # Build system prompt
            system_prompt = self._build_system_prompt(template_style)

            # Build user prompt
            user_prompt = self._build_user_prompt(draft_request, template_style)

            # Extract PDF paths
            pdf_paths = [t.get("file_uri") for t in selected_templates if t.get("file_uri")]
            # Convert file:/// URIs back to absolute paths for the client
            pdf_paths = [p.replace("file:///", "") if p.startswith("file:///") else p for p in pdf_paths]

            logger.info(f"Calling Gemini with {len(pdf_paths)} PDF template(s)")

            # Call Gemini client
            client = get_llm_client()
            result = await client.generate_with_pdfs(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                pdf_paths=pdf_paths if pdf_paths else None,
                temperature=0.2,
                max_tokens=8192
            )

            # Extract text from result
            contract_text = result.get("text", "") if isinstance(result, dict) else str(result)

            logger.info(f"Contract generated successfully ({len(contract_text)} chars)")

            return {
                "drafted_contract": contract_text
            }

        except Exception as e:
            logger.error(f"Error in drafting_agent: {e}", exc_info=True)
            raise

    def _build_system_prompt(self, template_style: Dict[str, Any]) -> str:
        """Build system prompt incorporating template style."""

        # Load base prompt from file if available
        prompt_path = Path(__file__).parent.parent / "llms" / "prompts" / "draft_prompt.txt"
        if prompt_path.exists():
            base_prompt = prompt_path.read_text(encoding="utf-8")
        else:
            base_prompt = "You are a legal contract generation assistant."

        # Add style guidance
        style_guidance = f"""

STYLE AND STRUCTURE REQUIREMENTS:

Headings: {', '.join(template_style.get('headings', ['Standard format']))}
Numbering: {template_style.get('numbering_format', 'hierarchical')}
Tone: {template_style.get('tone', 'formal legal')}

MUST INCLUDE THESE CLAUSES:
{self._format_clause_list(template_style.get('must_include_clauses', []))}

FORMATTING NOTES:
{self._format_notes(template_style.get('formatting_notes', []))}

IMPORTANT: If PDF templates are provided, carefully study their:
- Clause organization and sequencing
- Legal phrasing and terminology
- Formatting conventions
- Section structure
Then apply those patterns to generate a contract tailored to the user's specific requirements.
"""

        return base_prompt + style_guidance

    def _build_user_prompt(self, draft_request: Dict[str, Any], template_style: Dict[str, Any]) -> str:
        """Build user prompt with all contract requirements."""

        parties_list = "\n".join([f"- {p}" for p in draft_request.get("parties", [])])

        prompt = f"""Generate a {draft_request.get('agreement_type', 'legal agreement')} with the following details:

**PARTIES:**
{parties_list}

**JURISDICTION:** {draft_request.get('jurisdiction', 'United States')}

**PURPOSE:** {draft_request.get('purpose', 'General business agreement')}

**TERM:** {draft_request.get('term', '12 months')}

**EFFECTIVE DATE:** {draft_request.get('effective_date', 'Upon signing')}

**ADDITIONAL REQUIREMENTS:**
{draft_request.get('additional_requirements', 'None specified')}

---

Generate a complete, professional legal agreement that:
1. Follows the structure and style of any provided PDF templates
2. Includes all required clauses listed in the system prompt
3. Uses proper legal language and formatting
4. Addresses all user requirements above
5. Is ready for review by legal counsel

Output ONLY the final contract. Do NOT include explanations or commentary.
"""

        return prompt

    def _format_clause_list(self, clauses: List[str]) -> str:
        """Format clause list for prompt."""
        if not clauses:
            return "- Standard contract clauses"
        return "\n".join([f"- {clause}" for clause in clauses])

    def _format_notes(self, notes: List[str]) -> str:
        """Format formatting notes for prompt."""
        if not notes:
            return "- Use standard legal formatting"
        return "\n".join([f"- {note}" for note in notes])


# Singleton instance
agent = DraftingAgent()


async def run(agent_data: Dict[str, Any]) -> Dict[str, str]:
    """Convenience function to run drafting agent."""
    return await agent.run(agent_data)
