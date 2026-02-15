
from app.agents.state import ContractState
from app.llms import get_llm_client
import logging

import json

logger = logging.getLogger(__name__)

class ComplianceReasoningAgent:
    async def process(self, state: ContractState):
        logger.info("ComplianceReasoningAgent: Analyzing compliance")
        
        # This is the "Thinking" agent
        # Compare state.clauses with state.retrieved_statutes
        
        provider = state.metadata.get("provider", "google")
        llm = get_llm_client(provider=provider)
        
        findings = {}
        for clause in state.clauses:
            statutes_text = "\n".join([f"- {s.get('source')} (Section {s.get('section')}): {s.get('text')}" for s in state.retrieved_statutes])
            
            prompt = f"""
            Analyze the following legal clause for compliance against the provided statutes and common legal standards in {state.jurisdiction.get('country', 'India')}.

            Clause Title: {clause.get('title')}
            Clause Text: {clause.get('text')}

            Relevant Statutes:
            {statutes_text}

            Determine:
            1. Status: 'compliant', 'violation', or 'warning'.
            2. Risk Level: 'low', 'medium', or 'high'.
            3. Reason: Why it is or isn't compliant.
            4. Suggested Fix: How to make it compliant if it's not.

            Return ONLY a JSON object:
            {{
                "status": "...",
                "risk_level": "...",
                "reason": "...",
                "suggested_fix": "..."
            }}
            """
            
            try:
                response = await llm.generate(prompt)
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    findings[clause['id']] = json.loads(json_match.group(0))
                else:
                    findings[clause['id']] = {{
                        "status": "warning",
                        "risk_level": "medium",
                        "reason": "LLM failed to parse analysis for this clause.",
                        "suggested_fix": "Review manually."
                    }}
            except Exception as e:
                logger.error(f"Reasoning failed for clause {clause['id']}: {e}")
                findings[clause['id']] = {
                    "status": "error",
                    "risk_level": "high",
                    "reason": f"Analysis error: {str(e)}",
                    "suggested_fix": "Contact support."
                }
            
        state.compliance_findings = findings
        state.add_audit_log("ComplianceReasoning", "Analyze", f"Analyzed {len(state.clauses)} clauses with LLM reasoning")
