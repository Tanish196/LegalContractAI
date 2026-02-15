import React from "react";
import AIForm from "@/components/AIForm";
import { Card, CardContent } from "@/components/ui/card";

const ClauseClassification = () => {
  return (
    <AIForm
      title="Clause Classification"
      description="Automatically analyze and categorize legal clauses to understand their purpose and implications."
      placeholder="Paste your legal document or contract clauses here for classification..."
      taskType="clause-classification"
      summaryRenderer={(metadata) => {
        if (!metadata?.risks || !Array.isArray(metadata.risks)) return null;
        
        const high = metadata.risks.filter((r: any) => r.risk_level === 'High').length;
        const medium = metadata.risks.filter((r: any) => r.risk_level === 'Medium').length;
        const low = metadata.risks.filter((r: any) => r.risk_level === 'Low').length;
        const total = metadata.risks.length;
        
        return (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <Card>
              <CardContent className="py-4">
                <p className="text-xs uppercase tracking-wide text-muted-foreground">Total Clauses</p>
                <p className="text-2xl font-semibold">{total}</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="py-4">
                <p className="text-xs uppercase tracking-wide text-muted-foreground">High Risk</p>
                <p className="text-2xl font-semibold text-red-500">{high}</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="py-4">
                <p className="text-xs uppercase tracking-wide text-muted-foreground">Medium Risk</p>
                <p className="text-2xl font-semibold text-amber-500">{medium}</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="py-4">
                <p className="text-xs uppercase tracking-wide text-muted-foreground">Low Risk</p>
                <p className="text-2xl font-semibold text-emerald-500">{low}</p>
              </CardContent>
            </Card>
          </div>
        );
      }}
    />
  );
};

export default ClauseClassification;