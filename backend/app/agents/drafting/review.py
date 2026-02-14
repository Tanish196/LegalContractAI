from app.agents.state import ContractState
from app.llms import get_llm_client
import logging
import json

logger = logging.getLogger(__name__)

class SelfReviewAgent:
    """Reviews the drafted contract for completeness and quality using LLM."""

    async def process(self, state: ContractState):
        logger.info("SelfReviewAgent: Reviewing draft via LLM")

        if not state.drafted_clauses:
            state.add_audit_log("SelfReview", "Skip", "No clauses to review")
            return

        # Assemble all clause texts for review
        full_draft = "\n\n".join([c.get("text", "") for c in state.drafted_clauses])

        # Don't review error clauses
        if len(state.drafted_clauses) == 1 and state.drafted_clauses[0].get("type") == "error":
            state.add_audit_log("SelfReview", "Skip", "Skipping review of error clause")
            return

        llm = get_llm_client()

        requirements_summary = state.raw_text[:800] if state.raw_text else "No specific requirements"
        key_reqs = state.metadata.get("key_requirements", [])
        suggested_clauses = state.metadata.get("suggested_clauses", [])

        prompt = f"""You are a senior legal reviewer. Review the following drafted contract for quality, completeness, and legal soundness.

**Original Requirements:**
{requirements_summary}

**Key Requirements Identified:**
{json.dumps(key_reqs) if key_reqs else "Not specified"}

**Suggested Clauses:**
{json.dumps(suggested_clauses) if suggested_clauses else "Not specified"}

**Jurisdiction:** {state.metadata.get('jurisdiction', 'Not specified')}

**Drafted Contract:**
{full_draft[:4000]}

Review for:
1. Are all user requirements addressed?
2. Are essential legal clauses present (terms, termination, governing law, liability)?
3. Is the language consistent and professional?
4. Are there any gaps or missing protections?
5. Is it appropriate for the specified jurisdiction?

Respond in valid JSON only (no markdown fences):
{{
  "overall_quality": "<excellent/good/needs_improvement/poor>",
  "completeness_score": <1-10>,
  "issues": ["<list of specific issues found, empty if none>"],
  "missing_clauses": ["<list of important clauses that are missing>"],
  "improvement_suggestions": ["<list of concrete suggestions to improve the draft>"]
}}"""

        try:
            response = await llm.generate(prompt, temperature=0.1, max_tokens=1500)

            clean = response.strip()
            if clean.startswith("```"):
                clean = clean.split("\n", 1)[1] if "\n" in clean else clean[3:]
            if clean.endswith("```"):
                clean = clean[:-3]
            clean = clean.strip()

            parsed = json.loads(clean)

            quality = parsed.get("overall_quality", "good")
            score = parsed.get("completeness_score", 7)
            issues = parsed.get("issues", [])
            missing = parsed.get("missing_clauses", [])
            suggestions = parsed.get("improvement_suggestions", [])

            # Add review metadata to each clause
            for clause in state.drafted_clauses:
                clause["review_quality"] = quality
                clause["review_score"] = score

            # Store review results in metadata for potential use
            state.metadata["review_quality"] = quality
            state.metadata["review_score"] = score
            state.metadata["review_issues"] = issues
            state.metadata["review_missing_clauses"] = missing
            state.metadata["review_suggestions"] = suggestions

            state.add_audit_log(
                "SelfReview", "Review",
                f"Quality: {quality}, Score: {score}/10, Issues: {len(issues)}, Missing: {len(missing)}"
            )
            logger.info(f"SelfReviewAgent: Quality={quality}, Score={score}/10")

        except json.JSONDecodeError:
            logger.warning("SelfReviewAgent: Could not parse LLM review response")
            for clause in state.drafted_clauses:
                clause["review_comment"] = "Review completed (response unparseable)"
            state.add_audit_log("SelfReview", "Fallback", "LLM response could not be parsed")

        except Exception as e:
            logger.error(f"SelfReviewAgent failed: {e}", exc_info=True)
            for clause in state.drafted_clauses:
                clause["review_comment"] = "Review skipped due to error"
            state.add_audit_log("SelfReview", "Error", f"Review failed: {str(e)}")
