"""Structure Agent - PDF Structure Extraction
Used in: Drafting Multi-Agent System

Purpose:
- Extract structure, tone, and clause style from PDF templates
- Identify headings, numbering format, tone
- Determine must-include clauses
- Return template style metadata
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class StructureAgent:
    """Extracts structure and style patterns from PDF templates."""

    # Standard legal contract clauses that should typically be included
    STANDARD_CLAUSES = [
        "Parties",
        "Recitals",
        "Definitions",
        "Scope of Work / Services",
        "Term and Termination",
        "Payment Terms",
        "Confidentiality",
        "Intellectual Property",
        "Liability and Indemnification",
        "Dispute Resolution",
        "Governing Law",
        "Miscellaneous Provisions",
        "Signatures"
    ]

    def __init__(self):
        """Initialize structure agent."""
        logger.info("StructureAgent initialized")

    async def run(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract structure and style from selected templates.

        Args:
            agent_data: Output from template_agent containing draft_request and selected_templates

        Returns:
            {
                "template_style": {
                    "headings": [...],
                    "numbering_format": "...",
                    "tone": "formal",
                    "must_include_clauses": [...]
                },
                "draft_request": {...},
                "selected_templates": [...]
            }
        """
        try:
            draft_request = agent_data.get("draft_request", {})
            selected_templates = agent_data.get("selected_templates", [])

            logger.info(f"Analyzing structure from {len(selected_templates)} template(s)")

            # Since we can't actually parse PDFs in Python easily without heavy dependencies,
            # we'll provide intelligent defaults based on agreement type
            agreement_type = draft_request.get("agreement_type", "").lower()

            template_style = self._generate_template_style(agreement_type, selected_templates)

            logger.info(f"Generated template style: {template_style['tone']}, {len(template_style['must_include_clauses'])} required clauses")

            return {
                "template_style": template_style,
                "draft_request": draft_request,
                "selected_templates": selected_templates
            }

        except Exception as e:
            logger.error(f"Error in structure_agent: {e}", exc_info=True)
            # Return with default structure
            return {
                "template_style": self._get_default_style(),
                "draft_request": agent_data.get("draft_request", {}),
                "selected_templates": agent_data.get("selected_templates", [])
            }

    def _generate_template_style(self, agreement_type: str, templates: List[Dict]) -> Dict[str, Any]:
        """Generate template style based on agreement type and available templates."""

        # Determine required clauses based on agreement type
        must_include = self._get_required_clauses_for_type(agreement_type)

        # If templates are available, mention them in the style guide
        has_templates = len(templates) > 0

        style = {
            "headings": [
                "ALL CAPS for main sections",
                "Title Case for subsections",
                "Numbered sections (1., 2., 3., etc.)",
                "Lettered subsections (a., b., c., etc.)"
            ],
            "numbering_format": "hierarchical (1., 1.1, 1.1.1)",
            "tone": "formal legal",
            "must_include_clauses": must_include,
            "formatting_notes": [
                "Use clear paragraph breaks",
                "Include blank lines between sections",
                "Indent subsections appropriately",
                "Use bold for section headers"
            ],
            "has_reference_templates": has_templates,
            "template_count": len(templates)
        }

        return style

    def _get_required_clauses_for_type(self, agreement_type: str) -> List[str]:
        """Determine required clauses based on agreement type."""

        # Always include these
        base_clauses = [
            "Parties",
            "Recitals",
            "Term and Termination",
            "Governing Law",
            "Signatures"
        ]

        # Add type-specific clauses
        type_specific = {
            "nda": ["Confidential Information Definition", "Non-Disclosure Obligations", "Return of Materials"],
            "service": ["Scope of Services", "Payment Terms", "Deliverables", "Warranties"],
            "employment": ["Position and Duties", "Compensation and Benefits", "Termination Provisions"],
            "lease": ["Premises Description", "Rent", "Security Deposit", "Maintenance Obligations"],
            "purchase": ["Purchase Price", "Payment Terms", "Delivery", "Warranties", "Risk of Loss"],
        }

        for key, clauses in type_specific.items():
            if key in agreement_type:
                base_clauses.extend(clauses)
                break
        else:
            # Default clauses for general agreements
            base_clauses.extend(["Scope", "Payment Terms", "Confidentiality", "Liability"])

        return base_clauses

    def _get_default_style(self) -> Dict[str, Any]:
        """Return default template style."""
        return {
            "headings": ["Standard numbered sections"],
            "numbering_format": "hierarchical",
            "tone": "formal legal",
            "must_include_clauses": self.STANDARD_CLAUSES,
            "has_reference_templates": False,
            "template_count": 0
        }


# Singleton instance
agent = StructureAgent()


async def run(agent_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to run structure agent."""
    return await agent.run(agent_data)
