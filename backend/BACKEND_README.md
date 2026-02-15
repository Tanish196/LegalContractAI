# LegalContractAI Backend - Comprehensive Documentation

## 📖 Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Project Structure](#project-structure)
4. [Configuration](#configuration)
5. [API Endpoints](#api-endpoints)
6. [AI Agents](#ai-agents)
7. [Services](#services)
8. [LLM Integration](#llm-integration)
9. [RAG System](#rag-system)
10. [Database & Storage](#database--storage)
11. [Authentication & Security](#authentication--security)
12. [Error Handling](#error-handling)
13. [Testing & Deployment](#testing--deployment)
14. [Troubleshooting](#troubleshooting)

---

## Overview

The LegalContractAI backend is a production-ready FastAPI application that provides intelligent legal contract services. It features:

- **Multiple AI Agents** for specialized legal tasks (drafting, compliance, risk analysis)
- **Multi-LLM Support** (Google Gemini, OpenAI) with fallback mechanisms
- **RAG Integration** using Pinecone for semantic legal document search
- **Secure Data Storage** with Supabase PostgreSQL backend
- **Encrypted Communication** for sensitive legal data
- **Comprehensive API** with 9+ specialized endpoints
- **Rate Limiting & Usage Tracking** for controlled access
- **CORS Support** for frontend integration

### Key Features

✅ **Intelligent Contract Drafting** - AI-powered contract generation with templates  
✅ **Compliance Analysis** - Multi-jurisdiction compliance checking with RAG  
✅ **Risk Assessment** - Identify problematic clauses and legal risks  
✅ **Clause Classification** - Automated clause categorization and analysis  
✅ **Chat Interface** - Conversational legal AI assistant  
✅ **Report Generation** - Detailed analysis reports in Markdown  
✅ **Multi-Jurisdiction** - Support for different legal systems (US, India, etc.)  
✅ **Audit Trail** - Complete usage and activity logging  
✅ **Scalable Architecture** - Async/await for concurrent request handling  

---

## Quick Start

### 1. Prerequisites

```bash
# System Requirements
- Python 3.10 or higher
- 2GB RAM minimum
- Internet connection for API calls

# Required API Keys
- Google Generative AI (Gemini) API key
- (Optional) OpenAI API key
- (Optional) Pinecone API key
- (Optional) Supabase credentials
```

### 2. Installation

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# Required:
#   GOOGLE_API_KEY=your_gemini_api_key
#
# Optional:
#   OPENAI_API_KEY=your_openai_key
#   PINECONE_API_KEY=your_pinecone_key
#   SUPABASE_URL=your_supabase_url
#   SUPABASE_KEY=your_supabase_key
```

### 4. Run the Server

```bash
# Option 1: Using Python module
python -m app.main

# Option 2: Using uvicorn directly (with auto-reload for development)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Option 3: Production with gunicorn
gunicorn app.main:app --workers 4 --timeout 120
```

### 5. Verify Installation

```bash
# Health check
curl http://localhost:8000/api/health

# View API documentation
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

---

## Project Structure

```
backend/
│
├── app/                              # Main application package
│   │
│   ├── main.py                       # FastAPI app initialization
│   ├── config.py                     # Configuration management
│   │
│   ├── agents/                       # AI Agent modules
│   │   ├── __init__.py
│   │   ├── state.py                  # Shared agent state model
│   │   ├── ingestion_agent.py        # Input normalization
│   │   ├── clause_agent.py           # Clause extraction & splitting
│   │   ├── compliance_agent.py       # Compliance with RAG
│   │   ├── risk_agent.py             # Risk classification
│   │   ├── drafting_agent.py         # Contract drafting
│   │   ├── structure_agent.py        # Document structure analysis
│   │   ├── template_agent.py         # Template matching
│   │   ├── merge_agent.py            # Document merging
│   │   ├── examples.py               # Agent usage examples
│   │   ├── compliance/               # Compliance sub-agents
│   │   │   └── ...
│   │   └── drafting/                 # Drafting sub-agents
│   │       └── ...
│   │
│   ├── api/                          # API Route Handlers
│   │   ├── __init__.py
│   │   ├── health.py                 # Health checks
│   │   ├── drafting.py               # Contract drafting endpoints
│   │   ├── compliance.py             # Compliance checking endpoints
│   │   ├── analysis.py               # Document analysis endpoints
│   │   ├── chat.py                   # Chat interface endpoints
│   │   ├── reports.py                # Report generation endpoints
│   │   ├── research.py               # Legal research endpoints
│   │   ├── summarization.py          # Document summarization
│   │   └── usage.py                  # Usage statistics endpoints
│   │
│   ├── llms/                         # LLM Client Implementations
│   │   ├── __init__.py
│   │   ├── gemini_client.py          # Google Generative AI client
│   │   ├── openai_client.py          # OpenAI client
│   │   ├── hybrid_client.py          # Fallback/hybrid client
│   │   └── prompts/                  # Prompt templates
│   │       └── ...
│   │
│   ├── services/                     # Business Logic Services
│   │   ├── __init__.py
│   │   ├── draft_service.py          # Contract drafting logic
│   │   ├── compliance_service.py     # Compliance check logic
│   │   ├── insight_service.py        # Legal insights extraction
│   │   ├── supabase_service.py       # Supabase integration
│   │   └── encryption.py             # Encryption utilities
│   │
│   ├── RAG/                          # Retrieval-Augmented Generation
│   │   ├── __init__.py
│   │   ├── pinecone_store.py         # Pinecone vector database
│   │   └── embeddings.py             # Embedding generation
│   │
│   ├── schemas/                      # Pydantic Data Models
│   │   ├── __init__.py
│   │   ├── request.py                # Request schemas
│   │   ├── response.py               # Response schemas
│   │   └── models.py                 # Domain models
│   │
│   ├── utils/                        # Utility Functions
│   │   ├── __init__.py
│   │   ├── rate_limiter.py           # Rate limiting utilities
│   │   ├── validators.py             # Input validators
│   │   └── helpers.py                # Helper functions
│   │
│   └── pdf_templates/                # PDF Contract Templates
│       ├── msa/                      # Master Service Agreement
│       ├── nda/                      # Non-Disclosure Agreement
│       ├── sow/                      # Statement of Work
│       ├── la/                       # License Agreement
│       ├── ea/                       # Employment Agreement
│       ├── ica/                      # Independent Contractor Ag.
│       ├── pa/                       # Partnership Agreement
│       └── nca/                      # Non-Compete Agreement
│
├── legal_texts/                      # Legal Reference Documents
│   ├── us_contract_law_basics.md
│   ├── gdpr_compliance.txt
│   ├── hipaa_requirements.md
│   └── ...
│
├── scripts/                          # Utility Scripts
│   ├── check_db_schema.py            # Database schema inspection
│   ├── ingest_data.py                # Data ingestion utilities
│   ├── setup_pinecone.py             # Pinecone initialization
│   ├── test_fallback.py              # Test fallback mechanisms
│   ├── verify_encryption_flow.py     # Test encryption
│   └── verify_phase2.py              # Phase 2 verification
│
├── requirements.txt                  # Python dependencies
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore rules
└── README.md                         # Backend documentation
```

---

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# ==================
# API Configuration
# ==================

# Google Generative AI (Gemini)
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash-exp

# OpenAI (Optional, for fallback)
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4-turbo

# ==================
# RAG Configuration
# ==================

# Pinecone Vector Database
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=legal-documents

# ==================
# Database Configuration
# ==================

# Supabase (Optional, for data persistence)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key
CHAT_ENCRYPTION_KEY_V1=your_encryption_key_32_bytes

# ==================
# Server Configuration
# ==================

HOST=0.0.0.0
PORT=8000
DEBUG=False

# ==================
# CORS Configuration
# ==================

CORS_ORIGINS=http://localhost:5173,http://localhost:3000,https://yourdomain.com

# ==================
# Logging Configuration
# ==================

LOG_LEVEL=INFO
```

### Configuration File (app/config.py)

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Project Settings
PROJECT_NAME = "LegalContractAI"
VERSION = "1.0.0"

# AI Model Settings
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# RAG Settings
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")

# Database Settings
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
CHAT_ENCRYPTION_KEY_V1 = os.getenv("CHAT_ENCRYPTION_KEY_V1")

# CORS Settings
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://localhost:3000"
).split(",")
```

---

## API Endpoints

### Health & Status

#### **GET** `/api/health`

Check API health status and service availability.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-02-15T10:30:00Z",
  "services": {
    "gemini": "operational",
    "pinecone": "operational",
    "supabase": "operational"
  }
}
```

---

### Contract Drafting

#### **POST** `/api/drafting/draft`

Generate a professional contract based on requirements.

**Request:**
```json
{
  "party_a": "Acme Corporation",
  "party_b": "Example Industries Inc.",
  "jurisdiction": "United States",
  "purpose": "Service Agreement",
  "term": "24 months",
  "requirements": "Software development services with 40 hours/week allocation, $50,000/month, includes maintenance...",
  "template_type": "MSA"
}
```

**Response:**
```json
{
  "drafted_contract": "# SERVICE AGREEMENT\n\nThis Service Agreement ('Agreement')...",
  "compliance_report": [],
  "metadata": {
    "parties": ["Acme Corporation", "Example Industries Inc."],
    "jurisdiction": "United States",
    "purpose": "Service Agreement",
    "term": "24 months",
    "generated_at": "2026-02-15T10:30:00Z"
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/drafting/draft \
  -H "Content-Type: application/json" \
  -d '{
    "party_a": "Acme Corp",
    "party_b": "Example Inc",
    "jurisdiction": "United States",
    "purpose": "Service Agreement",
    "requirements": "Create a professional software development agreement"
  }'
```

---

### Compliance Analysis

#### **POST** `/api/compliance/check`

Analyze contract for compliance issues and risks.

**Request:**
```json
{
  "contract_text": "TERMINATION CLAUSE\n\nEither party may terminate this agreement with 30 days notice...",
  "jurisdiction": "United States",
  "check_type": "full"
}
```

**Response:**
```json
{
  "drafted_contract": "original contract text",
  "compliance_report": [
    {
      "clause": "Either party may terminate this agreement with 30 days notice",
      "risk_level": "medium",
      "severity": "warning",
      "fix": "Specify termination procedures including notice delivery method and termination for cause vs. convenience",
      "citations": ["Termination Clause - US Contract Law Basics"],
      "applicable_laws": ["UCC §2-309", "Restatement (Second) of Contracts §90"]
    }
  ],
  "summary": {
    "total_clauses": 12,
    "high_risk": 1,
    "medium_risk": 3,
    "low_risk": 8,
    "overall_assessment": "REVIEW RECOMMENDED",
    "priority_actions": [
      "Review termination procedures",
      "Add liability limitations",
      "Clarify dispute resolution"
    ]
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/compliance/check \
  -H "Content-Type: application/json" \
  -d '{
    "contract_text": "Your contract text...",
    "jurisdiction": "United States"
  }'
```

---

### Document Analysis

#### **POST** `/api/analysis/analyze`

Perform custom analysis on legal documents.

**Request:**
```json
{
  "content": "contract text or legal document",
  "analysis_type": "risk_assessment",
  "focus_areas": ["liability", "termination", "ip_rights"]
}
```

**Response:**
```json
{
  "analysis_type": "risk_assessment",
  "findings": [...],
  "recommendations": [...]
}
```

---

### Clause Classification

#### **POST** `/api/analysis/classify-clauses`

Categorize and classify individual clauses.

**Request:**
```json
{
  "clauses": [
    "Either party may terminate with 30 days notice",
    "All intellectual property created shall remain property of Company A"
  ]
}
```

**Response:**
```json
{
  "classifications": [
    {
      "clause": "Either party may terminate with 30 days notice",
      "type": "Termination",
      "subtypes": ["Notice Period", "Termination Right"],
      "risk_level": "medium"
    }
  ]
}
```

---

### Report Generation

#### **POST** `/api/reports/generate`

Generate formatted analysis reports.

**Request:**
```json
{
  "task_type": "compliance-summary",
  "content": "contract text or legal document",
  "jurisdiction": "United States",
  "format": "markdown"
}
```

**Response:**
```json
{
  "task_type": "compliance-summary",
  "report_markdown": "# Compliance Analysis Report\n\n## Executive Summary\n...",
  "metadata": {
    "generated_at": "2026-02-15T10:30:00Z",
    "jurisdiction": "United States"
  }
}
```

---

### Chat Interface

#### **POST** `/api/chat/message`

Chat with AI assistant about legal matters.

**Request:**
```json
{
  "message": "What should I include in an NDA?",
  "conversation_id": "conv-123",
  "context": "We are discussing NDAs for a software partnership"
}
```

**Response:**
```json
{
  "response": "An effective NDA should include...",
  "conversation_id": "conv-123",
  "sources": ["legal_reference_doc_1.md"]
}
```

---

### Legal Research

#### **POST** `/api/research/query`

Perform legal research using RAG.

**Request:**
```json
{
  "query": "What are the standard termination clauses in service agreements?",
  "jurisdiction": "United States",
  "document_types": ["statutes", "case_law", "templates"]
}
```

**Response:**
```json
{
  "query": "What are the standard termination clauses...",
  "results": [
    {
      "title": "Termination Clause Standards",
      "content": "...",
      "source": "contract_clauses_index",
      "relevance_score": 0.95
    }
  ]
}
```

---

### Document Summarization

#### **POST** `/api/summarization/summarize`

Generate summaries of legal documents.

**Request:**
```json
{
  "content": "long contract text",
  "summary_type": "executive",
  "key_points_count": 10
}
```

**Response:**
```json
{
  "summary": "This agreement is a Master Service Agreement between...",
  "key_points": [
    "Services are provided for 24 months",
    "Payment is $50,000/month",
    "..."
  ]
}
```

---

### Usage Statistics

#### **GET** `/api/usage/stats`

Get usage statistics and credit information.

**Response:**
```json
{
  "period": "2026-02-01T00:00:00Z to 2026-02-15T23:59:59Z",
  "usage": {
    "total_requests": 150,
    "successful_requests": 148,
    "failed_requests": 2,
    "total_tokens": 45230,
    "error_rate": 0.013
  },
  "breakdown_by_endpoint": {
    "drafting": 30,
    "compliance": 50,
    "analysis": 40,
    "chat": 30
  },
  "credits": {
    "daily_limit": 500,
    "used_today": 234,
    "remaining": 266
  }
}
```

---

## AI Agents

The system uses specialized AI agents for different legal tasks. Each agent is implemented as an async function that processes and updates a shared state object.

### Agent Architecture

```python
from app.agents.state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI

async def agent_function(state: AgentState) -> AgentState:
    """
    Process legal documents using AI.
    
    Args:
        state: Shared agent state containing context
        
    Returns:
        Updated state with results
    """
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")
    
    # Process input with AI
    result = await llm.ainvoke(state.input_data)
    
    # Update state
    state.output_data = result
    return state
```

### Available Agents

#### 1. **Ingestion Agent** (`ingestion_agent.py`)

Normalizes and validates input data.

```python
async def ingestion_agent(raw_input: dict) -> dict:
    """Normalize and validate user input."""
    # Validates required fields
    # Cleans text data
    # Extracts metadata
    return normalized_input
```

**Use Case**: Prepare user input for downstream processing.

---

#### 2. **Clause Agent** (`clause_agent.py`)

Splits contracts into individual clauses.

```python
async def clause_agent(contract_text: str) -> list[str]:
    """Extract and split contract into clauses."""
    # Splits contract into logical clauses
    # Identifies clause types
    # Returns structured clauses
    return clauses_list
```

**Use Case**: Prepare contracts for clause-level analysis.

---

#### 3. **Compliance Agent** (`compliance_agent.py`)

Analyzes clauses for compliance using RAG.

```python
async def compliance_agent(
    clause: str,
    jurisdiction: str,
    rag_store: PineconeStore
) -> ComplianceResult:
    """Check clause compliance with legal requirements."""
    # Retrieves relevant legal documents via RAG
    # Analyzes clause against regulations
    # Generates compliance report
    return compliance_result
```

**Use Case**: Check individual clauses for legal compliance.

---

#### 4. **Risk Agent** (`risk_agent.py`)

Classifies risk level of clauses.

```python
async def risk_agent(
    clause: str,
    compliance_data: dict
) -> RiskClassification:
    """Classify risk level of a clause."""
    # Evaluates risk factors
    # Assigns risk level (low/medium/high)
    # Provides mitigation recommendations
    return risk_classification
```

**Use Case**: Prioritize high-risk clauses for review.

---

#### 5. **Drafting Agent** (`drafting_agent.py`)

Generates contract content.

```python
async def drafting_agent(
    party_a: str,
    party_b: str,
    requirements: str
) -> str:
    """Generate contract draft."""
    # Creates professional contract
    # Includes all required clauses
    # Follows legal standards
    return drafted_contract
```

**Use Case**: Create initial contract drafts.

---

#### 6. **Structure Agent** (`structure_agent.py`)

Analyzes document structure and organization.

**Use Case**: Improve document formatting and organization.

---

#### 7. **Template Agent** (`template_agent.py`)

Matches and applies contract templates.

**Use Case**: Use pre-built templates for common contract types.

---

#### 8. **Merge Agent** (`merge_agent.py`)

Combines multiple clauses or documents.

**Use Case**: Merge multiple contract versions or clauses.

---

### Agent State Model

```python
class AgentState(BaseModel):
    """Shared state for agent pipeline."""
    
    # Input data
    contract_text: str
    clauses: list[str] = []
    metadata: dict = {}
    
    # Processing results
    compliance_report: list[dict] = []
    risk_assessment: dict = {}
    recommendations: list[str] = []
    
    # Control flow
    current_agent: str
    timestamp: datetime
    errors: list[str] = []
```

---

## Services

Services contain the core business logic for major features.

### Draft Service

```python
# services/draft_service.py

class DraftService:
    """Handle contract drafting logic."""
    
    async def draft_contract(
        self,
        party_a: str,
        party_b: str,
        jurisdiction: str,
        requirements: str,
        template_type: str = "MSA"
    ) -> DraftResult:
        """Draft a contract based on requirements."""
        # Validate inputs
        # Select appropriate template
        # Use AI to generate contract
        # Return formatted result
```

### Compliance Service

```python
# services/compliance_service.py

class ComplianceService:
    """Handle compliance checking logic."""
    
    async def check_compliance(
        self,
        contract_text: str,
        jurisdiction: str
    ) -> ComplianceReport:
        """Check contract compliance with regulations."""
        # Split contract into clauses
        # Analyze each clause for compliance
        # Aggregate results
        # Generate report
```

### Encryption Service

```python
# services/encryption.py

class EncryptionService:
    """Handle data encryption/decryption."""
    
    @staticmethod
    def encrypt_message(plaintext: str, key: str) -> str:
        """Encrypt sensitive data."""
        
    @staticmethod
    def decrypt_message(ciphertext: str, key: str) -> str:
        """Decrypt sensitive data."""
```

### Supabase Service

```python
# services/supabase_service.py

class SupabaseService:
    """Handle Supabase integration."""
    
    async def store_contract(self, contract: dict) -> str:
        """Store contract in Supabase."""
        
    async def retrieve_contract(self, contract_id: str) -> dict:
        """Retrieve contract from Supabase."""
```

---

## LLM Integration

### Multi-LLM Support

The system supports multiple LLM providers with fallback capabilities.

#### Google Generative AI (Gemini)

```python
# llms/gemini_client.py

from langchain_google_genai import ChatGoogleGenerativeAI

class GeminiClient:
    """Google Generative AI client."""
    
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=api_key
        )
    
    async def generate(self, prompt: str) -> str:
        """Generate response using Gemini."""
        response = await self.llm.ainvoke(prompt)
        return response.content
```

#### OpenAI Client

```python
# llms/openai_client.py

from langchain_openai import ChatOpenAI

class OpenAIClient:
    """OpenAI client."""
    
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(
            model="gpt-4-turbo",
            openai_api_key=api_key
        )
```

#### Hybrid Client (Fallback)

```python
# llms/hybrid_client.py

class HybridClient:
    """Fallback to OpenAI if Gemini fails."""
    
    async def generate(self, prompt: str) -> str:
        """Try Gemini first, fallback to OpenAI."""
        try:
            return await self.gemini_client.generate(prompt)
        except Exception as e:
            logger.warning(f"Gemini failed: {e}, using OpenAI")
            return await self.openai_client.generate(prompt)
```

### Prompt Management

```python
# llms/prompts/

contract_drafting_prompt = """
You are an expert legal document drafter. Generate a professional contract 
based on the following requirements:

Party A: {party_a}
Party B: {party_b}
Jurisdiction: {jurisdiction}
Purpose: {purpose}
Requirements: {requirements}

Generate a comprehensive, legally sound contract.
"""
```

---

## RAG System

The Retrieval-Augmented Generation system enables semantic search of legal documents.

### Pinecone Integration

```python
# RAG/pinecone_store.py

from pinecone import Pinecone

class PineconeStore:
    """Vector database for legal documents."""
    
    def __init__(self, api_key: str, index_name: str):
        self.pc = Pinecone(api_key=api_key)
        self.index = self.pc.Index(index_name)
    
    async def upsert_documents(self, documents: list[dict]):
        """Add documents to vector database."""
        embeddings = self._generate_embeddings(documents)
        self.index.upsert(vectors=embeddings)
    
    async def search(self, query: str, top_k: int = 5) -> list[dict]:
        """Semantic search for relevant documents."""
        query_embedding = self._embed_query(query)
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        return results
```

### Document Indexing

Available indexes:

- `indian-statutes` - Indian legal statutes
- `indian-regulations` - Indian regulations
- `contract-clauses` - Common contract clauses
- `case-law-summaries` - Case law summaries
- `legal-commentary` - Legal commentary and analysis

### Usage Example

```python
# Search for termination clause examples
results = await rag_store.search(
    "termination clause with notice period",
    top_k=5
)

for result in results:
    print(f"Source: {result['metadata']['source']}")
    print(f"Content: {result['metadata']['text']}")
    print(f"Relevance: {result['score']}")
```

---

## Database & Storage

### Supabase Integration

The system uses Supabase for persistent data storage.

#### Database Tables

```sql
-- Contracts table
CREATE TABLE contracts (
    id UUID PRIMARY KEY,
    title VARCHAR(255),
    content TEXT,
    party_a VARCHAR(255),
    party_b VARCHAR(255),
    jurisdiction VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Compliance Reports table
CREATE TABLE compliance_reports (
    id UUID PRIMARY KEY,
    contract_id UUID REFERENCES contracts(id),
    report_data JSONB,
    risk_level VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Chat History table
CREATE TABLE chat_history (
    id UUID PRIMARY KEY,
    user_id UUID,
    message TEXT,
    response TEXT,
    encrypted BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Usage Logs table
CREATE TABLE usage_logs (
    id UUID PRIMARY KEY,
    user_id UUID,
    endpoint VARCHAR(255),
    status_code INTEGER,
    tokens_used INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Supabase Service Usage

```python
from app.services.supabase_service import SupabaseService

service = SupabaseService()

# Store contract
contract_data = {
    "title": "Service Agreement",
    "content": "...",
    "party_a": "Company A",
    "party_b": "Company B"
}
contract_id = await service.store_contract(contract_data)

# Retrieve contract
contract = await service.retrieve_contract(contract_id)

# Log usage
await service.log_usage(
    endpoint="/api/drafting/draft",
    status_code=200,
    tokens_used=1250
)
```

---

## Authentication & Security

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Input Validation

All inputs are validated using Pydantic:

```python
from pydantic import BaseModel, Field

class DraftRequest(BaseModel):
    """Validated contract drafting request."""
    
    party_a: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="First party name"
    )
    party_b: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Second party name"
    )
    jurisdiction: str = Field(
        default="United States",
        description="Legal jurisdiction"
    )
    requirements: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Contract requirements"
    )
```

### Rate Limiting

```python
from app.utils.rate_limiter import RateLimiter

limiter = RateLimiter(requests_per_minute=60)

@app.post("/api/drafting/draft")
async def draft_contract(request: DraftRequest):
    """Draft endpoint with rate limiting."""
    if not await limiter.allow_request():
        raise HTTPException(
            status_code=429,
            detail="Too many requests"
        )
    # Process request
```

### Data Encryption

```python
from app.services.encryption import EncryptionService

# Encrypt sensitive data
encrypted_message = EncryptionService.encrypt_message(
    plaintext="Confidential clause text",
    key=os.getenv("CHAT_ENCRYPTION_KEY_V1")
)

# Decrypt when needed
decrypted = EncryptionService.decrypt_message(
    ciphertext=encrypted_message,
    key=os.getenv("CHAT_ENCRYPTION_KEY_V1")
)
```

---

## Error Handling

### Exception Handling

```python
from fastapi import HTTPException

@router.post("/api/endpoint")
async def endpoint(request: Request):
    try:
        # Process request
        result = await process(request)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
```

### Error Response Format

```json
{
  "error": "Error type name",
  "detail": "Detailed error message",
  "status_code": 400,
  "timestamp": "2026-02-15T10:30:00Z"
}
```

---

## Testing & Deployment

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_drafting.py -v

# Run with coverage
pytest --cov=app tests/
```

### Example Test

```python
# tests/test_drafting.py

import pytest
from app.api.drafting import router

@pytest.mark.asyncio
async def test_draft_contract():
    """Test contract drafting endpoint."""
    request = {
        "party_a": "Test Corp",
        "party_b": "Example Inc",
        "jurisdiction": "United States",
        "requirements": "Create a test agreement"
    }
    
    response = await router.draft_contract(request)
    
    assert response.status_code == 200
    assert "drafted_contract" in response.json()
```

### Deployment

#### Development

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Production (Gunicorn)

```bash
gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120
```

#### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Troubleshooting

### Common Issues

#### 1. API Key Errors

**Error**: `Invalid API key` or `Authentication failed`

**Solution**:
```bash
# Verify .env file
cat .env | grep GOOGLE_API_KEY

# Confirm key is valid at https://ai.google.dev
# Regenerate key if needed
```

#### 2. Pinecone Connection Issues

**Error**: `Failed to connect to Pinecone`

**Solution**:
```bash
# Check internet connection
ping api.pinecone.io

# Verify Pinecone credentials
echo $PINECONE_API_KEY

# Test connection with script
python scripts/test_pinecone.py
```

#### 3. Supabase Connection Issues

**Error**: `Connection refused` or `Authentication error`

**Solution**:
```bash
# Verify Supabase URL
cat .env | grep SUPABASE_URL

# Test connection
python scripts/check_db_schema.py
```

#### 4. Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# On Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# On macOS/Linux
lsof -i :8000
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

#### 5. Import Errors

**Error**: `ModuleNotFoundError: No module named 'app'`

**Solution**:
```bash
# Run from backend directory
cd backend

# Or install in development mode
pip install -e .
```

---

## Performance Optimization

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
async def get_templates():
    """Cache contract templates."""
    return await load_templates()
```

### Async/Await

```python
import asyncio

# Process multiple clauses concurrently
async def check_multiple_clauses(clauses: list[str]):
    tasks = [
        compliance_agent(clause)
        for clause in clauses
    ]
    return await asyncio.gather(*tasks)
```

### Connection Pooling

```python
# Reuse HTTP connections
import aiohttp

async with aiohttp.ClientSession() as session:
    # Make multiple requests
    results = await asyncio.gather(
        session.get(url1),
        session.get(url2)
    )
```

---

## Monitoring & Logging

### Logging Configuration

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Usage Analytics

```python
# Access usage statistics
GET /api/usage/stats

# Response includes:
# - Total requests
# - Successful/failed requests
# - Token consumption
# - Errors by endpoint
```

---

## Version History

- **v1.0.0** (February 2026) - Initial release
  - Contract drafting
  - Compliance checking
  - RAG integration
  - Multi-LLM support

---

## Support & Resources

- **API Docs**: http://localhost:8000/docs
- **FastAPI**: https://fastapi.tiangolo.com
- **LangChain**: https://python.langchain.com
- **Pinecone**: https://docs.pinecone.io
- **Supabase**: https://supabase.com/docs

---

**Last Updated**: February 2026  
**Version**: 1.0.0  
**Status**: Production Ready

