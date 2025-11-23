"""Compliance Service - Multi-Agent Pipeline with RAG-backed analysis."""

import json
import logging
from typing import Dict, Any, List, Optional

from app.agents import clause_agent, compliance_agent, risk_agent
from app.llms import get_gemini_client

logger = logging.getLogger(__name__)

async def check_compliance(contract_text: str, jurisdiction: str = "United States") -> Dict[str, Any]:
    """Run the complete compliance checking multi-agent pipeline.

    Args:
        contract_text: Full contract text to analyze
        jurisdiction: Legal jurisdiction for compliance

    Returns:
        {
            "drafted_contract": null,
            "compliance_report": [...]
        }
    """
    try:
        logger.info("=" * 60)
        logger.info("COMPLIANCE PIPELINE - Starting multi-agent flow")
        logger.info("=" * 60)

        # Step 1: clause_agent - Split contract into clauses
        logger.info("Step 1/3: Running clause_agent...")
        clause_result = await clause_agent.run(contract_text)
        clauses = clause_result.get("clauses", [])
        logger.info(f"✓ Clause extraction complete - {len(clauses)} clause(s) found")

        if not clauses:
            logger.warning("No clauses extracted from contract")
            return {
                "drafted_contract": None,
                "compliance_report": []
            }

        # Get LLM client for compliance analysis
        llm_client = get_gemini_client()

        compliance_report: List[Dict[str, Any]] = []
        suggested_language: List[Dict[str, str]] = []

        # Step 2-3: For each clause, run compliance_agent → risk_agent
        for i, clause in enumerate(clauses, 1):
            logger.info(f"Processing clause {i}/{len(clauses)}")

            # Step 2: compliance_agent - RAG-backed analysis
            logger.info("  Step 2: Running compliance_agent (RAG-backed)...")
            compliance_result = await compliance_agent.run(
                clause=clause,
                jurisdiction=jurisdiction,
                llm_client=llm_client
            )

            parsed = compliance_result.get("parsed", {})
            rag_context = compliance_result.get("rag_context") or {}
            rag_draft = rag_context.get("drafted_contract")

            # Step 3: risk_agent - Classify risk level
            logger.info(f"  Step 3: Running risk_agent...")
            risk_result = await risk_agent.run(parsed)

            if rag_draft:
                suggested_language.append({
                    "clause_index": i,
                    "title": _derive_issue_title(clause, parsed.get("issue_summary")),
                    "text": rag_draft.strip()
                })

            # Build compliance issue
            issue = {
                "clause": clause[:200] + "..." if len(clause) > 200 else clause,
                "heading": _derive_issue_title(clause, parsed.get("issue_summary")),
                "risk_level": risk_result.get("risk_level", "medium"),
                "fix": risk_result.get("fix", "Review clause for compliance"),
                "citations": risk_result.get("citations", ["RAG_Context"]),
                "issue_summary": parsed.get("issue_summary"),
                "missing_requirements": parsed.get("missing_requirements", []),
                "recommended_actions": _extract_action_items(
                    risk_result.get("fix"),
                    parsed.get("missing_requirements", [])
                ),
                "regulation": _extract_regulation(parsed.get("rag_findings")),
                "reference": _extract_reference(parsed.get("rag_findings"))
            }

            compliance_report.append(issue)
            logger.info(f"  ✓ Clause {i} analyzed - Risk: {issue['risk_level']}")

        logger.info("=" * 60)
        logger.info(f"COMPLIANCE PIPELINE - Complete - {len(compliance_report)} issues found")
        logger.info("=" * 60)

        summary = _build_summary(compliance_report)
        insights = _build_insights(summary, compliance_report, suggested_language)
        report_markdown = await _generate_markdown_report(
            llm_client=llm_client,
            contract_text=contract_text,
            jurisdiction=jurisdiction,
            compliance_report=compliance_report,
            summary=summary,
            insights=insights
        )

        return {
            "drafted_contract": contract_text,
            "compliance_report": compliance_report,
            "summary": summary,
            "insights": insights,
            "report_markdown": report_markdown
        }

    except Exception as e:
        logger.error(f"Error in compliance pipeline: {e}", exc_info=True)
        raise


def _derive_issue_title(clause: str, issue_summary: Optional[str]) -> str:
    if issue_summary:
        return issue_summary.split(".")[0][:120]
    clause_clean = clause.strip().split("\n", 1)[0]
    return clause_clean[:120] or "Clause Review"


def _extract_action_items(fix_text: Optional[str], missing_requirements: List[str]) -> List[str]:
    actions: List[str] = []
    if missing_requirements:
        actions.extend(missing_requirements)
    if fix_text:
        segments = [seg.strip(" -") for seg in fix_text.split("\n") if seg.strip()]
        for segment in segments:
            if segment and segment not in actions:
                actions.append(segment)
    return actions[:5]


def _extract_regulation(rag_findings: Any) -> Optional[str]:
    if not rag_findings:
        return None
    first = rag_findings[0]
    return first.get("regulation") if isinstance(first, dict) else None


