# LegalContractAI - AI-Powered Legal Contract Platform

A sophisticated, full-stack AI-powered platform for drafting, analyzing, and managing legal contracts. Built with a React frontend and FastAPI backend, leveraging advanced LLMs (Open AI) and RAG (Retrieval-Augmented Generation) for intelligent legal document management.

## 🎯 Overview

LegalContractAI is an end-to-end solution that combines:

- **Intelligent Contract Drafting**: Generate professional legal contracts using AI agents and templates
- **Compliance Analysis**: Real-time compliance checking against legal statutes and regulations
- **Risk Assessment**: Identify potential loopholes and high-risk clauses
- **Document Management**: Store, retrieve, and manage legal documents with Supabase integration
- **RAG Integration**: Access thousands of legal documents through semantic search
- **Multi-Jurisdiction Support**: Support for different legal jurisdictions (US, India, etc.)

### Key Features

- 📝 **Contract Drafting** - Generate contracts from templates and requirements
- ✅ **Compliance Checking** - Analyze contracts against legal requirements
- 🔍 **Clause Classification** - Categorize and analyze contract clauses
- ⚠️ **Risk Detection** - Identify loopholes and problematic terms
- 📊 **Report Generation** - Create detailed analysis reports
- 💬 **Interactive Chat** - Conversational AI for legal queries
- 🔐 **Secure Storage** - Encrypted storage with Supabase backend
- 📈 **Usage Analytics** - Track API usage and credit consumption

---

## 📁 Project Structure

```
LegalContractAI/
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── main.py            # FastAPI entry point
│   │   ├── config.py          # Configuration management
│   │   ├── agents/            # AI agents for legal tasks
│   │   │   ├── ingestion_agent.py
│   │   │   ├── clause_agent.py
│   │   │   ├── compliance_agent.py
│   │   │   ├── risk_agent.py
│   │   │   ├── merge_agent.py
│   │   │   ├── drafting_agent.py
│   │   │   ├── structure_agent.py
│   │   │   ├── template_agent.py
│   │   │   └── ...
│   │   ├── api/               # API route handlers
│   │   │   ├── drafting.py
│   │   │   ├── compliance.py
│   │   │   ├── analysis.py
│   │   │   ├── chat.py
│   │   │   ├── reports.py
│   │   │   ├── research.py
│   │   │   └── ...
│   │   ├── llms/              # LLM client implementations
│   │   │   ├── gemini_client.py
│   │   │   ├── openai_client.py
│   │   │   ├── hybrid_client.py
│   │   │   └── prompts/
│   │   ├── services/          # Business logic services
│   │   │   ├── draft_service.py
│   │   │   ├── compliance_service.py
│   │   │   ├── insight_service.py
│   │   │   ├── supabase_service.py
│   │   │   └── encryption.py
│   │   ├── RAG/               # Retrieval-Augmented Generation
│   │   │   └── pinecone_store.py
│   │   ├── schemas/           # Pydantic data models
│   │   ├── utils/             # Utility functions
│   │   └── pdf_templates/     # Contract templates by type
│   ├── legal_texts/           # Legal reference documents
│   ├── scripts/               # Utility scripts
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment variables template
│   └── README.md              # Backend documentation
│
├── frontend/                   # React + TypeScript frontend
│   ├── src/
│   │   ├── components/        # UI components
│   │   │   ├── ui/            # shadcn/ui primitives
│   │   │   ├── AIForm.tsx
│   │   │   ├── AICredits.tsx
│   │   │   ├── GeneratedReport.tsx
│   │   │   └── ...
│   │   ├── pages/             # Route pages
│   │   │   ├── ContractDrafting.tsx
│   │   │   ├── ComplianceCheck.tsx
│   │   │   ├── LoopholeDetection.tsx
│   │   │   └── ...
│   │   ├── lib/               # Utilities and clients
│   │   │   ├── ai-clients.ts
│   │   │   ├── supabase.ts
│   │   │   └── ...
│   │   ├── hooks/             # Custom React hooks
│   │   ├── contexts/          # React contexts
│   │   ├── services/          # API services
│   │   ├── types/             # TypeScript interfaces
│   │   ├── App.tsx            # Root component
│   │   └── main.tsx           # Entry point
│   ├── public/                # Static assets
│   ├── package.json           # Frontend dependencies
│   ├── vite.config.ts         # Vite configuration
│   ├── tailwind.config.ts     # Tailwind CSS config
│   ├── tsconfig.json          # TypeScript configuration
│   └── README.md              # Frontend documentation
│
└── docs/                      # Additional documentation
    └── ...
```

---

## 🚀 Quick Start

### Prerequisites

- **Node.js**: 18+ (with npm, yarn, or bun)
- **Python**: 3.10+ (with pip and virtual environment)
- **Git**: For version control
- **API Keys**:
  - OpenAI API key 
  - Google Generative AI (Gemini) API key (optional)
  - Pinecone API key (optional, for RAG)
  - Supabase credentials (optional, for persistence)

