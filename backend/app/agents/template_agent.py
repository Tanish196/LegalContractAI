"""Template Agent - PDF Template Selection
Used in: Drafting Multi-Agent System

Purpose:
- Select appropriate PDF template(s) from pdf_templates/ based on agreement_type
- Create file objects for Gemini API
- Return selected template paths and metadata
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from app.config import PDF_TEMPLATE_DIR

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TemplateAgent:
    """Selects appropriate PDF templates based on agreement type."""

    # Template matching rules (agreement_type -> PDF filename patterns)
    TEMPLATE_MAPPINGS = {
        "nda": ["nda", "non-disclosure", "confidentiality"],
        "service agreement": ["service", "msa", "master service"],
        "employment": ["employment", "offer letter", "hire"],
        "purchase": ["purchase", "sale", "buy"],
        "lease": ["lease", "rental", "rent"],
        "partnership": ["partnership", "joint venture"],
        "licensing": ["license", "licensing"],
        "consulting": ["consulting", "consultant"],
    }

    def __init__(self, templates_dir: Optional[str] = None):
        """Initialize template agent."""
        self.templates_dir = Path(templates_dir) if templates_dir else PDF_TEMPLATE_DIR
        logger.info(f"TemplateAgent initialized with templates dir: {self.templates_dir}")

    async def run(self, draft_request: Dict[str, Any]) -> Dict[str, Any]:
        """Select PDF templates based on agreement type.

        Args:
            draft_request: Output from ingestion_agent containing normalized input

        Returns:
            {
                "draft_request": { ... },
                "selected_templates": [
                    {
                        "mime_type": "application/pdf",
                        "file_uri": "file:///absolute/path/to/template.pdf",
                        "filename": "nda_template.pdf"
                    }
                ]
            }
        """
        try:
            agreement_type = draft_request.get("agreement_type", "").lower()
            logger.info(f"Selecting templates for agreement type: {agreement_type}")

            # Find matching templates
            selected_templates = self._find_matching_templates(agreement_type)

            # If no matches, use all available PDFs
            if not selected_templates:
                logger.warning(f"No templates found for '{agreement_type}', using all available PDFs")
                selected_templates = self._get_all_templates()

            logger.info(f"Selected {len(selected_templates)} template(s)")

            return {
                "draft_request": draft_request,
                "selected_templates": selected_templates
            }

        except Exception as e:
            logger.error(f"Error in template_agent: {e}", exc_info=True)
            # Return draft_request with empty templates on error
            return {
                "draft_request": draft_request,
                "selected_templates": []
            }

    def _find_matching_templates(self, agreement_type: str) -> List[Dict[str, str]]:
        """Find PDF templates matching the agreement type."""
        templates = []

        if not self.templates_dir.exists():
            logger.warning(f"Templates directory does not exist: {self.templates_dir}")
            return templates

        # Get matching patterns for this agreement type
        patterns = []
        for key, keywords in self.TEMPLATE_MAPPINGS.items():
            if key in agreement_type or any(kw in agreement_type for kw in keywords):
                patterns.extend(keywords)

        # Search for PDFs matching any pattern
        for pdf_file in self.templates_dir.glob("*.pdf"):
            filename_lower = pdf_file.stem.lower()
            if any(pattern in filename_lower for pattern in patterns):
                templates.append(self._create_template_object(pdf_file))

        return templates

    def _get_all_templates(self) -> List[Dict[str, str]]:
        """Get all available PDF templates."""
        templates = []

        if not self.templates_dir.exists():
            return templates

        for pdf_file in self.templates_dir.glob("*.pdf"):
            templates.append(self._create_template_object(pdf_file))

        return templates

    def _create_template_object(self, pdf_path: Path) -> Dict[str, str]:
        """Create Gemini-compatible file object for PDF."""
        absolute_path = pdf_path.resolve()
        # Use forward slashes for file URI even on Windows
        file_uri = f"file:///{absolute_path.as_posix()}"

        return {
            "mime_type": "application/pdf",
            "file_uri": file_uri,
            "filename": pdf_path.name
        }


# Singleton instance
agent = TemplateAgent()


async def run(draft_request: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to run template agent."""
    return await agent.run(draft_request)
