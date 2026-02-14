import React, { useEffect, useState } from 'react';
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area';
import { getActivityDetail, getRecentActivity, UsageHistoryItem } from '@/services/usage';
import { useAuth } from '@/contexts/AuthContext';
import { format } from 'date-fns';
import { marked } from 'marked';
import { Loader2 } from 'lucide-react';

const serviceTypeLabels: Record<string, string> = {
  contract_draft: 'Contract Drafting',
  compliance_check: 'Compliance Check'
};

const ActivityHistory = () => {
  const [activities, setActivities] = useState<UsageHistoryItem[]>([]);
  const [selectedActivity, setSelectedActivity] = useState<UsageHistoryItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const { user } = useAuth();

  useEffect(() => {
    async function loadActivity() {
      if (!user) return;

      try {
        setLoading(true);
        const items = await getRecentActivity(user.id, 100);
        setActivities(items);
        if (items.length > 0 && !selectedActivity) {
          handleSelectActivity(items[0]);
        }
      } catch (error) {
        console.error('Failed to load activity history:', error);
      } finally {
        setLoading(false);
      }
    }

    loadActivity();
  }, [user]);

  const handleSelectActivity = async (activity: UsageHistoryItem) => {
    if (selectedActivity?.id === activity.id) return;

    // Set metadata first so UI feels responsive
    setSelectedActivity(activity);

    // Then fetch details if not already present
    if (!activity.prompt_output) {
      setLoadingDetail(true);
      try {
        const detail = await getActivityDetail(activity.id);
        if (detail) {
          setSelectedActivity(detail);
          // Optionally update the activities list with the detail to avoid re-fetching
          setActivities(prev => prev.map(a => a.id === detail.id ? detail : a));
        }
      } catch (error) {
        console.error('Failed to fetch activity detail:', error);
      } finally {
        setLoadingDetail(false);
      }
    }
  };

  if (!user) {
    return null;
  }

  return (
    <div className="container mx-auto py-6 h-[calc(100vh-8rem)] flex flex-col">
      <div className="grid grid-cols-[300px_1fr] gap-6 flex-1 min-h-0">
        {/* Left panel */}
        <div className="border rounded-lg shadow-sm bg-background flex flex-col min-h-0">
          <div className="p-4 border-b bg-muted/10">
            <h2 className="font-semibold">Activity History</h2>
          </div>
          <ScrollArea className="flex-1 min-h-0 bg-background">
            <div className="space-y-1 p-2">
              {loading && activities.length === 0 ? (
                <div className="flex justify-center py-8">
                  <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
                </div>
              ) : activities.map((activity) => (
                <button
                  key={activity.id}
                  onClick={() => handleSelectActivity(activity)}
                  className={`w-full text-left p-3 rounded-lg transition-colors border mb-1 ${selectedActivity?.id === activity.id
                    ? 'bg-primary/10 border-primary/20 text-foreground ring-1 ring-primary/20'
                    : 'hover:bg-accent border-transparent'
                    }`}
                >
                  <div className="font-medium flex justify-between items-start gap-2">
                    <span className="truncate">
                      {serviceTypeLabels[activity.service_type] || activity.service_type}
                    </span>
                    <span className="text-[10px] whitespace-nowrap opacity-60 mt-1">
                      {format(new Date(activity.created_at), 'MMM d')}
                    </span>
                  </div>
                  {activity.prompt_title && (
                    <div className="text-xs text-muted-foreground truncate mt-1 opactiy-80">
                      {activity.prompt_title}
                    </div>
                  )}
                </button>
              ))}
            </div>
          </ScrollArea>
        </div>

        <div className="border rounded-lg shadow-sm bg-background flex flex-col min-w-0 min-h-0">
          <div className="border-b p-4 min-h-[73px] bg-muted/10 flex-shrink-0 flex items-center justify-between">
            <div>
              <h2 className="font-semibold text-lg line-clamp-1">
                {selectedActivity?.prompt_title || serviceTypeLabels[selectedActivity?.service_type || ''] || 'Activity Detail'}
              </h2>
              <div className="text-xs text-muted-foreground">
                {selectedActivity ? format(new Date(selectedActivity.created_at), 'MMMM d, yyyy h:mm a') : ''}
              </div>
            </div>
          </div>

          <ScrollArea className="flex-1 min-h-0">
            <div className="p-6">
              {loadingDetail ? (
                <div className="flex flex-col items-center justify-center py-20 gap-3">
                  <Loader2 className="h-8 w-8 animate-spin text-primary" />
                  <p className="text-sm text-muted-foreground">Loading document details...</p>
                </div>
              ) : selectedActivity?.prompt_output ? (
                <div
                  className="prose prose-sm dark:prose-invert max-w-none break-words"
                  dangerouslySetInnerHTML={{
                    __html: marked(selectedActivity.prompt_output, { breaks: true })
                  }}
                />
              ) : (
                <div className="flex items-center justify-center text-muted-foreground py-20">
                  {selectedActivity ? "No content available for this activity" : "Select an activity to view details"}
                </div>
              )}
            </div>
            <ScrollBar orientation="horizontal" />
          </ScrollArea>
        </div>
      </div>
    </div>
  );
};

export default ActivityHistory;