### Setup Instructions

#### 1. Clone the Repository

```bash
git clone <repository-url> LegalContractAI
cd LegalContractAI
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your API keys
# GOOGLE_API_KEY=your_gemini_api_key (optional)
# OPENAI_API_KEY=your_openai_api_key 
# PINECONE_API_KEY=your_pinecone_key (optional)
# SUPABASE_URL=your_supabase_url (optional)
# SUPABASE_KEY=your_supabase_key (optional)
```

#### 3. Start the Backend

```bash
# From backend directory
python -m app.main
# Or
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

#### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
# or
pnpm install
# or
bun install

# Create .env file
cat > .env << EOF
VITE_API_BASE_URL=http://localhost:8000
VITE_DEFAULT_CREDITS=5
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
EOF
```

#### 5. Start the Frontend

```bash
# From frontend directory
npm run dev
# or
pnpm dev
# or
bun dev
```

The application will be available at `http://localhost:5173`

---

## 📚 Architecture Overview

### Technology Stack

#### **Backend**
- **Framework**: FastAPI (Python web framework)
- **Server**: Uvicorn (ASGI server)
- **AI/ML**: 
  - Open AI models
  - LangChain (LLM orchestration)
  - Pinecone (Vector database for RAG)
  - Sentence Transformers (Embeddings)
- **Data Storage**: 
  - Supabase (PostgreSQL + Auth + Storage)
  - Pinecone (Vector search)
- **Data Validation**: Pydantic
- **Async Support**: AsyncIO, aiohttp

#### **Frontend**
- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite (lightning-fast builds)
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui (Radix UI primitives)
- **State Management**: React Context API, TanStack Query
- **HTTP Client**: Fetch API, axios
- **Backend Integration**: Supabase SDK
- **Form Handling**: React Hook Form

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
│          (Vite + TypeScript + Tailwind + shadcn)            │
├─────────────────────────────────────────────────────────────┤
│                      HTTP/REST API                           │
├─────────────────────────────────────────────────────────────┤
│                   Backend (FastAPI)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Routes (Drafting, Compliance, Analysis, etc.)  │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  AI Agents (Ingestion, Clause, Compliance, Risk)    │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  LLM Clients (Gemini, OpenAI, Hybrid)               │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │  Services (Draft, Compliance, Encryption, RAG)      │  │
│  └──────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│              External Services & Databases                  │
│  ┌─────────────┬──────────────┬─────────────────────┐      │
│  │Open AI Model│  Pinecone    │   Supabase          │      │
│  │   (LLMs)    │ (Vector DB)  │ (Data + Auth)       │      │
│  └─────────────┴──────────────┴─────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Contract Drafting**:
   ```
   User Input → Frontend → API Endpoint → Ingestion Agent → 
   LLM (OpenAI) → Response → Frontend Display
   ```

2. **Compliance Checking**:
   ```
   Contract Text → Clause Agent (split clauses) → 
   Compliance Agent (RAG + LLM analysis) → Risk Agent (classify) → 
   Report Generator → JSON Response
   ```

3. **RAG-Enhanced Analysis**:
   ```
   Query → Embedding (Sentence Transformer) → Vector Search (Pinecone) →
   Retrieved Documents → LLM with Retrieved Context → Response
   ```

---

## 🔌 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/drafting/draft` | Generate contract |
| POST | `/api/compliance/check` | Analyze compliance |
| POST | `/api/analysis/analyze` | General analysis |
| POST | `/api/reports/generate` | Generate reports |
| POST | `/api/research/query` | Research query |
| POST | `/api/summarization/summarize` | Summarize documents |
| POST | `/api/chat/message` | Chat interaction |
| GET | `/api/usage/stats` | Usage statistics |

### Request/Response Examples

#### Contract Drafting

```bash
curl -X POST http://localhost:8000/api/drafting/draft \
  -H "Content-Type: application/json" \
  -d '{
    "party_a": "Acme Corporation",
    "party_b": "Example Industries Inc.",
    "jurisdiction": "United States",
    "purpose": "Service Agreement",
    "term": "24 months",
    "requirements": "Software development services with confidentiality clause"
  }'
```

#### Compliance Check

```bash
curl -X POST http://localhost:8000/api/compliance/check \
  -H "Content-Type: application/json" \
  -d '{
    "contract_text": "Your contract text here...",
    "jurisdiction": "United States"
  }'
```

---

## 🛠️ Development Guide

### Backend Development

#### Running in Development Mode

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Creating New Agents

Agents follow a common pattern:

