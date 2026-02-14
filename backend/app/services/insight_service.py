"""LLM-backed report generation for UI tasks that are not full pipelines."""

from __future__ import annotations

import json
from typing import Any, Dict, Optional


from app.llms import get_llm_client

PROMPT_LIBRARY: Dict[str, Dict[str, Any]] = {
    "case-summary": {
        "goal": "Summarize the most material facts, issues, holdings, and implications of a legal case.",
        "sections": ["Case Snapshot", "Key Holdings", "Practical Implications", "Next Steps"],
    },
    "loophole-detection": {
        "goal": "Identify exploitable ambiguities or missing safeguards in the provided text.",
        "sections": ["Loophole Radar", "Impact Assessment", "Suggested Fix"],
    },
    "clause-classification": {
        "goal": "Group clauses by legal topic with short explanations for each grouping.",
        "sections": ["Clause Map", "Observations"],
    },
    "contract-drafting": {
        "goal": "Draft a baseline agreement structure when the full drafting pipeline is unavailable.",
        "sections": ["Agreement Overview", "Core Terms", "Signature Block"],
    },
    "compliance-check": {
        "goal": "Outline compliance issues when the full pipeline is not required.",
        "sections": ["Executive Summary", "Issues", "Recommended Actions"],
    },
}

BASE_INSTRUCTIONS = (
    "You are a senior legal analyst producing a client-ready deliverable. "
    "Return polished Markdown only (no JSON, no prefatory text). Always include a title, headings, "
    "subheadings, bullet points, and clear call-to-action items."
)


def _build_prompt(
    task_type: str,
    content: str,
    jurisdiction: Optional[str],
    metadata: Optional[Dict[str, Any]]
) -> str:
    config = PROMPT_LIBRARY.get(task_type) or {
        "goal": "Provide a structured legal analysis.",
        "sections": ["Summary", "Findings", "Recommended Actions"],
    }

    trimmed_content = content.strip()
    if len(trimmed_content) > 12000:
        trimmed_content = trimmed_content[:12000] + "\n...[truncated]"

    payload = json.dumps(
        {
            "task_type": task_type,
            "jurisdiction": jurisdiction,
            "goal": config["goal"],
            "sections": config["sections"],
            "metadata": metadata or {},
            "source_text": trimmed_content,
        },
        ensure_ascii=False
    )

    prompt = (
        f"{BASE_INSTRUCTIONS}\n"
        f"Task Focus: {config['goal']}\n"
        f"Required Sections: {', '.join(config['sections'])}\n"
        f"Jurisdiction Context: {jurisdiction or 'Not specified'}\n"
        "Style Guide: Limit paragraphs to 4 sentences, prefer bullet lists, highlight risk levels, "
        "and end with a concise Next Steps section.\n\n"
        f"DATA:\n{payload}\n\nRespond with Markdown only."
    )
    return prompt


async def generate_structured_report(
    task_type: str,
    content: str,
    jurisdiction: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    llm_client = get_llm_client()
    prompt = _build_prompt(task_type, content, jurisdiction, metadata)
    result = await llm_client.generate(prompt, temperature=0.25, max_tokens=2048)
    return result.strip()
