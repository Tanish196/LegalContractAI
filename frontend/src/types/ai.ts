export type TaskType = 'case-summary' | 'loophole-detection' | 'clause-classification' | 'contract-drafting' | 'compliance-check' | 'legal-research' | 'chat-assistant';

export type ServiceType = 'contract_draft' | 'compliance_check';

export interface AIFormProps {
  title: string;
  description: string;
  placeholder?: string;
  taskType: TaskType;
  additionalFields?: React.ReactNode;
  additionalData?: Record<string, any>;
}