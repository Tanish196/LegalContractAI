# LegalContractAI Frontend

A modern, responsive React + TypeScript application for AI-powered legal document assistance. The frontend provides an intuitive interface for contract drafting, clause classification, compliance checking, loophole detection, and case summarization. All AI workloads are securely proxied through our FastAPI backend, which handles Generative AI access, RAG retrieval, and comprehensive auditing.

Built with **Vite + React + TypeScript**, styled with **Tailwind CSS**, and enhanced with **shadcn/ui** components for a professional, accessible user experience.

This README explains setup, usage, architecture, and development guidelines.

## Table of contents

- About
- Features
- Requirements
- Quick start
- Environment variables
- Available scripts
- Project structure
- Development notes
- Contributing
- License

## About

This application provides a comprehensive UI for AI-assisted legal tasks, powered by a sophisticated backend API. It demonstrates professional-grade integration patterns for legal document processing:

- **Contract Drafting** - AI-generated contracts from templates and requirements
- **Clause Classification** - Intelligent categorization and analysis of contract terms
- **Compliance Checking** - Real-time compliance analysis against legal statutes
- **Loophole Detection** - Identification of risky terms and legal gaps
- **Case Summarization** - Automated summarization of legal documents
- **Research Queries** - Semantic search over legal knowledge base
- **Interactive Chat** - Conversational AI for legal questions

**Architecture**: All AI operations are delegated to the FastAPI backend, which provides:
- Multi-LLM support (Google Gemini, OpenAI) with intelligent routing
- RAG (Retrieval-Augmented Generation) via Pinecone vector database
- Persistent storage with Supabase (PostgreSQL + Auth)
- Encrypted message storage for chat history
- Usage tracking and credit-based billing

**Built With**:
- **Frontend**: Vite + React 18+ + TypeScript
- **Styling**: Tailwind CSS + shadcn/ui (accessible, customizable components)
- **State**: React Context API + TanStack Query for server state
- **HTTP**: Fetch API with intelligent error handling
- **Backend Integration**: Fully typed API client with endpoint routing
- **Database**: Optional Supabase for persistence and authentication

## Features

- **Pre-built Pages** - Dedicated pages for each legal task in `src/pages/`
- **Reusable Components** - UI primitives and layouts in `src/components/`
- **Backend-First Architecture** - All AI requests proxy through FastAPI backend
- **Smart API Client** - Fully typed API client (`src/lib/ai-clients.ts`) with endpoint routing
- **Authentication** - Optional Supabase auth integration for user accounts
- **Persistent Storage** - User documents and chat history stored in Supabase (optional)
- **Dark/Light Mode** - Built-in theme support via Tailwind Dark Mode
- **Responsive Design** - Mobile-first, works on all screen sizes
- **Error Handling** - Comprehensive error boundaries and user feedback
- **Credit-Based System** - Configurable daily credit allocation per user
- **Rate Limiting** - Client-side rate limiting to prevent API abuse
- **Accessibility** - WCAG 2.1 compliant with shadcn/ui primitives

## Requirements

- Node.js (18+ recommended)
- npm, yarn, or bun (project was bootstrapped with Vite)

Note: This repository includes a `bun.lockb` but the project works with npm/yarn as well. Use your preferred package manager.

## Quick start

1. Clone the repository

```powershell
git clone <repo-url> "legal-contract-app"
cd "legal-contract-app"
```

2. Install dependencies

```powershell
npm install
# or
pnpm install
# or
bun install
```

3. Create a `.env` file at the project root (see Environment variables below)

4. Start the dev server

```powershell
npm run dev
# or with pnpm/bun
pnpm dev; bun dev
```

Open `http://localhost:5173` (Vite default) in your browser.

## Environment Variables

Create a `.env` file in the project root. Vite expects variables prefixed with `VITE_`.

### Required Variables

- `VITE_API_BASE_URL` (**required**) — Base URL of the FastAPI backend (e.g., `http://localhost:8000`). All AI requests are proxied through this backend.

### Optional Variables

- `VITE_DEFAULT_CREDITS` (optional) — Default number of free credits allocated per user per day (default: `5`)
- `VITE_SUPABASE_URL` (optional) — Supabase project URL for persistent storage (e.g., `https://project.supabase.co`)
- `VITE_SUPABASE_ANON_KEY` (optional) — Supabase anonymous/public key for client-side access

### Example `.env` File

```text
# Backend Configuration (Required)
VITE_API_BASE_URL=http://localhost:8000

# Optional: Credit System
VITE_DEFAULT_CREDITS=5

# Optional: Database & Auth
VITE_SUPABASE_URL=https://example.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIs...
```

### Important Security Notes

