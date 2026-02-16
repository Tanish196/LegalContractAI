"""
Pydantic Schemas for API Request/Response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union, Literal


# --- Common ---
class ErrorResponse(BaseModel):
    detail: str


# --- Clause Analysis ---
class ClauseAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Contract text to analyze")
    provider: Optional[str] = None

class ClauseRisk(BaseModel):
    clause_text: str
    risk_level: str = Field(..., pattern="^(High|Medium|Low)$")
    explanation: str
    recommendation: Optional[str] = None

class ClauseAnalysisResponse(BaseModel):
    risks: List[ClauseRisk]
    summary: str

# --- Legal Research ---
class LegalResearchRequest(BaseModel):
    query: str = Field(..., min_length=5, description="Legal question")
    jurisdiction: str = "India"
    provider: Optional[str] = None

class Citation(BaseModel):
    title: str
    source: str
    text: str

class LegalResearchResponse(BaseModel):
    answer: str
    citations: List[Citation]

# --- Case Summarization ---
class CaseSummaryRequest(BaseModel):
    case_text: str = Field(..., min_length=100)
    provider: Optional[str] = None

class CaseSummaryResponse(BaseModel):
    summary: str
    key_holdings: List[str]
    citations: List[str]

# --- Chat Assistant ---
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    provider: Optional[str] = None
    history: List[Dict[str, str]] = [] # [{"role": "user", "content": "..."}]

class ChatResponse(BaseModel):
    reply: str
    intent: str
    suggested_action: Optional[str] = None
    citations: Optional[List[Citation]] = None


# ============================================================================
# CONTRACT DRAFTING SCHEMAS
# ============================================================================

class PartyInput(BaseModel):
    """Party information for contract"""
    name: str = Field(..., description="Full legal name of the party")
    role: Optional[str] = Field(None, description="Role in the contract (e.g., 'Client', 'Service Provider')")


class ContractDraftRequest(BaseModel):
    """Request schema for contract drafting endpoint"""
    
    # Party information (support multiple formats)
    parties: Optional[List[PartyInput]] = Field(None, description="List of parties")
    party_a: Optional[str] = Field(None, description="First party name")
    party_b: Optional[str] = Field(None, description="Second party name")
    
    # Contract details
    jurisdiction: Optional[str] = Field("United States", description="Legal jurisdiction")
    purpose: Optional[str] = Field("General Agreement", description="Contract purpose/type")
    term: Optional[str] = Field("12 months", description="Contract duration")
    contract_type: Optional[str] = Field(None, description="Type of contract")
    
    # User requirements
    requirements: str = Field(..., description="Contract requirements and specifications", min_length=10)
    key_terms: Optional[str] = Field(None, description="Key contract terms")
    
    class Config:
        json_schema_extra = {
            "example": {
                "party_a": "Acme Corporation",
                "party_b": "Example Industries Inc.",
                "jurisdiction": "United States",
                "purpose": "Service Agreement",
                "term": "24 months",
                "requirements": "This is a software development service agreement..."
            }
        }


class ContractDraftResponse(BaseModel):
    """Response schema for contract drafting endpoint"""
    drafted_contract: str = Field(..., description="Generated contract text in Markdown")
    compliance_report: List[Dict[str, Any]] = Field(default_factory=list, description="Empty for drafting service")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Extracted metadata")


# ============================================================================
# COMPLIANCE CHECK SCHEMAS
# ============================================================================

class ComplianceCheckRequest(BaseModel):
    """Request schema for compliance check endpoint"""
    contract_text: str = Field(..., description="Full contract text to analyze", min_length=50)
    jurisdiction: Optional[str] = Field("United States", description="Legal jurisdiction for compliance")
    provider: Optional[str] = Field("google", description="Preferred LLM provider (openai or google)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "contract_text": "TERMINATION CLAUSE\n\nEither party may terminate...",
                "jurisdiction": "United States",
                "provider": "google"
            }
        }


class InsightTaskRequest(BaseModel):
    """Schema for general-purpose report generation."""
    task_type: Literal[
        "case-summary",
        "loophole-detection",
        "clause-classification",
        "contract-drafting",
        "compliance-check"
    ] = Field(..., description="Type of structured report to generate")
    content: str = Field(..., description="Source text or instructions", min_length=20)
    jurisdiction: Optional[str] = Field(None, description="Optional jurisdiction context")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional structured data for the LLM prompt")
    provider: Optional[str] = Field(None, description="Preferred LLM provider (openai or google)")


class InsightTaskResponse(BaseModel):
    """Response schema for general-purpose report generation."""
    task_type: str = Field(..., description="Echoed task type")
    report_markdown: str = Field(..., description="Structured Markdown content")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional context (e.g., jurisdiction)")


class ComplianceIssue(BaseModel):
    """Single compliance issue in report"""
    clause: str = Field(..., description="Original clause text")
    heading: Optional[str] = Field(None, description="Readable heading for UI sections")
    risk_level: str = Field(..., description="Risk level: low, medium, or high")
    fix: str = Field(..., description="Suggested fix or modification")
    citations: List[str] = Field(default_factory=list, description="Legal reference sources")
    issue_summary: Optional[str] = Field(None, description="Summary of the compliance gap")
    missing_requirements: List[str] = Field(default_factory=list, description="Specific missing elements")
    recommended_actions: List[str] = Field(default_factory=list, description="Actionable remediation steps")
    regulation: Optional[str] = Field(None, description="Referenced regulation or framework")
    reference: Optional[str] = Field(None, description="Specific statutory citation")


class ComplianceCheckResponse(BaseModel):
    """Response schema for compliance check endpoint"""
    drafted_contract: str = Field(..., description="Original contract text")
    compliance_report: List[ComplianceIssue] = Field(..., description="List of compliance issues")
    summary: Optional[Dict[str, Any]] = Field(None, description="Executive summary metrics")
    insights: Optional[Dict[str, Any]] = Field(None, description="Action items and suggested language")
    report_markdown: Optional[str] = Field(None, description="Richly formatted compliance memo in Markdown")


# ============================================================================
# GENERAL SCHEMAS
# ============================================================================

class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")


# --- Usage History ---
class UsageRecordRequest(BaseModel):
    user_id: str
    service_type: str
    prompt_title: Optional[str] = None
    prompt_output: Optional[str] = None

class UsageHistoryItem(BaseModel):
    id: str
    user_id: str
    service_type: str
    created_at: str
    prompt_title: Optional[str] = None
    prompt_output: Optional[str] = None
    is_encrypted: bool = False

class UsageHistoryResponse(BaseModel):
    history: List[UsageHistoryItem]

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    agents_loaded: bool = Field(..., description="Whether agents are loaded")
    llm_available: bool = Field(..., description="Whether LLM client is available")
