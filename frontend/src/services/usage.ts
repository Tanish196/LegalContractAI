import { supabase } from '@/lib/supabase';
import { ServiceType, TaskType } from '@/types/ai';

// Map AI task types to service types for database storage
const taskToServiceType: Record<TaskType, ServiceType> = {
  'contract-drafting': 'contract_draft',
  'compliance-check': 'compliance_check',
  'case-summary': 'case_summary',
  'loophole-detection': 'loophole_detection',
  'clause-classification': 'clause_classification',
  'legal-research': 'legal_research',
  'chat-assistant': 'chat_assistant'
};

export interface UsageHistoryItem {
  id: string;
  user_id: string;
  service_type: ServiceType;
  created_at: string;
  prompt_title: string | null;
  prompt_output: string | null;
}

export async function recordUsage(
  userId: string,
  taskType: TaskType,
  promptTitle?: string,
  promptOutput?: string
): Promise<void> {
  const serviceType = taskToServiceType[taskType];

  try {
    // 1. Record in history
    const { error: historyError } = await supabase
      .from('usage_history')
      .insert({
        user_id: userId,
        service_type: serviceType,
        prompt_title: promptTitle || null,
        prompt_output: promptOutput || null
      });

    if (historyError) throw historyError;

    // 2. Decrement remaining credits
    const { data: creditData, error: fetchError } = await supabase
      .from('user_credits')
      .select('credits_remaining, credits_used_today')
      .eq('user_id', userId)
      .single();

    if (!fetchError && creditData) {
      await supabase
        .from('user_credits')
        .update({
          credits_remaining: Math.max(0, creditData.credits_remaining - 1),
          credits_used_today: (creditData.credits_used_today || 0) + 1,
          updated_at: new Date().toISOString()
        })
        .eq('user_id', userId);
    }
  } catch (err) {
    console.error('Failed to record usage:', err);
    throw err;
  }
}

export interface CreditInfo {
  used: number;
  total: number;
  remaining: number;
}

export async function getUserCredits(userId: string): Promise<CreditInfo> {
  try {
    const defaultTotal = parseInt(import.meta.env.VITE_DEFAULT_CREDITS || '5');

    // Get the user's credits from user_credits table
    const { data: creditData, error: creditError } = await supabase
      .from('user_credits')
      .select('credits_remaining, credits_used_today')
      .eq('user_id', userId)
      .single();

    // If no record exists, they might be a new user, default to env value
    if (creditError && creditError.code !== 'PGRST116') { // PGRST116 is 'no rows'
      throw creditError;
    }

    const remaining = creditData ? creditData.credits_remaining : defaultTotal;
    const used = defaultTotal - remaining;

    return {
      used,
      total: defaultTotal,
      remaining
    };
  } catch (err) {
    console.error('Failed to get user credits:', err);
    return {
      used: 0,
      total: 5,
      remaining: 5
    };
  }
}

export async function getRecentActivity(userId: string, limit: number = 5): Promise<UsageHistoryItem[]> {
  try {
    const { data, error } = await supabase
      .from('usage_history')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
      .limit(limit);

    if (error) {
      console.error('Error fetching recent activity:', error);
      throw error;
    }

    return data || [];
  } catch (err) {
    console.error('Failed to fetch recent activity:', err);
    throw err;
  }
}
