from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ContractState(BaseModel):
    """
    Shared state object for the agentic workflow.
    Passed between agents in the Orchestrator loop.
    """
    # core input
    raw_text: str = Field(default="", description="The original input text or request")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="User provided metadata like contract_type, parties, etc.")
    
    # context
    jurisdiction: Dict[str, str] = Field(default_factory=dict, description="Resolved jurisdiction (e.g., {'country': 'India', 'state': 'Delhi'})")
    
    # processing artifacts
    clauses: List[Dict[str, Any]] = Field(default_factory=list, description="Extracted raw clauses")
    retrieved_statutes: List[Dict[str, Any]] = Field(default_factory=list, description="Relevant statutes/regulations from RAG")
    retrieved_cases: List[Dict[str, Any]] = Field(default_factory=list, description="Relevant case law from RAG")
    
    # analysis results
    compliance_findings: Dict[str, Any] = Field(default_factory=dict, description="Issues found per clause")
    risk_summary: Dict[str, Any] = Field(default_factory=dict, description="Aggregated risk scores and high-level analysis")
    
    # generation artifacts
    drafted_clauses: List[Dict[str, Any]] = Field(default_factory=list, description="Newly generated or rewritten clauses")
    final_contract: str = Field(default="", description="Assembled final contract text")
    
    # observability
    audit_log: List[Dict[str, Any]] = Field(default_factory=list, description="Trace of agent actions and decisions")

    def add_audit_log(self, agent_name: str, action: str, details: str):
        self.audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "action": action,
            "details": details
        })