- **Never commit `.env` files** to version control
- **Secrets (API keys, etc.) live on the backend** - not in frontend code
- **Supabase keys are safe** - anon keys are intentionally public and row-level secured
- **CORS must be configured** on the backend to allow your frontend origin
- **HTTPS in production** - always use HTTPS when deploying frontend and backend

## Available scripts

Scripts are defined in `package.json`. Use them through your package manager, e.g. `npm run <script>`.

- `dev` — start Vite dev server
- `build` — build production assets with Vite
- `build:dev` — build using the `development` mode
- `preview` — locally preview the production build
- `lint` — run ESLint

Examples (PowerShell):

```powershell
npm run dev
npm run build
npm run preview
npm run lint
```

## Project Structure

```
src/
├── components/              # React Components
│   ├── ui/                 # shadcn/ui primitives (Button, Input, Card, etc.)
│   ├── AIForm.tsx          # AI task input form
│   ├── AICredits.tsx       # Credit display and management
│   ├── GeneratedReport.tsx # Report display component
│   ├── Header.tsx          # Navigation header
│   └── ...                 # Additional components
│
├── pages/                  # Route Pages (each with dedicated legal task)
│   ├── ContractDrafting.tsx        # Contract generation interface
│   ├── ComplianceCheck.tsx         # Compliance analysis interface
│   ├── LoopholeDetection.tsx       # Risk detection interface
│   ├── CaseSummary.tsx             # Document summarization
│   ├── ClauseClassification.tsx    # Clause analysis
│   └── ...
│
├── lib/                    # Utilities and API Clients
│   ├── ai-clients.ts      # Backend API client with full endpoint routing
│   ├── supabase.ts        # Supabase client initialization
│   └── ...
│
├── hooks/                  # Custom React Hooks
│   ├── useCredits.ts      # Credit management hook
│   ├── useApi.ts          # API calling hook
│   └── ...
│
├── contexts/               # React Context API Providers
│   ├── AuthContext.tsx    # Authentication context
│   ├── CreditContext.tsx  # Credit system context
│   └── ...
│
├── services/               # API Services (higher-level)
│   ├── contractService.ts
│   ├── complianceService.ts
│   └── ...
│
├── types/                  # TypeScript Type Definitions
│   ├── api.ts             # API request/response types
│   ├── legal.ts           # Legal domain types
│   └── ...
│
├── App.tsx                 # Root component with routing
├── main.tsx               # Vite entry point
├── index.css              # Global styles
└── vite-env.d.ts          # Vite type definitions

public/                     # Static assets
├── index.html             # HTML template
├── robots.txt             # SEO
└── assets/                # Images, icons, etc.

package.json              # Dependencies and scripts
tailwind.config.ts        # Tailwind CSS configuration
tsconfig.json             # TypeScript configuration
vite.config.ts            # Vite build configuration
```

## Development Notes

### Key Files & APIs

- **`src/lib/ai-clients.ts`** — Central backend API client. All LegalContractAI endpoints are routed here. Modify this file to add new endpoints or change request/response handling.

- **`src/lib/supabase.ts`** — Supabase client initialization. Exports a Supabase client instance or `null` if env vars are missing. Components should use null-safe patterns when accessing.

### Important Development Patterns

1. **Backend-First Architecture**
   - Never call Gemini/OpenAI API directly from the frontend
   - All AI requests must go through `VITE_API_BASE_URL`
   - The backend handles authentication, rate limiting, and audit logging

2. **Type Safety**
   - All API requests/responses are fully typed in TypeScript
   - Check `src/types/api.ts` for request/response interfaces
   - Use strict null checking to avoid runtime errors

3. **Error Handling**
   - Use error boundaries for graceful error display
   - Log errors to console for debugging
   - Provide user-friendly error messages in the UI

4. **Component Development**
   ```typescript
   // ✅ Good: Use shadcn/ui primitives and Tailwind
   import { Button } from "@/components/ui/button";
   import { Input } from "@/components/ui/input";

   export const MyComponent = () => {
     return (
       <div className="p-4 space-y-4">
         <Input placeholder="Enter text" />
         <Button>Submit</Button>
       </div>
     );
   };
   ```

5. **API Integration**
   ```typescript
   // ✅ Good: Use the AI client from lib
   import { aiClient } from "@/lib/ai-clients";

   const response = await aiClient.post("/drafting/draft", {
     party_a: "Company A",
     party_b: "Company B",
     requirements: "..."
   });
   ```

6. **State Management**
   - Use React Context for global state (auth, credits, theme)
   - Use TanStack Query for server state caching
   - Use local state (useState) for component-level data

7. **Adding New Pages**
   1. Create `src/pages/MyNewPage.tsx`
   2. Add route in `src/App.tsx`
   3. Add navigation link in `src/components/Header.tsx`
   4. Implement using existing components and hooks

### Performance Optimization

