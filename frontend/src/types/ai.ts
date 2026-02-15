import React from 'react';

export type TaskType = 'case-summary' | 'loophole-detection' | 'clause-classification' | 'contract-drafting' | 'compliance-check' | 'legal-research' | 'chat-assistant' | 'law-template';

export type ServiceType =
  | 'contract_draft'
  | 'compliance_check'
  | 'case_summary'
  | 'loophole_detection'
  | 'clause_classification'
  | 'legal_research'
  | 'chat_assistant';

export interface AIFormProps {
  title: string;
  description: string;
  placeholder?: string;
  taskType: TaskType;
  additionalFields?: React.ReactNode;
  additionalData?: Record<string, any>;
  onReset?: () => void;
  summaryRenderer?: (metadata: Record<string, any> | null) => React.ReactNode;
}