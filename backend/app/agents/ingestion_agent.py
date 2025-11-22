"""
Ingestion Agent - Data Normalization and Extraction
Used in: Contract Drafting Service

Purpose:
- Extract and normalize contract metadata from raw input
- Apply defaults for missing fields
- Clean and validate data structure
"""

import logging
import re
from typing import Dict, List, Optional, Any

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class IngestionAgent:
    """
    Processes and normalizes contract input data.
    Extracts parties, jurisdiction, purpose, and term information.
    """

    DEFAULT_JURISDICTION = "United States"
    DEFAULT_PURPOSE = "General Agreement"
    DEFAULT_TERM = "12 months"

    def __init__(self):
        """Initialize the ingestion agent."""
        logger.info("IngestionAgent initialized")

    async def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for ingestion agent.

        Args:
            data: Raw input dictionary containing contract information

        Returns:
            Dictionary with normalized data:
            {
                "draft_request": {
                    "parties": [...],
                    "jurisdiction": "...",
                    "agreement_type": "...",
                    "purpose": "...",
                    "term": "...",
                    "effective_date": "...",
                    "additional_requirements": "..."
                }
            }
            OR for legacy compliance flow:
            {
                "meta": {
                    "parties": [...],
                    "jurisdiction": "...",
                    "purpose": "...",
                    "term": "..."
                }
            }
        """
        try:
            logger.info("Starting ingestion process")

            # Extract and normalize parties
            parties = self._extract_parties(data)

            # Extract or apply default jurisdiction
            jurisdiction = self._extract_jurisdiction(data)

            # Extract or apply default purpose / agreement_type
            purpose = self._extract_purpose(data)
            agreement_type = data.get("agreement_type") or data.get("contract_type") or purpose

            # Extract or apply default term
            term = self._extract_term(data)

            # Extract effective date
            effective_date = data.get("effective_date") or "Upon signing"

            # Extract additional requirements
            additional_requirements = data.get("additional_requirements") or data.get("requirements") or data.get("key_terms") or ""
            if data.get("key_terms") and data.get("requirements"):
                additional_requirements = f"{data.get('requirements')}\n\nKey Terms:\n{data.get('key_terms')}"

            # Extract party names as simple list
            party_names = [p.get("name") if isinstance(p, dict) else str(p) for p in parties]

            # Build normalized data - support both formats
            result = {
                # New format for drafting pipeline
                "draft_request": {
                    "parties": party_names,
                    "jurisdiction": jurisdiction,
                    "agreement_type": agreement_type,
                    "purpose": purpose,
                    "term": term,
                    "effective_date": effective_date,
                    "additional_requirements": additional_requirements
                },
                # Legacy format for compliance pipeline
                "meta": {
                    "parties": parties,
                    "jurisdiction": jurisdiction,
                    "purpose": purpose,
                    "term": term
                }
            }

            logger.info(f"Ingestion completed successfully: {len(parties)} parties found, type={agreement_type}")
            return result

        except Exception as e:
            logger.error(f"Error during ingestion: {str(e)}", exc_info=True)
            raise

    def _extract_parties(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Extract party information from input data.

        Supports multiple input formats:
        - parties: [{"name": "...", "role": "..."}, ...]
        - party_a, party_b: separate fields
        - parties: ["name1", "name2"]

        Returns:
            List of party dictionaries with name and role
        """
        parties = []

        # Check for structured parties list
        if "parties" in data and isinstance(data["parties"], list):
            for party in data["parties"]:
                if isinstance(party, dict):
                    parties.append({
                        "name": self._clean_text(party.get("name", "")),
                        "role": self._clean_text(party.get("role", "Party"))
                    })
                elif isinstance(party, str):
                    parties.append({
                        "name": self._clean_text(party),
                        "role": "Party"
                    })

        # Check for separate party_a and party_b fields
        if "party_a" in data or "party-a" in data:
            party_a_name = self._clean_text(
                data.get("party_a") or data.get("party-a", "")
            )
            if party_a_name:
                parties.append({
                    "name": party_a_name,
                    "role": "Party A"
                })

        if "party_b" in data or "party-b" in data:
            party_b_name = self._clean_text(
                data.get("party_b") or data.get("party-b", "")
            )
            if party_b_name:
                parties.append({
                    "name": party_b_name,
                    "role": "Party B"
                })

        # If no parties found, create placeholder parties
        if not parties:
            logger.warning("No parties found in input data, using defaults")
            parties = [
                {"name": "Party A", "role": "First Party"},
                {"name": "Party B", "role": "Second Party"}
            ]

        return parties

    def _extract_jurisdiction(self, data: Dict[str, Any]) -> str:
        """
        Extract jurisdiction from input data.

        Checks multiple possible field names and applies defaults.
        """
        jurisdiction = (
            data.get("jurisdiction") or
            data.get("jurisdiction_code") or
            data.get("region") or
            self.DEFAULT_JURISDICTION
        )

        return self._normalize_jurisdiction(self._clean_text(str(jurisdiction)))

    def _normalize_jurisdiction(self, jurisdiction: str) -> str:
        """
        Normalize jurisdiction codes to full names.
        """
        jurisdiction_map = {
            "us": "United States",
            "usa": "United States",
            "uk": "United Kingdom",
            "eu": "European Union",
            "ca": "Canada",
            "au": "Australia",
            "in": "India",
            "de": "Germany",
            "fr": "France",
        }

        jurisdiction_lower = jurisdiction.lower().strip()
        return jurisdiction_map.get(jurisdiction_lower, jurisdiction)

    def _extract_purpose(self, data: Dict[str, Any]) -> str:
        """
        Extract contract purpose/type from input data.
        """
        # Check various possible field names
        purpose = (
            data.get("purpose") or
            data.get("contract_type") or
            data.get("contract-type") or
            data.get("type") or
            data.get("description") or
            self.DEFAULT_PURPOSE
        )

        return self._clean_text(str(purpose))

    def _extract_term(self, data: Dict[str, Any]) -> str:
        """
        Extract contract term/duration from input data.
        """
        # Check various possible field names
        term = (
            data.get("term") or
            data.get("duration") or
            data.get("period") or
            data.get("term_length") or
            self.DEFAULT_TERM
        )

        return self._normalize_term(self._clean_text(str(term)))

    def _normalize_term(self, term: str) -> str:
        """
        Normalize term format to be human-readable.
        """
        # Handle numeric-only input (assume months)
        if term.isdigit():
            months = int(term)
            if months == 12:
                return "1 year"
            elif months == 24:
                return "2 years"
            elif months == 36:
                return "3 years"
            else:
                return f"{months} months"

        # Return as-is if already descriptive
        return term

    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text input.

        - Strip whitespace
        - Remove excessive spaces
        - Remove special characters that might cause issues
        """
        if not text:
            return ""

        # Strip whitespace
        text = text.strip()

        # Normalize multiple spaces to single space
        text = re.sub(r'\s+', ' ', text)

        return text


# Singleton instance for easy import
agent = IngestionAgent()


async def run(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to run the ingestion agent.

    Args:
        data: Raw input dictionary

    Returns:
        Normalized metadata dictionary
    """
    return await agent.run(data)
