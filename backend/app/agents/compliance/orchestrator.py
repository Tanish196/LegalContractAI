import logging
from app.agents.state import ContractState
from app.agents.compliance.ingestion import IngestionAgent
from app.agents.compliance.jurisdiction import JurisdictionResolverAgent
from app.agents.compliance.clause_extraction import ClauseExtractorAgent
from app.agents.compliance.statute_retrieval import StatuteRetrievalAgent
from app.agents.compliance.reasoning import ComplianceReasoningAgent
from app.agents.compliance.remediation import RemediationAgent
from app.agents.compliance.risk_scoring import RiskScoringAgent

logger = logging.getLogger(__name__)

class ComplianceOrchestrator:
    def __init__(self):
        self.ingestion = IngestionAgent()
        self.jurisdiction = JurisdictionResolverAgent()
        self.extractor = ClauseExtractorAgent()
        self.retriever = StatuteRetrievalAgent()
        self.reasoner = ComplianceReasoningAgent()
        self.remediator = RemediationAgent()
        self.risk_scorer = RiskScoringAgent()

    async def run(self, raw_text: str, metadata: dict = None) -> ContractState:
        # 1. Initialize State
        state = ContractState(raw_text=raw_text, metadata=metadata or {})
        state.add_audit_log("Orchestrator", "Start", "Compliance check initiated")

        # 2. Ingestion
        await self.ingestion.process(state)
        
        # 3. Jurisdiction
        await self.jurisdiction.process(state)
        
        # 4. Clause Extraction
        await self.extractor.process(state)
        
        # 5. Statute Retrieval (RAG)
        await self.retriever.process(state)
        
        # 6. Compliance Reasoning (Thinking)
        await self.reasoner.process(state)
        
        # 7. Remediation
        await self.remediator.process(state)
        
        # 8. Risk Scoring
        await self.risk_scorer.process(state)

        state.add_audit_log("Orchestrator", "End", "Compliance check completed")
        return state
