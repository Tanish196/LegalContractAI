"""
Risk Agent - Risk Level Classification and Fix Generation
Used in: Compliance Check Service

Purpose:
- Accept parsed LLM compliance analysis
- Determine final risk level using JSON + heuristic fallback
- Extract fix recommendations
- Return structured risk assessment
"""

import logging
from typing import Dict, List, Any

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class RiskAgent:
    """
    Classifies risk levels and extracts actionable fixes.
    Uses parsed JSON from compliance agent with heuristic fallback.
    """

    # Valid risk levels
    RISK_LEVELS = ["low", "medium", "high"]

    def __init__(self):
        """Initialize the risk agent."""
        logger.info("RiskAgent initialized")

    async def run(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for risk assessment.

        Args:
            parsed: Parsed compliance analysis from compliance_agent
                Expected structure:
                {
                    "issue_summary": "...",
                    "risk_level": "low|medium|high",
                    "missing_requirements": [...],
                    "suggested_fix": "...",
                    "citations": [...]
                }

        Returns:
            Dictionary containing:
            {
                "risk_level": "low|medium|high",
                "fix": "Suggested fix text",
                "citations": [...]
            }
        """
        try:
            logger.info("Starting risk assessment")

            # Extract risk level
            risk_level = self._determine_risk_level(parsed)

            # Extract fix recommendation
            fix = self._extract_fix(parsed)

            # Extract citations
            citations = self._extract_citations(parsed)

            result = {
                "risk_level": risk_level,
                "fix": fix,
                "citations": citations
            }

            logger.info(f"Risk assessment completed: {risk_level} risk level")
            return result

        except Exception as e:
            logger.error(f"Error during risk assessment: {str(e)}", exc_info=True)
            raise

    def _determine_risk_level(self, parsed: Dict[str, Any]) -> str:
        """
        Determine risk level from parsed compliance data.

        Priority:
        1. Use explicit risk_level field if valid
        2. Apply heuristic based on issue_summary and missing_requirements
        3. Default to medium
        """
        # Try to get explicit risk level
        if "risk_level" in parsed:
            risk_level = str(parsed["risk_level"]).lower().strip()
            if risk_level in self.RISK_LEVELS:
                logger.info(f"Using explicit risk level: {risk_level}")
                return risk_level

        # Fallback: Apply heuristics
        logger.info("Using heuristic risk level determination")
        return self._heuristic_risk_level(parsed)

    def _heuristic_risk_level(self, parsed: Dict[str, Any]) -> str:
        """
        Determine risk level using heuristic analysis.

        Rules:
        - HIGH: Contains "high", "critical", "violation", "illegal", "non-compliant", "breach"
               OR 3+ missing requirements
        - MEDIUM: Contains "medium", "concern", "missing", "should", "may"
                 OR 1-2 missing requirements
        - LOW: Default or positive indicators
        """
        # Combine all text fields for analysis
        text_fields = []

        if "issue_summary" in parsed:
            text_fields.append(str(parsed["issue_summary"]))

        if "suggested_fix" in parsed:
            text_fields.append(str(parsed["suggested_fix"]))

        combined_text = " ".join(text_fields).lower()

        # Count missing requirements
        missing_count = 0
        if "missing_requirements" in parsed and isinstance(parsed["missing_requirements"], list):
            missing_count = len(parsed["missing_requirements"])

        # HIGH risk indicators
        high_indicators = [
            'high', 'high risk', 'critical', 'severe', 'violation',
            'illegal', 'non-compliant', 'non compliant', 'breach',
            'mandatory', 'required', 'must be', 'fails to'
        ]

        for indicator in high_indicators:
            if indicator in combined_text:
                logger.info(f"HIGH risk detected via indicator: {indicator}")
                return "high"

        # Check missing requirements count
        if missing_count >= 3:
            logger.info(f"HIGH risk detected via missing requirements: {missing_count}")
            return "high"

        # MEDIUM risk indicators
        medium_indicators = [
            'medium', 'medium risk', 'concern', 'concerns', 'missing',
            'should', 'may', 'consider', 'recommend', 'suggested',
            'advisable', 'improve', 'enhance', 'unclear'
        ]

        for indicator in medium_indicators:
            if indicator in combined_text:
                logger.info(f"MEDIUM risk detected via indicator: {indicator}")
                return "medium"

        # Check missing requirements count
        if missing_count > 0:
            logger.info(f"MEDIUM risk detected via missing requirements: {missing_count}")
            return "medium"

        # LOW risk indicators (positive)
        low_indicators = [
            'compliant', 'acceptable', 'adequate', 'satisfactory',
            'meets requirements', 'no issues', 'low risk', 'minimal'
        ]

        for indicator in low_indicators:
            if indicator in combined_text:
                logger.info(f"LOW risk detected via indicator: {indicator}")
                return "low"

        # Default to low if no strong indicators
        logger.info("No strong risk indicators found, defaulting to LOW")
        return "low"

    def _extract_fix(self, parsed: Dict[str, Any]) -> str:
        """
        Extract fix recommendation from parsed data.
        """
        # Try explicit suggested_fix field
        if "suggested_fix" in parsed and parsed["suggested_fix"]:
            fix = str(parsed["suggested_fix"]).strip()
            if fix and fix.lower() != "none":
                return fix

        # Build fix from missing requirements
        if "missing_requirements" in parsed and parsed["missing_requirements"]:
            requirements = parsed["missing_requirements"]
            if isinstance(requirements, list) and requirements:
                fix_parts = ["The following requirements should be addressed:"]
                for i, req in enumerate(requirements, 1):
                    fix_parts.append(f"{i}. {req}")
                return "\n".join(fix_parts)

        # Use issue summary as fix basis
        if "issue_summary" in parsed and parsed["issue_summary"]:
            return f"Review and address: {parsed['issue_summary']}"

        # Default fallback
        return "No specific fix recommended. Consider review by legal counsel."

    def _extract_citations(self, parsed: Dict[str, Any]) -> List[str]:
        """
        Extract legal citations from parsed data.
        """
        citations = []

        if "citations" in parsed:
            if isinstance(parsed["citations"], list):
                citations = [str(c) for c in parsed["citations"] if c]
            elif isinstance(parsed["citations"], str):
                citations = [parsed["citations"]]

        # Remove duplicates while preserving order
        seen = set()
        unique_citations = []
        for citation in citations:
            if citation not in seen:
                seen.add(citation)
                unique_citations.append(citation)

        return unique_citations

    def generate_risk_summary(self, risk_level: str, fix: str) -> str:
        """
        Generate human-readable risk summary.

        Args:
            risk_level: Risk level (low/medium/high)
            fix: Fix recommendation

        Returns:
            Formatted risk summary text
        """
        risk_descriptions = {
            "high": "⚠️ HIGH RISK - Immediate attention required",
            "medium": "⚡ MEDIUM RISK - Review and consider modifications",
            "low": "✓ LOW RISK - Generally acceptable"
        }

        description = risk_descriptions.get(risk_level, "UNKNOWN RISK")

        summary = f"{description}\n\n"

        if fix:
            summary += f"Recommended Action:\n{fix}"

        return summary


# Singleton instance
agent = RiskAgent()


async def run(parsed: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to run the risk agent.

    Args:
        parsed: Parsed compliance analysis

    Returns:
        Risk assessment results
    """
    return await agent.run(parsed)
