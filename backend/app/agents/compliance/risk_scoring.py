from app.agents.state import ContractState
import logging

logger = logging.getLogger(__name__)

class RiskScoringAgent:
    async def process(self, state: ContractState):
        logger.info("RiskScoringAgent: Calculating risk score")
        
        # Simple aggregation logic
        high_risks = 0
        medium_risks = 0
        
        for finding in state.compliance_findings.values():
            if finding.get("risk_level") == "high":
                high_risks += 1
            elif finding.get("risk_level") == "medium":
                medium_risks += 1
                
        total_score = (high_risks * 10) + (medium_risks * 5)
        normalized_score = min(100, total_score) # 0-100 scale
        
        state.risk_summary = {
            "overall_score": normalized_score,
            "risk_level": "Critical" if normalized_score > 50 else "Moderate" if normalized_score > 20 else "Low",
            "breakdown": {"high": high_risks, "medium": medium_risks}
        }
        
        state.add_audit_log("RiskScoring", "Calculate", f"Risk Score: {normalized_score}")