- **Code Splitting**: Vite automatically code-splits on route boundaries
- **Image Optimization**: Use appropriate formats (WebP, etc.)
- **Query Caching**: TanStack Query handles server-state caching
- **Lazy Loading**: Use React.lazy() for large components

### Supabase Integration

If Supabase is configured, the following features are available:

```typescript
import { supabase } from "@/lib/supabase";

// Fetch stored contracts
const { data, error } = await supabase
  .from("contracts")
  .select("*")
  .eq("user_id", userId);

// Listen for real-time updates
const subscription = supabase
  .from("chat_history")
  .on("*", (payload) => console.log("New message:", payload))
  .subscribe();
```

## Backend API Integration

This frontend communicates with a FastAPI backend that provides the following endpoints:

| Task | Endpoint | Method |
|------|----------|--------|
| Contract Drafting | `/api/drafting/draft` | POST |
| Compliance Check | `/api/compliance/check` | POST |
| Report Generation | `/api/reports/generate` | POST |
| General Analysis | `/api/analysis/analyze` | POST |
| Research Query | `/api/research/query` | POST |
| Summarization | `/api/summarization/summarize` | POST |
| Chat | `/api/chat/message` | POST |
| Usage Stats | `/api/usage/stats` | GET |
| Health Check | `/api/health` | GET |

**See [Backend Documentation](../backend/README.md) for detailed endpoint specifications and example payloads.**

### Request/Response Example

```typescript
// Drafting Contract
const response = await aiClient.post("/drafting/draft", {
  party_a: "Acme Corporation",
  party_b: "Example Industries Inc.",
  jurisdiction: "United States",
  purpose: "Service Agreement",
  requirements: "Software development services..."
});

// Response
{
  drafted_contract: "# SERVICE AGREEMENT\n\n...",
  compliance_report: [],
  metadata: { ... }
}
```

**Backend must be running on `VITE_API_BASE_URL` for the frontend to work properly.**

---

## Testing & Quality

### Linting

```powershell
npm run lint
```

ESLint checks code quality and style. Fix issues with:

```powershell
npm run lint -- --fix
```

### Building for Production

```powershell
npm run build      # Create optimized production build
npm run preview    # Preview production build locally
```

### CI/CD Recommendations

Before merging PRs, ensure:

```powershell
npm ci              # Clean install of dependencies
npm run build       # Build succeeds
npm run lint        # No lint errors
```

Consider adding:
- Unit tests (Jest, Vitest)
- E2E tests (Cypress, Playwright)
- Pre-commit hooks (husky)

---

## Deployment

### Quick Deployment Options

#### **Vercel (Recommended)**
```powershell
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

Vercel automatically:
- Builds your project
- Optimizes images and assets
- Provides global CDN
- Supports preview deployments

#### **Netlify**
```powershell
# Connect via GitHub
# Netlify auto-builds on push
```

#### **Docker (Self-Hosted)**
```dockerfile
# Dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/dist ./dist
CMD ["serve", "-s", "dist"]
```

```bash
docker build -t legalcontractai-frontend .
docker run -p 3000:3000 -e VITE_API_BASE_URL=<backend-url> legalcontractai-frontend
```

### Environment Configuration

When deploying:
1. Set `VITE_API_BASE_URL` to your backend URL
2. Set `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` (if using Supabase)
3. Ensure backend CORS allows your frontend origin
4. Use HTTPS in production

---

## Contributing

We welcome contributions! Here's how to help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Contribution Guidelines

- Follow ESLint rules: `npm run lint`
- Build successfully: `npm run build`
- Keep changes focused and small
- Write clear commit messages
- Test your changes locally
- Update documentation as needed
- Add TypeScript types for new code

### Code Style

- Use TypeScript for type safety
- Follow the existing component patterns
- Use shadcn/ui components for UI
- Use Tailwind CSS for styling
- Keep components small and focused
- Write descriptive variable/function names

---

## License

MIT License - See the main [LICENSE](../LICENSE) file for details.

---

## Additional Resources

- **[Main Project README](../README.md)** - Complete project overview
- **[Backend Documentation](../backend/README.md)** - Backend API details
- **[Backend DOCKER_SETUP](../DOCKER_SETUP.md)** - Docker deployment guide
- **[React Official Docs](https://react.dev)** - React framework docs
- **[Vite Docs](https://vitejs.dev)** - Build tool documentation
- **[Tailwind CSS Docs](https://tailwindcss.com)** - CSS framework
- **[shadcn/ui Docs](https://ui.shadcn.com)** - Component library
- **[TypeScript Docs](https://www.typescriptlang.org)** - Type system
- **[Supabase Docs](https://supabase.com/docs)** - Database & Auth

---

**Last Updated**: February 16, 2026  
**Version**: 1.0.0


