import { TaskType } from '@/types/ai';

interface AIResponse {
  data: string | null;
  error: Error | null;
  metadata?: Record<string, any> | null;
}

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '');

type RouteConfig = {
  path: string;
  expects: 'text' | 'json';
  buildPayload: (content: string) => Record<string, any>;
  transform: (payload: any) => { result: string; metadata?: Record<string, any> | null };
};

const defaultReportRoute = (taskType: TaskType): RouteConfig => ({
  path: '/api/reports/generate',
  expects: 'json',
  buildPayload: (content) => ({ task_type: taskType, content }),
  transform: (payload) => ({ result: payload.report_markdown, metadata: payload })
});

const ROUTES: Record<TaskType, RouteConfig> = {
  'contract-drafting': {
    path: '/api/drafting/draft',
    expects: 'text',
    buildPayload: (content) => ({
      requirements: content,
      purpose: 'Contract generated via UI',
      jurisdiction: 'United States'
    }),
    transform: (payload: string) => ({ result: payload, metadata: null })
  },
  'compliance-check': {
    path: '/api/compliance/check',
    expects: 'json',
    buildPayload: (content) => ({
      contract_text: content,
      jurisdiction: 'United States'
    }),
    transform: (payload) => ({
      result: payload.report_markdown || payload.drafted_contract || '',
      metadata: payload
    })
  },
  'case-summary': {
    path: '/api/reports/generate',
    expects: 'json',
    buildPayload: (content) => ({ task_type: 'case-summary', content }),
    transform: (payload) => ({ result: payload.report_markdown, metadata: payload })
  },
  'clause-classification': {
    path: '/api/reports/generate',
    expects: 'json',
    buildPayload: (content) => ({ task_type: 'clause-classification', content }),
    transform: (payload) => ({ result: payload.report_markdown, metadata: payload })
  },
  'loophole-detection': {
    path: '/api/reports/generate',
    expects: 'json',
    buildPayload: (content) => ({ task_type: 'loophole-detection', content }),
    transform: (payload) => ({ result: payload.report_markdown, metadata: payload })
  }
};

export const aiClient = {
  async process(taskType: TaskType, content: string): Promise<AIResponse> {
    try {
      const route = ROUTES[taskType] ?? defaultReportRoute(taskType);
      const response = await fetch(`${API_BASE_URL}${route.path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(route.buildPayload(content))
      });

      if (!response.ok) {
        const detail = await response.text();
        throw new Error(detail || `Backend request failed with status ${response.status}`);
      }

      const payload = route.expects === 'text' ? await response.text() : await response.json();
      const { result, metadata } = route.transform(payload);

      return { data: result, error: null, metadata: metadata ?? null };
    } catch (error) {
      console.error('AI Processing Error:', error);
      return { data: null, error: error instanceof Error ? error : new Error('Processing failed') };
    }
  }
};