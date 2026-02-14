import { useEffect, useState } from 'react';
import { ScrollArea } from '@/components/ui/scroll-area';
import { getActivityDetail, getRecentActivity, UsageHistoryItem } from '@/services/usage';
import { useAuth } from '@/contexts/AuthContext';
import { format } from 'date-fns';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';
import { marked } from 'marked';
import { Loader2 } from 'lucide-react';

const serviceTypeLabels: Record<string, string> = {
  contract_draft: 'Contract Drafting',
  compliance_check: 'Compliance Check',
  case_summary: 'Case Summarization',
  loophole_detection: 'Loophole Detection',
  clause_classification: 'Clause Classification',
  legal_research: 'Legal Research',
  chat_assistant: 'AI Advisor Chat'
};

export function RecentActivity() {
  const [activities, setActivities] = useState<UsageHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedActivity, setSelectedActivity] = useState<UsageHistoryItem | null>(null);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [renderAsMarkdown, setRenderAsMarkdown] = useState(true);
  const navigate = useNavigate();
  const { user } = useAuth();

  // Ensure marked is configured to support common markdown features
  marked.setOptions({ gfm: true, breaks: true });

  useEffect(() => {
    async function loadActivity() {
      if (!user) return;

      try {
        const items = await getRecentActivity(user.id, 10);
        setActivities(items);
      } catch (error) {
        console.error('Failed to load recent activity:', error);
      } finally {
        setLoading(false);
      }
    }

    loadActivity();
  }, [user]);

  const handleSelectActivity = async (activity: UsageHistoryItem) => {
    setSelectedActivity(activity);

    if (!activity.prompt_output) {
      setLoadingDetail(true);
      try {
        const detail = await getActivityDetail(activity.id);
        if (detail) {
          setSelectedActivity(detail);
        }
      } catch (error) {
        console.error('Failed to load activity detail:', error);
      } finally {
        setLoadingDetail(false);
      }
    }
  };

  if (!user || (loading && activities.length === 0)) {
    return null;
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-medium">Recent Activity</h2>
        <Button
          variant="outline"
          size="sm"
          onClick={() => navigate('/activity-history')}
        >
          View All
        </Button>
      </div>

      <ScrollArea className="h-[250px]">
        {activities.length === 0 ? (
          <p className="text-sm text-muted-foreground text-center py-8">
            No recent activity to display
          </p>
        ) : (
          <div className="space-y-4">
            {activities.map((activity) => (
              <div
                key={activity.id}
                className="flex items-center justify-between border-b pb-2 last:border-0 cursor-pointer hover:bg-accent/50 p-2 rounded-lg transition-colors"
                onClick={() => handleSelectActivity(activity)}
              >
                <div>
                  <p className="font-medium">
                    {serviceTypeLabels[activity.service_type] || activity.service_type}
                  </p>
                  <p className="text-sm text-muted-foreground">
                    {format(new Date(activity.created_at), 'MMM d, yyyy h:mm a')}
                  </p>
                  {activity.prompt_title && (
                    <p className="text-sm text-muted-foreground mt-1">
                      {activity.prompt_title}
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </ScrollArea>

      <Dialog open={selectedActivity !== null} onOpenChange={() => setSelectedActivity(null)}>
        <DialogContent className="max-w-3xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>
              {selectedActivity?.prompt_title || serviceTypeLabels[selectedActivity?.service_type || ''] || 'Activity Details'}
            </DialogTitle>
          </DialogHeader>
          <div className="mt-4 space-y-4">
            <div>
              <h4 className="text-sm font-medium mb-1">Service Type</h4>
              <p className="text-sm text-muted-foreground">
                {selectedActivity && (serviceTypeLabels[selectedActivity.service_type] || selectedActivity.service_type)}
              </p>
            </div>
            <div>
              <h4 className="text-sm font-medium mb-1">Date</h4>
              <p className="text-sm text-muted-foreground">
                {selectedActivity && format(new Date(selectedActivity.created_at), 'MMMM d, yyyy h:mm a')}
              </p>
            </div>
            {loadingDetail ? (
              <div className="flex justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
              </div>
            ) : selectedActivity?.prompt_output && (
              <div>
                <h4 className="text-sm font-medium mb-1">Output</h4>
                <div className="flex items-center gap-2 mb-2">
                  <Button size="sm" variant={renderAsMarkdown ? 'default' : 'ghost'} onClick={() => setRenderAsMarkdown(true)}>Rendered</Button>
                  <Button size="sm" variant={!renderAsMarkdown ? 'default' : 'ghost'} onClick={() => setRenderAsMarkdown(false)}>Raw</Button>
                </div>
                <div className="bg-muted p-4 rounded-lg overflow-x-auto">
                  {renderAsMarkdown ? (
                    (() => {
                      const rawHtml = marked.parse(selectedActivity.prompt_output || '');
                      const sanitized = sanitizeHtml(rawHtml);
                      // helpful for debugging in dev console — removed in production if desired
                      if (typeof window !== 'undefined' && process.env.NODE_ENV !== 'production') {
                        // eslint-disable-next-line no-console
                        console.debug('Rendered markdown HTML:', sanitized);
                      }

                      return (
                        <div
                          className="max-w-none text-sm break-words prose prose-sm dark:prose-invert"
                          dangerouslySetInnerHTML={{ __html: sanitized }}
                        />
                      );
                    })()
                  ) : (
                    <pre className="text-sm whitespace-pre-wrap">{selectedActivity.prompt_output}</pre>
                  )}
                </div>
              </div>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}

// Very small sanitizer: removes <script> tags and strip attributes starting with "on" (event handlers).
function sanitizeHtml(html: string) {
  // Remove script tags
  let sanitized = html.replace(/<script[\s\S]*?>[\s\S]*?<\/script>/gi, '');

  // Remove event handler attributes like onclick, onerror, etc.
  sanitized = sanitized.replace(/\s(on[a-z]+)=("[^"]*"|'[^']*'|[^\s>]+)/gi, '');

  // Remove javascript: URIs in href/src
  sanitized = sanitized.replace(/(href|src)=("|')?javascript:[^"'> ]*("|')?/gi, '');

  return sanitized;
}
