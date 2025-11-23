# LegalContractAI Integration & Experience Plan

## 1. Objectives
- Replace direct frontend → Gemini calls with a unified backend API so the product has one source of truth for prompts, auditing, and RAG capabilities.
- Attach the existing RAG pipeline to the compliance flow to ground outputs in curated statutes and improve legal defensibility.
- Elevate the reviewer experience with rich viewing, inline editing, and PDF/DOCX export so attorneys can act on insights quickly.
- Introduce prompt-engineering guardrails that produce structured, high-value reports suitable for legal professionals.

## 2. Scope Overview
| Track | Key Deliverables |
| --- | --- |
| Backend | RAG-backed compliance agent, richer prompts, REST responses tailored for UI consumption |
| Frontend | API client for backend services, structured document viewer + editor, export utilities |
| Documentation | Updated backend README, new RAG usage notes, frontend instructions for environment + API integration |

## 3. Backend Technical Approach
1. **RAG Attachment**
   - Expose `get_rag_response` inside `compliance_agent` as a retrieval layer before LLM scoring.
   - Reuse retrieved chunks as authoritative citations and feed them into the structured prompt template.
   - Cache retriever + embeddings to avoid rebuilding per request.
2. **Compliance Service Changes**
   - Expand the compliance response to include `drafted_contract`, `compliance_report`, and `insights` (executive summary, action list) for UI rendering.
   - Ensure each clause result carries `title`, `issue`, `risk_level`, `recommendation`, and `citations` fields.
3. **Prompt Engineering**
   - Build a single JSON-first prompt for compliance summarization that enforces sections: Executive Summary, Clause-by-Clause Analysis, Action Checklist, and Template Suggestions.
   - Add temperature / token controls for predictable, audit-friendly results.
4. **API Surface**
   - Add `/api/reports/preview` endpoint (FastAPI router) returning the structured payload consumed by the frontend.
   - Enable CORS for Vite dev port and production origin, using env `CORS_ORIGINS`.

## 4. Frontend Technical Approach
1. **API Client Refactor**
   - Replace `aiClient.process` usage with a typed SDK that hits backend endpoints (drafting + compliance). Keep Supabase credit tracking unchanged.
   - Handle streaming or long-running operations with loading states and error surfaces.
2. **Document Experience**
   - Create `GeneratedDocumentPanel` component that:
     - Renders backend JSON as headers/subheaders/bullets using semantic tokens.
     - Provides an editable markdown/HTML textarea (e.g., `react-ace` or controlled textarea) with change tracking.
     - Offers an export toolbar with `Download as PDF/DOCX` actions.
   - Use `html2pdf.js` (for PDF) and `docx` npm package for Word exports.
3. **State Management**
   - Centralize task submission + data storage in context so multiple pages (Compliance, Drafting) reuse the same viewer/editor.
4. **Accessibility & UX**
   - Provide toast feedback for exports, use `Skeleton` components during load, and keep typography consistent (headings, lists, definition blocks).

## 5. Documentation Deliverables
- `backend/README.md`: add RAG instructions, environment requirements, and API contract for the new endpoints.
- `backend/app/RAG/README.md`: describe dataset expectations, retriever tuning, and local setup.
- `frontend/README.md`: document backend integration, required env vars (`VITE_API_BASE_URL`), and build steps.

## 6. Testing Strategy
- **Backend**: pytest unit tests for compliance service, plus integration tests hitting the FastAPI test client with sample contracts.
- **Frontend**: React Testing Library coverage for the viewer/editor component and API client mocks.
- **E2E Manual**: Run through drafting → edit → export flows using sample data to ensure parity across browsers.

## 7. Risks & Mitigations
- **Large Docs**: Ensure retriever chunking and FAISS index are persisted or cached; add guardrails on request size.
- **PDF/DOCX Rendering**: Validate fonts/assets in SSR contexts; provide fallback plain-text export if library fails.
- **LLM Variability**: Enforce JSON schema validation and fail-safe messaging in UI when parsing errors occur.

## 8. Timeline (High-Level)
1. Day 1-2: Backend RAG integration + prompt refinement.
2. Day 3: API contract updates, documentation, automated tests.
3. Day 4-5: Frontend client swap, viewer/editor/export components, QA.

This plan should be revisited after backend wiring is complete to capture any new dependencies discovered during implementation.
