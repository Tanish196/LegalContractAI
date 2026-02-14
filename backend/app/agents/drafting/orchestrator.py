import logging
from app.agents.state import ContractState
from app.agents.drafting.intent_analysis import IntentAnalysisAgent
from app.agents.drafting.policy_check import PolicyCheckAgent
from app.agents.drafting.template_selection import TemplateSelectionAgent
from app.agents.drafting.generation import GenerationAgent
from app.agents.drafting.review import SelfReviewAgent

logger = logging.getLogger(__name__)

class DraftingOrchestrator:
    def __init__(self):
        self.intent_analyzer = IntentAnalysisAgent()
        self.policy_checker = PolicyCheckAgent()
        self.template_selector = TemplateSelectionAgent()
        self.generator = GenerationAgent()
        self.reviewer = SelfReviewAgent()

    async def run(self, raw_requirements: str, metadata: dict = None, provider: str = None) -> ContractState:
        # 1. Initialize State
        state = ContractState(raw_text=raw_requirements, metadata=metadata or {})
        state.add_audit_log("DraftingOrchestrator", "Start", "Drafting process initiated")

        try:
            # 2. Understand Intent
            await self.intent_analyzer.process(state)
            
            # 3. Check Policies
            await self.policy_checker.process(state)
            
            # 4. Select Template
            await self.template_selector.process(state)
            
            # 5. Generate Content
            await self.generator.process(state)
            
            # 6. Self-Review / Refine
            await self.reviewer.process(state)
            
            # 7. Final Assembly
            state.final_contract = "\n\n".join([c.get("text", "") for c in state.drafted_clauses])
            
            if not state.final_contract or len(state.final_contract) < 100:
                raise ValueError("Agent pipeline produced insufficient content")

        except Exception as e:
            logger.warning(f"Drafting pipeline failed or produced poor results: {e}. Running fallback...")
            state.add_audit_log("DraftingOrchestrator", "Fallback", f"Error: {str(e)}")
            await self._run_fallback(state, provider)

        state.add_audit_log("DraftingOrchestrator", "End", "Drafting process completed")
        return state

    async def _run_fallback(self, state: ContractState, provider: str = None):
        """Single-prompt fallback if the agent pipeline crashes or fails to produce a good draft."""
        from app.llms import get_llm_client
        
        client = get_llm_client(provider)
        
        prompt = f"""
        You are a highly skilled legal counsel. The automated drafting pipeline encountered an issue, 
        so you must now manually draft the entire contract in one go.

        CONTRACT REQUIREMENTS:
        {state.raw_text}

        METADATA:
        {state.metadata}

        Please provide a professional, complete legal contract in Markdown format. 
        Include all necessary clauses (Parties, Effective Date, Termination, Liability, etc.) 
        based on the user's jurisdiction and purpose.
        """
        
        try:
            response = await client.generate(prompt)
            state.final_contract = response
            state.add_audit_log("DraftingOrchestrator", "Fallback Success", "Contract generated via fallback LLM call")
        except Exception as fall_err:
            logger.error(f"Fallback also failed: {fall_err}")
            state.final_contract = f"Error: Could not generate contract. {str(fall_err)}"
            state.add_audit_log("DraftingOrchestrator", "Total Failure", str(fall_err))
