"""
Merge Agent - Clause Enhancement with Risk Fixes
Used in: Compliance Check Service (Optional)

Purpose:
- Accept original clause + risk assessment
- If risk is low, return unchanged
- If risk is medium/high, append fix requirements
- Return merged clause text
"""

import logging
from typing import Dict, Any

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MergeAgent:
    """
    Merges original clause with compliance fix recommendations.
    Conditionally enhances clauses based on risk level.
    """

    def __init__(self):
        """Initialize the merge agent."""
        logger.info("MergeAgent initialized")

    async def run(self, clause: str, risk_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for clause merging.

        Args:
            clause: Original contract clause text
            risk_output: Risk assessment from risk_agent
                Expected structure:
                {
                    "risk_level": "low|medium|high",
                    "fix": "...",
                    "citations": [...]
                }

        Returns:
            Dictionary containing:
            {
                "merged_clause": "Enhanced or original clause text"
            }
        """
        try:
            logger.info("Starting clause merge process")

            # Extract risk level
            risk_level = risk_output.get("risk_level", "medium").lower()

            # If low risk, return unchanged
            if risk_level == "low":
                logger.info("Low risk detected, returning original clause unchanged")
                return {"merged_clause": clause}

            # For medium/high risk, append fix section
            logger.info(f"{risk_level.upper()} risk detected, appending fix requirements")
            merged_clause = self._append_fix_section(
                clause,
                risk_level,
                risk_output.get("fix", ""),
                risk_output.get("citations", [])
            )

            return {"merged_clause": merged_clause}

        except Exception as e:
            logger.error(f"Error during clause merge: {str(e)}", exc_info=True)
            # Return original clause on error
            return {"merged_clause": clause}

    def _append_fix_section(
        self,
        clause: str,
        risk_level: str,
        fix: str,
        citations: list
    ) -> str:
        """
        Append compliance fix section to clause.

        Args:
            clause: Original clause text
            risk_level: Risk level (medium/high)
            fix: Fix recommendation text
            citations: Legal citations

        Returns:
            Enhanced clause with fix section
        """
        # Build fix section
        separator = "\n\n" + "=" * 60 + "\n"

        fix_header = self._get_fix_header(risk_level)

        fix_section = f"{separator}{fix_header}\n\n"

        # Add fix details
        if fix:
            fix_section += f"**Recommended Modifications:**\n{fix}\n\n"

        # Add citations if available
        if citations:
            fix_section += "**Legal References:**\n"
            for i, citation in enumerate(citations, 1):
                fix_section += f"{i}. {citation}\n"
            fix_section += "\n"

        # Add guidance
        fix_section += "**Action Required:**\n"
        if risk_level == "high":
            fix_section += "This clause requires immediate revision before execution. Consult with legal counsel to ensure compliance.\n"
        else:  # medium
            fix_section += "Consider revising this clause to address the identified concerns. Legal review is recommended.\n"

        fix_section += separator

        # Combine original clause with fix section
        merged = f"{clause.strip()}{fix_section}"

        return merged

    def _get_fix_header(self, risk_level: str) -> str:
        """
        Get appropriate header based on risk level.
        """
        if risk_level == "high":
            return "⚠️ COMPLIANCE FIX REQUIRED - HIGH RISK ⚠️"
        elif risk_level == "medium":
            return "⚡ COMPLIANCE REVIEW RECOMMENDED - MEDIUM RISK"
        else:
            return "ℹ️ COMPLIANCE NOTE"

    async def merge_multiple_clauses(
        self,
        clauses_with_risks: list[tuple[str, Dict[str, Any]]]
    ) -> str:
        """
        Merge multiple clauses with their risk assessments.

        Args:
            clauses_with_risks: List of (clause, risk_output) tuples

        Returns:
            Complete merged document
        """
        merged_sections = []

        for i, (clause, risk_output) in enumerate(clauses_with_risks, 1):
            # Create section header
            section_header = f"\n\n{'=' * 60}\nCLAUSE {i}\n{'=' * 60}\n\n"

            # Merge clause
            result = await self.run(clause, risk_output)
            merged_clause = result["merged_clause"]

            # Combine
            merged_sections.append(f"{section_header}{merged_clause}")

        return "\n".join(merged_sections)

    def create_executive_summary(
        self,
        clauses_with_risks: list[tuple[str, Dict[str, Any]]]
    ) -> str:
        """
        Create executive summary of all compliance findings.

        Args:
            clauses_with_risks: List of (clause, risk_output) tuples

        Returns:
            Executive summary text
        """
        high_risk_count = 0
        medium_risk_count = 0
        low_risk_count = 0

        for _, risk_output in clauses_with_risks:
            risk_level = risk_output.get("risk_level", "medium").lower()
            if risk_level == "high":
                high_risk_count += 1
            elif risk_level == "medium":
                medium_risk_count += 1
            else:
                low_risk_count += 1

        summary = f"""
COMPLIANCE EXECUTIVE SUMMARY
{'=' * 60}

Total Clauses Analyzed: {len(clauses_with_risks)}

Risk Distribution:
  ⚠️  HIGH Risk:    {high_risk_count} clause(s)
  ⚡ MEDIUM Risk:  {medium_risk_count} clause(s)
  ✓  LOW Risk:     {low_risk_count} clause(s)

"""

        if high_risk_count > 0:
            summary += "⚠️ IMMEDIATE ACTION REQUIRED\n"
            summary += f"   {high_risk_count} clause(s) identified with high compliance risk.\n"
            summary += "   Review and revision strongly recommended before contract execution.\n\n"

        if medium_risk_count > 0:
            summary += "⚡ REVIEW RECOMMENDED\n"
            summary += f"   {medium_risk_count} clause(s) identified with medium compliance risk.\n"
            summary += "   Consider modifications to strengthen compliance.\n\n"

        if high_risk_count == 0 and medium_risk_count == 0:
            summary += "✓ OVERALL ASSESSMENT: ACCEPTABLE\n"
            summary += "   No significant compliance issues identified.\n"
            summary += "   Standard legal review still recommended.\n\n"

        summary += f"{'=' * 60}\n"

        return summary


# Singleton instance
agent = MergeAgent()


async def run(clause: str, risk_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to run the merge agent.

    Args:
        clause: Original clause text
        risk_output: Risk assessment results

    Returns:
        Merged clause results
    """
    return await agent.run(clause, risk_output)