```python
from app.agents.state import AgentState
from langchain_google_genai import ChatGoogleGenerativeAI

async def my_new_agent(state: AgentState) -> AgentState:
    """Process the state and update it with results."""
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")
    
    # Your logic here
    result = await llm.ainvoke(state.input)
    
    state.output = result
    return state
```

#### Creating New API Endpoints

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/my-feature", tags=["my-feature"])

class MyRequest(BaseModel):
    input_field: str

@router.post("/endpoint")
async def my_endpoint(request: MyRequest):
    try:
        # Your logic here
        result = await process_request(request)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Frontend Development

#### Component Development

```typescript
// Using shadcn/ui components
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export const MyComponent = () => {
  return (
    <div className="p-4">
      <Input placeholder="Enter text" />
      <Button>Submit</Button>
    </div>
  );
};
```

#### API Integration

```typescript
// Using the AI client
import { aiClient } from "@/lib/ai-clients";

const response = await aiClient.post("/drafting/draft", {
  party_a: "Company A",
  party_b: "Company B",
  requirements: "..."
});
```

#### Adding New Pages

1. Create component in `src/pages/`
2. Add route in `src/App.tsx`
3. Update navigation in `src/components/Header.tsx`

---

## 🔐 Security Considerations

- **API Keys**: Store all sensitive keys in `.env` files (never commit to git)
- **Encryption**: PayloadChat messages are encrypted using AES encryption
- **CORS**: Configured to only allow trusted origins
- **Input Validation**: All inputs validated with Pydantic
- **Authentication**: Optional Supabase authentication
- **Rate Limiting**: Implemented to prevent abuse

### Environment Variables Best Practices

```bash
# .env (never commit)
GOOGLE_API_KEY=sk-xxx
OPENAI_API_KEY=sk-xxx
PINECONE_API_KEY=pk-xxx
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=xxx
CHAT_ENCRYPTION_KEY_V1=xxx

# Frontend .env
VITE_API_BASE_URL=http://localhost:8000
VITE_SUPABASE_URL=https://xxx.supabase.co
VITE_SUPABASE_ANON_KEY=xxx
```

---

## 📊 Database Schema

### Key Tables (Supabase)

- **contracts**: Stored contracts with metadata
- **compliance_reports**: Compliance analysis results
- **chat_history**: Encrypted chat messages
- **usage_logs**: API usage tracking
- **templates**: Contract templates

---

## 🧪 Testing

### Backend Testing

```bash
cd backend

# Run tests
pytest tests/ -v

# Run specific test file
pytest tests/test_api.py -v

# Run with coverage
pytest --cov=app tests/
```

### Frontend Testing

```bash
cd frontend

# Run linting
npm run lint

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 📦 Deployment

### Backend Deployment

Options:
- **Heroku**: `git push heroku main`
- **Railway**: Connect GitHub repo
- **Docker**: Build with included Dockerfile
- **AWS EC2**: Deploy with systemd/supervisor

### Frontend Deployment

Options:
- **Vercel**: Deploy directly from GitHub
- **Netlify**: Connect repository
- **AWS S3 + CloudFront**: Static hosting
- **Docker**: Run in container

### Docker Deployment

```bash
# Build backend image
docker build -f backend/Dockerfile -t legalcontractai-backend .

# Build frontend image
docker build -f frontend/Dockerfile -t legalcontractai-frontend .

# Run with docker-compose
docker-compose up -d
```

---

## 🗺️ Roadmap

### Planned Features

- [ ] Multi-language support
- [ ] Advanced document comparison
- [ ] Automated contract renewal reminders
- [ ] Team collaboration features
- [ ] Advanced audit trail logging
- [ ] Mobile app (React Native)
- [ ] Blockchain verification of contracts
- [ ] Custom model fine-tuning

---

## 🤝 Contributing

We welcome contributions! Here's how to help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Contribution Guidelines

- Follow PEP 8 (Python) and ESLint (TypeScript) conventions
- Write clear commit messages
- Add tests for new features
- Update documentation as needed
- Keep PRs focused and manageable

---

## 📖 Additional Resources

- [Backend Documentation](./backend/README.md)
- [Frontend Documentation](./frontend/README.md)
- [API Documentation](http://localhost:8000/docs) (Swagger UI)
- [Open AI API docs :](https://developers.openai.com/api/reference/overview/)
- [Google Generative AI Docs](https://ai.google.dev)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [React Docs](https://react.dev)
- [Tailwind CSS Docs](https://tailwindcss.com)

---

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## 🆘 Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Find and kill process on port 8000
lsof -i :8000
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

**Import errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**API key errors:**
```bash
# Verify .env file exists and contains valid keys
cat .env
```

### Frontend Issues

**Module not found:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Port 5173 already in use:**
```bash
# Vite will automatically try next port or specify manually
npm run dev -- --port 5174
```

---

## 📞 Support & Community

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Email**: support@legalcontractai.com

---

**Last Updated**: February 2026  
**Version**: 1.0.0

