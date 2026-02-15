# LegalContractAI Backend API

FastAPI backend for AI-powered legal contract drafting, compliance checking, and intelligent analysis. Powered by advanced LLMs (Google Gemini, OpenAI) with RAG (Retrieval-Augmented Generation) capabilities using Pinecone vector database.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` and update with your API key:

```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 3. Run the Server

```bash
# Development mode with auto-reload
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access API Documentation

Open your browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📋 API Endpoints

### Health Check

**GET** `/api/health`

Check if API and services are running.

```bash
curl http://localhost:8000/api/health
```

---

### Contract Drafting

**POST** `/api/drafting/draft`

Generate a professional contract using AI.

**Request Body:**
```json
{
  "party_a": "Acme Corporation",
  "party_b": "Example Industries Inc.",
  "jurisdiction": "United States",
  "purpose": "Service Agreement",
  "term": "24 months",
  "requirements": "This is a software development service agreement where Party A will provide web development services to Party B..."
}
```

**Response:**
```json
{
  "drafted_contract": "# SERVICE AGREEMENT\n\nThis Service Agreement...",
  "compliance_report": [],
  "metadata": {
    "parties": [...],
    "jurisdiction": "United States",
    ...
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
    "requirements": "Create a service agreement for software development"
  }'
```

---

### Compliance Check

**POST** `/api/compliance/check`

Analyze contract for compliance issues.

**Request Body:**
```json
{
  "contract_text": "TERMINATION CLAUSE\n\nEither party may terminate this agreement...",
  "jurisdiction": "United States"
}
```

**Response:**
```json
{
  "drafted_contract": "original contract text",
  "compliance_report": [
    {
      "clause": "Either party may terminate...",
      "risk_level": "medium",
      "fix": "Add specific notice period and termination procedures",
      "citations": ["us_contract_law_basics.md"]
    }
  ],
  "summary": {
    "total_clauses": 5,
    "high_risk": 1,
    "medium_risk": 2,
    "low_risk": 2,
    "overall_assessment": "REVIEW NEEDED"
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/compliance/check \
  -H "Content-Type: application/json" \
  -d '{
    "contract_text": "Your contract text here...",
    "jurisdiction": "United States"
  }'
```

---

### Structured Report Generation

**POST** `/api/reports/generate`

Produce a richly formatted Markdown report (case summary, loophole analysis, etc.) via server-side prompt engineering.

**Request Body:**
```json
{
  "task_type": "case-summary",
  "content": "Paste raw facts, clauses, or instructions here",
  "jurisdiction": "Optional context"
}
```

**Response:**
```json
{
  "task_type": "case-summary",
  "report_markdown": "# Case Snapshot...",
  "metadata": {
    "jurisdiction": "United States"
  }
}
```

---

## 🏗️ Architecture

### Service 1: Contract Drafting

```
Request → ingestion_agent → LLM → Response
```

**Agents Used:**
- ✅ `ingestion_agent` - Normalizes input data
- ✅ LLM (Gemini) - Generates contract

**No pipeline, no other agents involved.**

---

### Service 2: Compliance Check

```
Request → clause_agent → [for each clause]:
  compliance_agent (RAG retrieval + Gemini prompt) → risk_agent
  → Aggregator → Markdown Report
```

**Agents Used:**
- ✅ `clause_agent` - Splits contract into clauses
- ✅ `compliance_agent` - Combines RAG retrieval (FAISS + statutes) with Gemini analysis
- ✅ `risk_agent` - Classifies risk level
- ✅ Markdown composer - Generates executive summary + action list for frontend editor

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── agents/              # AI Agents
│   │   ├── ingestion_agent.py
│   │   ├── clause_agent.py
│   │   ├── compliance_agent.py
│   │   ├── risk_agent.py
│   │   └── merge_agent.py
│   ├── api/                 # API Endpoints
│   │   ├── drafting.py      # Contract drafting endpoint
│   │   ├── compliance.py    # Compliance check endpoint
│   │   └── health.py        # Health check
│   ├── llms/                # LLM Clients
│   │   └── gemini_client.py
│   ├── schemas/             # Pydantic Schemas
│   │   └── __init__.py
│   ├── rag/                 # RAG (to be added by teammate)
│   └── utils/               # Utility functions
├── legal_texts/             # Legal reference documents
│   └── us_contract_law_basics.md
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── README.md               # This file
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash-exp

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS Origins
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Logging
LOG_LEVEL=INFO
```

### Legal Reference Files

Add legal reference documents to `legal_texts/` directory:

```bash
legal_texts/
├── us_contract_law_basics.md
├── gdpr_compliance.txt
├── hipaa_requirements.md
└── ...
```

Supported formats: `.txt`, `.md`

---

## 🧪 Testing

### Test with cURL

```bash
# Health check
curl http://localhost:8000/api/health

# Draft contract
curl -X POST http://localhost:8000/api/drafting/draft \
  -H "Content-Type: application/json" \
  -d @test_draft.json

# Check compliance
curl -X POST http://localhost:8000/api/compliance/check \
  -H "Content-Type: application/json" \
  -d @test_compliance.json
```

### Test with Python

```python
import requests

# Draft contract
response = requests.post(
    "http://localhost:8000/api/drafting/draft",
    json={
        "party_a": "Test Corp",
        "party_b": "Example Inc",
        "jurisdiction": "United States",
        "requirements": "Create a simple service agreement"
    }
)
print(response.json())

# Check compliance
response = requests.post(
    "http://localhost:8000/api/compliance/check",
    json={
        "contract_text": "Your contract text here...",
        "jurisdiction": "United States"
    }
)
print(response.json())
```

---

## 🔍 API Response Formats

### Success Response (Drafting)
```json
{
  "drafted_contract": "string (Markdown)",
  "compliance_report": [],
  "metadata": {
    "parties": [...],
    "jurisdiction": "string",
    "purpose": "string",
    "term": "string"
  }
}
```

### Success Response (Compliance)
```json
{
  "drafted_contract": "string (original)",
  "compliance_report": [
    {
      "clause": "string",
      "risk_level": "low|medium|high",
      "fix": "string",
      "citations": ["string"]
    }
  ],
  "summary": {
    "total_clauses": 0,
    "high_risk": 0,
    "medium_risk": 0,
    "low_risk": 0,
    "overall_assessment": "string"
  }
}
```

### Error Response
```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```

---

## 🚦 Status Codes

- `200` - Success
- `400` - Bad Request (invalid input)
- `500` - Internal Server Error

---

## 📚 Documentation

- **Agent Documentation**: `app/agents/README.md`
- **Agent Examples**: `app/agents/examples.py`
- **Quick Start**: `QUICKSTART.md`

---

## 🔗 Integration with Frontend

The frontend should call these endpoints:

```typescript
// Contract Drafting
const response = await fetch('http://localhost:8000/api/drafting/draft', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    party_a: "Acme Corp",
    party_b: "Example Inc",
    jurisdiction: "United States",
    requirements: "..."
  })
});

// Compliance Check
const response = await fetch('http://localhost:8000/api/compliance/check', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    contract_text: "...",
    jurisdiction: "United States"
  })
});

// Structured Insight
const response = await fetch('http://localhost:8000/api/reports/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    task_type: 'case-summary',
    content: 'Facts or clauses to analyze'
  })
});
```

Set the frontend environment variable `VITE_API_BASE_URL` to point at the backend origin (e.g., `http://localhost:8000`) so every AI page proxies requests through the API instead of calling Gemini directly.
```

---

## 🛠️ Development

### Run in Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### View Logs

Logs are printed to console. Configure log level in `.env`:

```bash
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR
```

---

## 📝 Notes

- **RAG**: To be implemented by teammate in `app/rag/`
- **LLM**: Uses Gemini API (compatible with frontend)
- **Legal Texts**: Add more reference files to `legal_texts/` for better compliance analysis
- **No Vector DB**: Uses keyword-based search only
- **Async**: All agents use async functions

---

## ✅ Ready to Use

All components are production-ready:
- ✅ 5 AI Agents implemented
- ✅ 2 API endpoints (drafting + compliance)
- ✅ LLM client (Gemini)
- ✅ Request/response validation
- ✅ Error handling
- ✅ CORS configured
- ✅ API documentation

---

## 🎉 Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Set your `GEMINI_API_KEY` in `.env`
3. Run: `python -m app.main`
4. Visit: http://localhost:8000/docs

**Your backend is ready!** 🚀
