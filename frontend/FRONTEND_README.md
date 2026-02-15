# LegalContractAI Frontend - Comprehensive Documentation

## 📖 Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Project Structure](#project-structure)
4. [Setup & Installation](#setup--installation)
5. [Configuration](#configuration)
6. [Component Architecture](#component-architecture)
7. [Pages & Routes](#pages--routes)
8. [API Integration](#api-integration)
9. [State Management](#state-management)
10. [Styling & UI](#styling--ui)
11. [Optional Features](#optional-features)
12. [Development Workflow](#development-workflow)
13. [Building for Production](#building-for-production)
14. [Troubleshooting](#troubleshooting)

---

## Overview

**LegalContractAI Frontend** is a modern, responsive React application built with TypeScript, Vite, and Tailwind CSS. It provides a user-friendly interface for legal professionals to:

- ✅ Draft contracts using AI templates
- ✅ Analyze existing contracts for compliance issues
- ✅ Classify clauses automatically
- ✅ Detect and highlight loopholes
- ✅ Generate detailed legal reports
- ✅ Chat with an AI legal assistant
- ✅ Manage contract templates
- ✅ Track API usage and credits

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Build Tool** | Vite | Lightning-fast bundling and HMR |
| **Framework** | React 18+ | UI component framework |
| **Language** | TypeScript | Type-safe development |
| **Styling** | Tailwind CSS | Utility-first CSS framework |
| **UI Components** | shadcn/ui | Ready-to-use React components |
| **Icons** | Material UI Icons | Rich icon library |
| **State** | React Context + TanStack Query | Application state management |
| **Forms** | React Hook Form | Efficient form handling |
| **HTTP** | Fetch API | API communication |
| **Database** | Supabase | Optional data persistence |
| **Package Manager** | npm/pnpm/bun | Dependency management |

---

## Quick Start

### 1. Prerequisites

```bash
# Required
- Node.js 18+ (with npm, yarn, or bun)
- Git for version control

# Optional but recommended
- VS Code with recommended extensions
- Postman or similar for API testing
```

### 2. Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
pnpm install
# or
bun install
```

### 3. Configuration

```bash
# Create .env file
cat > .env << EOF
VITE_API_BASE_URL=http://localhost:8000
VITE_DEFAULT_CREDITS=5
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key
EOF
```

### 4. Start Development Server

```bash
npm run dev
# or
pnpm dev
# or
bun dev
```

Open **http://localhost:5173** in your browser.

### 5. API Documentation

While frontend is running, access backend API docs at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Project Structure

```
frontend/
│
├── src/                              # Source code
│   │
│   ├── components/                   # React components
│   │   ├── ui/                       # Reusable UI primitives (shadcn/ui)
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── toast.tsx
│   │   │   └── ...
│   │   │
│   │   ├── AIForm.tsx                # AI input form component
│   │   ├── AICredits.tsx             # Credits display component
│   │   ├── GeneratedReport.tsx       # Report display component
│   │   ├── ErrorBoundary.tsx         # Error boundary wrapper
│   │   ├── Features.tsx              # Feature showcase
│   │   ├── Header.tsx                # Navigation header
│   │   ├── Hero.tsx                  # Hero section
│   │   ├── Layout.tsx                # Main layout wrapper
│   │   ├── LegalTask.tsx             # Task card component
│   │   ├── PipelineViewer.tsx        # Agent pipeline visualizer
│   │   ├── RecentActivity.tsx        # Recent activity feed
│   │   ├── ThemeProvider.tsx         # Theme context provider
│   │   └── ...
│   │
│   ├── pages/                        # Route pages
│   │   ├── ContractDrafting.tsx      # Draft new contracts
│   │   ├── ComplianceCheck.tsx       # Analyze compliance
│   │   ├── ClauseClassification.tsx  # Classify clauses
│   │   ├── LoopholeDetection.tsx     # Detect loopholes
│   │   ├── ReportGeneration.tsx      # Generate reports
│   │   ├── ChatInterface.tsx         # AI chat page
│   │   ├── Dashboard.tsx             # Main dashboard
│   │   ├── TemplateLibrary.tsx       # Template browser
│   │   └── NotFound.tsx              # 404 page
│   │
│   ├── contexts/                     # React Context
│   │   ├── AuthContext.tsx           # Authentication state
│   │   ├── AppContext.tsx            # Global app state
│   │   ├── CreditsContext.tsx        # Credits management
│   │   └── ThemeContext.tsx          # Theme selection
│   │
│   ├── hooks/                        # Custom React hooks
│   │   ├── useApi.ts                 # API calling hook
│   │   ├── useLocalStorage.ts        # Local storage hook
│   │   ├── useAuth.ts                # Authentication hook
│   │   ├── useCredits.ts             # Credits management hook
│   │   └── useTheme.ts               # Theme hook
│   │
│   ├── lib/                          # Utilities & integrations
│   │   ├── ai-clients.ts             # Backend API client
│   │   ├── supabase.ts               # Supabase initialization
│   │   ├── utils.ts                  # Helper functions
│   │   └── constants.ts              # App constants
│   │
│   ├── services/                     # Business logic services
│   │   ├── apiService.ts             # API communication
│   │   ├── contractService.ts        # Contract operations
│   │   ├── storageService.ts         # Local/Supabase storage
│   │   └── analyticsService.ts       # Usage tracking
│   │
│   ├── types/                        # TypeScript interfaces
│   │   ├── api.ts                    # API response types
│   │   ├── contract.ts               # Contract types
│   │   ├── common.ts                 # Common types
│   │   └── index.ts                  # Type exports
│   │
│   ├── App.tsx                       # Root component
│   ├── App.css                       # App styles
│   ├── main.tsx                      # Entry point
│   ├── index.css                     # Global styles
│   └── vite-env.d.ts                 # Vite environment types
│
├── public/                           # Static assets
│   ├── robots.txt
│   ├── diagnostic.html               # Diagnostic page
│   ├── react-test.html               # Test page
│   └── assets/                       # Images, fonts, etc.
│
├── index.html                        # HTML template
├── package.json                      # Dependencies & scripts
├── tsconfig.json                     # TypeScript config
├── tsconfig.app.json                 # App TypeScript config
├── tsconfig.node.json                # Node TypeScript config
├── vite.config.ts                    # Vite configuration
├── tailwind.config.ts                # Tailwind configuration
├── postcss.config.js                 # PostCSS configuration
├── eslint.config.js                  # ESLint configuration
├── components.json                   # shadcn/ui config
├── bun.lockb                         # Bun lock file
├── .eslintignore                     # ESLint ignore rules
└── README.md                         # This file
```

---

## Setup & Installation

### Detailed Installation Guide

#### 1. Clone Repository

```bash
git clone https://github.com/your-repo/LegalContractAI.git
cd LegalContractAI/frontend
```

#### 2. Install Node.js (if not already installed)

```bash
# Check Node version
node --version  # Should be 18+

# Install via:
# https://nodejs.org (recommended)
# or use nvm (Node Version Manager)
# or homebrew: brew install node
```

#### 3. Install Dependencies

Choose your preferred package manager:

```bash
# Using npm (included with Node.js)
npm install

# Using pnpm (faster, more space-efficient)
npm install -g pnpm
pnpm install

# Using bun (fastest, all-in-one)
npm install -g bun
bun install
```

#### 4. Create Environment File

```bash
# Create .env file in frontend root
cat > .env << EOF
# Backend API URL (required)
VITE_API_BASE_URL=http://localhost:8000

# Default AI credits per day (optional)
VITE_DEFAULT_CREDITS=5

# Supabase configuration (optional, for data persistence)
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key_here
EOF
```

#### 5. Verify Installation

```bash
# Check if dependencies installed correctly
npm list react react-dom typescript

# Should show versions like:
# react@18.x.x
# react-dom@18.x.x
# typescript@5.x.x
```

#### 6. Start Development Server

```bash
npm run dev

# Output should show:
# ✅ VITE v5.x.x ready in xx ms
# ➜  Local:   http://localhost:5173/
# ➜  press h to show help
```

---

## Configuration

### Environment Variables

Create `.env` file in the frontend directory:

```bash
# ==================
# Required Configuration
# ==================

# Backend API base URL (must match your backend server)
VITE_API_BASE_URL=http://localhost:8000

# ==================
# Optional Configuration
# ==================

# Daily AI credit limit per user
VITE_DEFAULT_CREDITS=5

# Supabase configuration for optional data persistence
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGc...your_anon_key

# Development settings
VITE_DEBUG=false
VITE_LOG_LEVEL=info
```

### Vite Configuration

File: `vite.config.ts`

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: false,
    open: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
  }
})
```

### TypeScript Configuration

File: `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### Tailwind CSS Configuration

File: `tailwind.config.ts`

```typescript
import type { Config } from 'tailwindcss'
import defaultTheme from 'tailwindcss/defaultTheme'

const config: Config = {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Roboto', ...defaultTheme.fontFamily.sans],
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
}

export default config
```

### ESLint Configuration

File: `eslint.config.js`

```javascript
export default [
  {
    ignores: ['dist', 'node_modules'],
  },
  {
    files: ['**/*.{js,jsx,ts,tsx}'],
    languageOptions: {
      parser: '@typescript-eslint/parser',
      parserOptions: {
        ecmaVersion: 2020,
        sourceType: 'module',
        ecmaFeatures: { jsx: true },
      },
    },
    rules: {
      'react-hooks/rules-of-hooks': 'error',
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': ['warn'],
    },
  },
]
```

---

## Component Architecture

### Component Hierarchy

```
App (Root)
├── ThemeProvider (Theme context)
├── Layout
│   ├── Header (Navigation)
│   ├── Main Content
│   │   ├── Pages (Routed via React Router)
│   │   │   ├── Dashboard
│   │   │   ├── ContractDrafting
│   │   │   ├── ComplianceCheck
│   │   │   └── ...
│   │   └── ErrorBoundary
│   └── Footer
└── Toast (Notifications)
```

### Core Components

#### **Button Component** (shadcn/ui)

```typescript
import { Button } from "@/components/ui/button"

export function MyComponent() {
  return (
    <>
      <Button>Default</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="destructive">Destructive</Button>
      <Button size="lg">Large</Button>
    </>
  )
}
```

#### **Input Component** (shadcn/ui)

```typescript
import { Input } from "@/components/ui/input"

export function MyComponent() {
  return (
    <Input 
      type="text"
      placeholder="Enter text..."
      disabled={false}
    />
  )
}
```

#### **Card Component**

```typescript
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

export function MyComponent() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Card Title</CardTitle>
        <CardDescription>Card description</CardDescription>
      </CardHeader>
      <CardContent>
        Card content goes here
      </CardContent>
    </Card>
  )
}
```

#### **Dialog Component**

```typescript
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

export function MyComponent() {
  return (
    <Dialog>
      <DialogTrigger>Open Dialog</DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Dialog Title</DialogTitle>
          <DialogDescription>
            Dialog description
          </DialogDescription>
        </DialogHeader>
        {/* Content */}
      </DialogContent>
    </Dialog>
  )
}
```

#### **Custom: AIForm**

```typescript
// src/components/AIForm.tsx
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'

export function AIForm() {
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    // Call API
    setLoading(false)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter your request..."
      />
      <Button disabled={loading}>
        {loading ? 'Processing...' : 'Submit'}
      </Button>
    </form>
  )
}
```

---

## Pages & Routes

### App Routing Structure

```typescript
// src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import ContractDrafting from './pages/ContractDrafting'
import ComplianceCheck from './pages/ComplianceCheck'
// ... other imports

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/drafting" element={<ContractDrafting />} />
          <Route path="/compliance" element={<ComplianceCheck />} />
          <Route path="/clauses" element={<ClauseClassification />} />
          <Route path="/loopholes" element={<LoopholeDetection />} />
          <Route path="/reports" element={<ReportGeneration />} />
          <Route path="/chat" element={<ChatInterface />} />
          <Route path="/templates" element={<TemplateLibrary />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}

export default App
```

### Available Pages

#### 1. **Dashboard** (`/`)
Main landing page with feature overview and quick actions.

```typescript
// src/pages/Dashboard.tsx
export default function Dashboard() {
  return (
    <div className="space-y-8">
      <Hero />
      <Features />
      <QuickActionCards />
    </div>
  )
}
```

#### 2. **Contract Drafting** (`/drafting`)
Create new contracts using AI templates.

```typescript
// src/pages/ContractDrafting.tsx
export default function ContractDrafting() {
  const [form, setForm] = useState({
    party_a: '',
    party_b: '',
    jurisdiction: 'United States',
    requirements: ''
  })
  const [draft, setDraft] = useState('')
  const [loading, setLoading] = useState(false)

  const handleDraft = async () => {
    setLoading(true)
    const response = await aiClient.post('/drafting/draft', form)
    setDraft(response.drafted_contract)
    setLoading(false)
  }

  return (
    <div className="space-y-4">
      <AIForm onSubmit={handleDraft} loading={loading} />
      {draft && <GeneratedReport content={draft} />}
    </div>
  )
}
```

#### 3. **Compliance Check** (`/compliance`)
Analyze contracts for compliance issues.

#### 4. **Clause Classification** (`/clauses`)
Categorize contract clauses automatically.

#### 5. **Loophole Detection** (`/loopholes`)
Identify problematic terms and gaps.

#### 6. **Report Generation** (`/reports`)
Create detailed analysis reports.

#### 7. **Chat Interface** (`/chat`)
Conversational AI legal assistant.

#### 8. **Template Library** (`/templates`)
Browse and manage contract templates.

---

## API Integration

### API Client Setup

File: `src/lib/ai-clients.ts`

```typescript
const API_BASE = import.meta.env.VITE_API_BASE_URL

export const aiClient = {
  async post(endpoint: string, data: any) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`)
    }
    
    return response.json()
  },

  async get(endpoint: string) {
    const response = await fetch(`${API_BASE}${endpoint}`)
    
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`)
    }
    
    return response.json()
  },
}
```

### Making API Calls

```typescript
import { aiClient } from '@/lib/ai-clients'

// Drafting API
const draftResponse = await aiClient.post('/api/drafting/draft', {
  party_a: 'Company A',
  party_b: 'Company B',
  jurisdiction: 'United States',
  requirements: 'Software development agreement'
})

// Compliance API
const complianceResponse = await aiClient.post('/api/compliance/check', {
  contract_text: 'contract text here...',
  jurisdiction: 'United States'
})

// Health check
const health = await aiClient.get('/api/health')
```

### Custom Hook for API Calling

```typescript
// src/hooks/useApi.ts
import { useState } from 'react'
import { aiClient } from '@/lib/ai-clients'

export function useApi<T = any>(
  endpoint: string,
  method: 'GET' | 'POST' = 'POST'
) {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<Error | null>(null)
  const [loading, setLoading] = useState(false)

  const execute = async (payload?: any) => {
    setLoading(true)
    try {
      const result = method === 'GET'
        ? await aiClient.get(endpoint)
        : await aiClient.post(endpoint, payload)
      setData(result)
      return result
    } catch (err) {
      setError(err as Error)
      throw err
    } finally {
      setLoading(false)
    }
  }

  return { data, error, loading, execute }
}
```

Usage:

```typescript
// In component
const { data, loading, execute } = useApi('/api/drafting/draft')

const handleDraft = async () => {
  await execute({
    party_a: 'Company A',
    party_b: 'Company B'
  })
}
```

---

## State Management

### Context API for Global State

```typescript
// src/contexts/AppContext.tsx
import { createContext, useState, ReactNode } from 'react'

interface AppContextType {
  credits: number
  setCredits: (credits: number) => void
  theme: 'light' | 'dark'
  setTheme: (theme: 'light' | 'dark') => void
}

export const AppContext = createContext<AppContextType | undefined>(undefined)

export function AppProvider({ children }: { children: ReactNode }) {
  const [credits, setCredits] = useState(5)
  const [theme, setTheme] = useState<'light' | 'dark'>('light')

  return (
    <AppContext.Provider value={{ credits, setCredits, theme, setTheme }}>
      {children}
    </AppContext.Provider>
  )
}

// Hook for using context
export function useApp() {
  const context = useContext(AppContext)
  if (!context) {
    throw new Error('useApp must be used within AppProvider')
  }
  return context
}
```

### Using Context in Components

```typescript
// src/components/AICredits.tsx
import { useApp } from '@/contexts/AppContext'

export function AICredits() {
  const { credits } = useApp()

  return (
    <div className="flex items-center gap-2">
      <span className="text-sm font-medium">Credits: {credits}</span>
    </div>
  )
}
```

### React Query for Server State

```typescript
// src/hooks/useContractQuery.ts
import { useQuery } from '@tanstack/react-query'
import { aiClient } from '@/lib/ai-clients'

export function useContractDraft(payload: any) {
  return useQuery({
    queryKey: ['contract-draft', payload],
    queryFn: () => aiClient.post('/api/drafting/draft', payload),
    enabled: !!payload,
  })
}
```

---

## Styling & UI

### Tailwind CSS Usage

```typescript
// Component with Tailwind classes
export function MyComponent() {
  return (
    <div className="flex flex-col gap-4 p-6 bg-white rounded-lg shadow-md">
      <h1 className="text-2xl font-bold text-gray-900">Title</h1>
      <p className="text-gray-600">Description</p>
      <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
        Action
      </button>
    </div>
  )
}
```

### Dark Mode Support

```typescript
export function MyComponent() {
  return (
    <div className="bg-white dark:bg-slate-900 text-black dark:text-white">
      Content with dark mode support
    </div>
  )
}
```

### Common Patterns

```typescript
// Grid layout
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

// Flexbox
<div className="flex items-center justify-between gap-2">

// Responsive padding
<div className="p-4 md:p-6 lg:p-8">

// Responsive font sizes
<h1 className="text-xl md:text-2xl lg:text-3xl">
```

---

## Optional Features

### Supabase Integration

If using optional Supabase persistence:

```typescript
// src/lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = 
  supabaseUrl && supabaseKey 
    ? createClient(supabaseUrl, supabaseKey)
    : null
```

```typescript
// Usage in component
import { supabase } from '@/lib/supabase'

async function saveContract(contract: any) {
  if (!supabase) {
    console.warn('Supabase not configured')
    return
  }

  const { data, error } = await supabase
    .from('contracts')
    .insert([contract])

  if (error) console.error(error)
  return data
}
```

---

## Development Workflow

### Development Server Commands

```bash
# Start development server
npm run dev

# Start with specific port
npm run dev -- --port 5174

# Build for production
npm run build

# Preview production build locally
npm run preview

# Run linter
npm run lint

# Fix linting issues
npm run lint -- --fix
```

### Hot Module Replacement (HMR)

Vite provides instant HMR:
- Change component code and see updates instantly
- Preserve component state during changes
- No full page refresh required

### Debugging

```typescript
// Use browser DevTools
// 1. Press F12 to open DevTools
// 2. Go to Console tab
// 3. Use console.log() for debugging

// Component debugging
import { useEffect } from 'react'

export function MyComponent() {
  useEffect(() => {
    console.log('Component mounted')
    return () => console.log('Component unmounted')
  }, [])

  return <div>Content</div>
}
```

### Code Organization Best Practices

1. **Keep components small and focused**
   - One component per file
   - Max 200-300 lines per component

2. **Use TypeScript interfaces**
   ```typescript
   interface ContractData {
     id: string
     title: string
     content: string
     created_at: Date
   }
   ```

3. **Separate business logic**
   - Move logic to custom hooks or services
   - Keep components focused on UI

4. **Reuse components**
   - Create base components in `components/ui/`
   - Build from existing components

---

## Building for Production

### Production Build

```bash
# Create optimized production build
npm run build

# Output goes to 'dist/' directory
# Files are minified and optimized
```

### Build Output

```
dist/
├── index.html
├── assets/
│   ├── index-abc123.js      # Main bundle
│   ├── index-def456.css     # Styles bundle
│   └── vendor-ghi789.js     # Dependencies
└── robots.txt
```

### Performance Optimization

```typescript
// Code splitting with lazy loading
import { lazy, Suspense } from 'react'

const ContractDrafting = lazy(() => 
  import('./pages/ContractDrafting')
)

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <ContractDrafting />
    </Suspense>
  )
}
```

### Deployment Options

#### 1. **Vercel** (Recommended for Next.js, works with Vite)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

#### 2. **Netlify**

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy --prod --dir dist
```

#### 3. **AWS S3 + CloudFront**

```bash
# Build
npm run build

# Deploy to S3
aws s3 sync dist/ s3://your-bucket-name/
```

#### 4. **Docker**

```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY . .
RUN npm install && npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## Troubleshooting

### Common Issues

#### 1. **Module Not Found Errors**

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Or with pnpm
pnpm install --force
```

#### 2. **Port Already in Use**

```bash
# Use different port
npm run dev -- --port 5174

# Or find and kill process on port 5173
# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5173
kill -9 <PID>
```

#### 3. **API Connection Errors**

```bash
# Verify backend is running
curl http://localhost:8000/api/health

# Check VITE_API_BASE_URL in .env
cat .env | grep VITE_API_BASE_URL

# Clear browser cache (Ctrl+Shift+Delete)
```

#### 4. **TypeScript Errors**

```bash
# Ensure tsconfig.json is correct
npm run build

# Check for type errors
npx tsc --noEmit
```

#### 5. **Build Failures**

```bash
# Clean build
npm run build -- --force

# Check for linting errors
npm run lint

# Check package.json for issues
npm audit
```

#### 6. **Slow Development**

```bash
# Clear Vite cache
rm -rf .vite

# Restart dev server
npm run dev

# Increase Node memory
NODE_OPTIONS=--max-old-space-size=4096 npm run dev
```

---

## Performance Tips

### 1. Optimize Images
- Use WebP format when possible
- Lazy load images below fold
- Compress images before deployment

### 2. Code Splitting
- Use dynamic imports for routes
- Lazy load heavy components
- Monitor bundle size

### 3. Caching
- Leverage browser caching
- Cache API responses with React Query
- Use service workers

### 4. Network Optimization
- Minimize API calls
- Use request batching
- Implement debouncing for searches

---

## Available Scripts

| Script | Purpose |
|--------|---------|
| `npm run dev` | Start dev server |
| `npm run build` | Production build |
| `npm run build:dev` | Development build |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |

---

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

---

## Resources & Documentation

- 📚 [React Documentation](https://react.dev)
- 📚 [TypeScript Handbook](https://www.typescriptlang.org/docs)
- 📚 [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- 📚 [Vite Documentation](https://vitejs.dev)
- 📚 [shadcn/ui Components](https://ui.shadcn.com)
- 📚 [FastAPI Backend API](http://localhost:8000/docs)

---

## Support & Issues

- **Report Bugs**: [GitHub Issues](https://github.com/your-repo/issues)
- **Documentation**: [Backend README](../backend/README.md)
- **API Docs**: http://localhost:8000/docs

---

**Last Updated**: February 2026  
**Version**: 1.0.0  
**Status**: Production Ready