def _extract_reference(rag_findings: Any) -> Optional[str]:
    if not rag_findings:
        return None
    first = rag_findings[0]
    return first.get("reference") if isinstance(first, dict) else None


def _build_summary(compliance_report: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(compliance_report)
    high = sum(1 for issue in compliance_report if issue.get("risk_level") == "high")
    medium = sum(1 for issue in compliance_report if issue.get("risk_level") == "medium")
    low = sum(1 for issue in compliance_report if issue.get("risk_level") == "low")

    if high:
        overall = "CRITICAL"
    elif medium:
        overall = "REVIEW NEEDED"
    else:
        overall = "ACCEPTABLE"

    return {
        "total_clauses": total,
        "high_risk": high,
        "medium_risk": medium,
        "low_risk": low,
        "overall_assessment": overall
    }


def _build_insights(
    summary: Dict[str, Any],
    compliance_report: List[Dict[str, Any]],
    suggested_language: List[Dict[str, str]]
) -> Dict[str, Any]:
    executive_summary = (
        f"{summary['total_clauses']} clause(s) reviewed. "
        f"High risk: {summary['high_risk']}, Medium risk: {summary['medium_risk']}, Low risk: {summary['low_risk']}. "
        f"Overall assessment: {summary['overall_assessment']}."
    )

    prioritized_actions = []
    for issue in compliance_report:
        if issue.get("risk_level") == "low":
            continue
        prioritized_actions.append({
            "title": issue.get("heading") or "Clause Review",
            "risk_level": issue.get("risk_level"),
            "actions": issue.get("recommended_actions", []),
            "citations": issue.get("citations", [])
        })

    return {
        "executive_summary": executive_summary,
        "action_items": prioritized_actions[:10],
        "suggested_language": suggested_language
    }


async def _generate_markdown_report(
    llm_client,
    contract_text: str,
    jurisdiction: str,
    compliance_report: List[Dict[str, Any]],
    summary: Dict[str, Any],
    insights: Dict[str, Any]
) -> str:
    instructions = (
        "You are a senior legal analyst preparing a client-ready compliance memorandum. "
        "Produce polished Markdown with the following sections in order:\n"
        "# Compliance Review Report\n"
        "## Executive Summary\n"
        "## Risk Radar (table with Clause / Risk Level / Action)\n"
        "## Detailed Findings (one subsection per clause with headings, bullet points, citations)\n"
        "## Action Checklist (bullets grouped by priority)\n"
        "## Suggested Language Updates (quote blocks)."
        "Keep tone concise, avoid hedging, and cite governing sources when available."
    )

    payload = json.dumps(
        {
            "jurisdiction": jurisdiction,
            "summary": summary,
            "insights": insights,
            "issues": compliance_report,
            "contract_excerpt": contract_text[:2000]
        },
        ensure_ascii=False
    )

    prompt = f"{instructions}\n\nDATA:\n{payload}\n\nRespond with Markdown only."

    try:
        report = await llm_client.generate(prompt, temperature=0.2, max_tokens=2048)
        return report.strip()
    except Exception as exc:
        logger.warning("Failed to generate Markdown report via LLM: %s", exc)
        return _fallback_markdown(summary, compliance_report, insights, jurisdiction)


def _fallback_markdown(
    summary: Dict[str, Any],
    compliance_report: List[Dict[str, Any]],
    insights: Dict[str, Any],
    jurisdiction: str
) -> str:
    lines = ["# Compliance Review Report", f"_Jurisdiction: {jurisdiction}_", "", "## Executive Summary", insights.get("executive_summary", "")]

    lines.append("\n## Risk Radar")
    lines.append("| Clause | Risk | Primary Action |")
    lines.append("| --- | --- | --- |")
    for issue in compliance_report:
        lines.append(
            f"| {issue.get('heading', 'Clause')} | {issue.get('risk_level')} | {issue.get('recommended_actions', ['Review clause'])[0]} |"
        )

    lines.append("\n## Detailed Findings")
    for issue in compliance_report:
        lines.extend([
            f"### {issue.get('heading', 'Clause Review')}",
            f"- **Risk Level:** {issue.get('risk_level')}",
            f"- **Summary:** {issue.get('issue_summary') or 'Refer to clause details.'}",
            f"- **Recommended Fix:** {issue.get('fix')}",
            f"- **Citations:** {', '.join(issue.get('citations', [])) or 'N/A'}",
            ""
        ])

    lines.append("## Action Checklist")
    for action in insights.get("action_items", []):
        lines.append(f"- **{action['risk_level'].upper()}** — {action['title']}: {action['actions'][0] if action['actions'] else 'Review clause.'}")

    if insights.get("suggested_language"):
        lines.append("\n## Suggested Language Updates")
        for suggestion in insights["suggested_language"]:
            lines.append(f"### {suggestion.get('title', 'Clause Update')}")
            lines.append(f"> {suggestion.get('text')}")

    return "\n".join(lines)
