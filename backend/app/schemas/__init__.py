"""
Pydantic Schemas for API Request/Response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


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
    
    class Config:
        json_schema_extra = {
            "example": {
                "contract_text": "TERMINATION CLAUSE\n\nEither party may terminate...",
                "jurisdiction": "United States"
            }
        }


class ComplianceIssue(BaseModel):
    """Single compliance issue in report"""
    clause: str = Field(..., description="Original clause text")
    risk_level: str = Field(..., description="Risk level: low, medium, or high")
    fix: str = Field(..., description="Suggested fix or modification")
    citations: List[str] = Field(default_factory=list, description="Legal reference sources")


class ComplianceCheckResponse(BaseModel):
    """Response schema for compliance check endpoint"""
    drafted_contract: str = Field(..., description="Original contract text")
    compliance_report: List[ComplianceIssue] = Field(..., description="List of compliance issues")
    summary: Optional[Dict[str, Any]] = Field(None, description="Executive summary")


# ============================================================================
# GENERAL SCHEMAS
# ============================================================================

class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    agents_loaded: bool = Field(..., description="Whether agents are loaded")
    llm_available: bool = Field(..., description="Whether LLM client is available")
