"""
Clause Agent - Contract Clause Extraction
Used in: Compliance Check Service

Purpose:
- Split contract text into individual clauses
- Remove empty or insignificant fragments
- Return structured list of clauses for analysis
"""

import logging
import re
from typing import Dict, List, Any

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ClauseAgent:
    """
    Extracts and segments clauses from contract text.
    Uses rule-based splitting logic.
    """

    MIN_CLAUSE_LENGTH = 20  # Minimum character count for valid clause
    MAX_CLAUSES = 200  # Safety limit to prevent memory issues

    def __init__(self):
        """Initialize the clause agent."""
        logger.info("ClauseAgent initialized")

    async def run(self, contract_text: str) -> Dict[str, Any]:
        """
        Main entry point for clause extraction.

        Args:
            contract_text: Full contract text to analyze

        Returns:
            Dictionary containing list of extracted clauses:
            {
                "clauses": ["clause 1", "clause 2", ...]
            }
        """
        try:
            logger.info("Starting clause extraction")

            if not contract_text or not isinstance(contract_text, str):
                logger.warning("Empty or invalid contract text provided")
                return {"clauses": []}

            # Preprocess the text
            cleaned_text = self._preprocess_text(contract_text)

            # Split into clauses using multiple strategies
            clauses = self._split_clauses(cleaned_text)

            # Filter and clean clauses
            clauses = self._filter_clauses(clauses)

            logger.info(f"Extracted {len(clauses)} valid clauses")

            return {"clauses": clauses}

        except Exception as e:
            logger.error(f"Error during clause extraction: {str(e)}", exc_info=True)
            raise

    def _preprocess_text(self, text: str) -> str:
        """
        Clean and prepare text for clause splitting.

        - Normalize line breaks
        - Remove excessive whitespace
        - Preserve paragraph structure
        """
        # Normalize line breaks
        text = text.replace('\r\n', '\n').replace('\r', '\n')

        # Remove multiple consecutive newlines (keep max 2)
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Remove leading/trailing whitespace from each line
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)

        return text.strip()

    def _split_clauses(self, text: str) -> List[str]:
        """
        Split contract text into clauses using multiple strategies.

        Strategies:
        1. Numbered sections (1., 2., etc.)
        2. Lettered sections (A., B., etc.)
        3. Paragraph breaks (double newlines)
        4. Section headers (SECTION, ARTICLE, etc.)
        5. Semicolon separation for list-style clauses
        """
        clauses = []

        # Strategy 1: Split by numbered sections (1., 2., 3., etc.)
        # Matches: "1.", "1.1", "2.3.4", etc.
        numbered_pattern = r'(?:^|\n)(\d+(?:\.\d+)*\.?\s+.+?)(?=(?:\n\d+(?:\.\d+)*\.?\s+)|$)'
        numbered_matches = re.finditer(numbered_pattern, text, re.MULTILINE | re.DOTALL)
        numbered_clauses = [match.group(1).strip() for match in numbered_matches]

        if len(numbered_clauses) > 3:
            # If we found substantial numbered sections, use those
            return numbered_clauses

        # Strategy 2: Split by lettered sections (A., B., C., etc.)
        lettered_pattern = r'(?:^|\n)([A-Z]\.?\s+.+?)(?=(?:\n[A-Z]\.?\s+)|$)'
        lettered_matches = re.finditer(lettered_pattern, text, re.MULTILINE | re.DOTALL)
        lettered_clauses = [match.group(1).strip() for match in lettered_matches]

        if len(lettered_clauses) > 3:
            return lettered_clauses

        # Strategy 3: Split by section keywords
        section_pattern = r'(?:^|\n)((?:SECTION|ARTICLE|CLAUSE|PARAGRAPH)\s+\d+[:.].+?)(?=(?:\n(?:SECTION|ARTICLE|CLAUSE|PARAGRAPH)\s+\d+[:])|$)'
        section_matches = re.finditer(section_pattern, text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        section_clauses = [match.group(1).strip() for match in section_matches]

        if len(section_clauses) > 2:
            return section_clauses

        # Strategy 4: Split by double line breaks (paragraphs)
        paragraph_clauses = [p.strip() for p in text.split('\n\n') if p.strip()]

        if len(paragraph_clauses) > 2:
            return paragraph_clauses

        # Strategy 5: Split by single line breaks if paragraphs didn't work
        line_clauses = [line.strip() for line in text.split('\n') if line.strip()]

        if len(line_clauses) > 1:
            # Merge very short consecutive lines (likely continuations)
            merged_clauses = []
            current_clause = ""

            for line in line_clauses:
                if len(line) < 60 and current_clause:
                    # Short line, append to current clause
                    current_clause += " " + line
                else:
                    # Start new clause
                    if current_clause:
                        merged_clauses.append(current_clause)
                    current_clause = line

            if current_clause:
                merged_clauses.append(current_clause)

            return merged_clauses

        # Fallback: Return whole text as single clause
        return [text] if text else []

    def _filter_clauses(self, clauses: List[str]) -> List[str]:
        """
        Filter out invalid or insignificant clauses.

        - Remove empty clauses
        - Remove very short clauses (< MIN_CLAUSE_LENGTH)
        - Remove header-only clauses
        - Limit total number of clauses
        """
        filtered = []

        for clause in clauses:
            # Skip empty
            if not clause or not clause.strip():
                continue

            # Skip very short clauses
            if len(clause) < self.MIN_CLAUSE_LENGTH:
                continue

            # Skip header-only lines (e.g., "SECTION 1" without content)
            if self._is_header_only(clause):
                continue

            # Skip repetitive boilerplate
            if self._is_boilerplate_noise(clause):
                continue

            filtered.append(clause.strip())

            # Safety limit
            if len(filtered) >= self.MAX_CLAUSES:
                logger.warning(f"Reached maximum clause limit ({self.MAX_CLAUSES})")
                break

        return filtered

    def _is_header_only(self, clause: str) -> bool:
        """
        Check if clause is just a header without substantive content.
        """
        # Very short text that's mostly uppercase
        if len(clause) < 30 and clause.upper() == clause:
            return True

        # Matches patterns like "SECTION 1", "ARTICLE II", etc. without more content
        header_pattern = r'^(?:SECTION|ARTICLE|CLAUSE|PARAGRAPH)\s+[IVXLCDM0-9]+\.?\s*$'
        if re.match(header_pattern, clause.strip(), re.IGNORECASE):
            return True

        return False

    def _is_boilerplate_noise(self, clause: str) -> bool:
        """
        Check if clause is common boilerplate noise to skip.
        """
        noise_patterns = [
            r'^page\s+\d+\s*$',  # "Page 1"
            r'^-+\s*$',  # Just dashes
            r'^_+\s*$',  # Just underscores
            r'^\*+\s*$',  # Just asterisks
            r'^={3,}\s*$',  # Just equals signs
        ]

        clause_lower = clause.lower().strip()

        for pattern in noise_patterns:
            if re.match(pattern, clause_lower, re.IGNORECASE):
                return True

        return False


# Singleton instance
agent = ClauseAgent()


async def run(contract_text: str) -> Dict[str, Any]:
    """
    Convenience function to run the clause agent.

    Args:
        contract_text: Full contract text

    Returns:
        Dictionary with extracted clauses
    """
    return await agent.run(contract_text)
