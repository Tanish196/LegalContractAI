// @ts-nocheck
/// <reference types="react" />
/** @jsxImportSource react */
import React, { useEffect, useState } from "react";
import { cn } from "@/lib/utils";
import { Check, Loader2, Clock } from "lucide-react";

export interface PipelineStage {
    id: string;
    label: string;
    description: string;
    icon?: string;
}

interface PipelineViewerProps {
    stages: PipelineStage[];
    isActive: boolean;
}

const DEFAULT_STAGES: PipelineStage[] = [
    { id: "intent", label: "Intent Analysis", description: "Understanding contract requirements", icon: "🔍" },
    { id: "policy", label: "Policy Check", description: "Validating compliance & policies", icon: "🛡️" },
    { id: "template", label: "Template Selection", description: "Choosing optimal structure", icon: "📋" },
    { id: "generation", label: "Generation", description: "Drafting contract clauses", icon: "✍️" },
    { id: "review", label: "Self Review", description: "Quality & completeness check", icon: "✅" },
];

const COMPLIANCE_STAGES: PipelineStage[] = [
    { id: "ingestion", label: "Ingestion", description: "Parsing document structure", icon: "📥" },
    { id: "jurisdiction", label: "Jurisdiction", description: "Determining legal context", icon: "xx" }, // xx to be replaced or handled by flag emoji logic if available, or just use map icon
    { id: "extraction", label: "Extraction", description: "Identifying key clauses", icon: "🔍" },
    { id: "retrieval", label: "Retrieval", description: "Fetching relevant statutes", icon: "📚" },
    { id: "reasoning", label: "Reasoning", description: "Analyzing compliance", icon: "🧠" },
    { id: "risk", label: "Risk Scoring", description: "Calculating risk assessment", icon: "⚠️" },
];

const RESEARCH_STAGES: PipelineStage[] = [
    { id: "query", label: "Query Analysis", description: "Parsing legal question", icon: "❓" },
    { id: "statutes", label: "Statutes", description: "Searching acts & regulations", icon: "📖" },
    { id: "cases", label: "Case Law", description: "Finding relevant precedents", icon: "⚖️" },
    { id: "synthesis", label: "Synthesis", description: "Combining legal authorities", icon: "🧪" },
    { id: "formatting", label: "Formatting", description: "Structuring legal memo", icon: "📝" },
];

const SUMMARY_STAGES: PipelineStage[] = [
    { id: "ingest", label: "Text Analysis", description: "Reading case text", icon: "📄" },
    { id: "facts", label: "Fact Extraction", description: "Identifying key facts", icon: "🔍" },
    { id: "holding", label: "Holding", description: "Determining court's ruling", icon: "⚖️" },
    { id: "reasoning", label: "Reasoning", description: "Summarizing legal logic", icon: "🧠" },
    { id: "final", label: "Final Summary", description: "Generating concise output", icon: "📝" },
];

/**
 * PipelineViewer — shows the 5 agentic stages as a horizontal landscape progress bar.
 * Stages animate sequentially when `isActive` is true.
 */
const PipelineViewer: React.FC<PipelineViewerProps> = ({
    stages = DEFAULT_STAGES,
    isActive,
}) => {
    const [currentStage, setCurrentStage] = useState(-1);

    useEffect(() => {
        if (!isActive) {
            setCurrentStage(-1);
            return;
        }

        setCurrentStage(0);

        // Simulate progression through stages
        // Intent: ~2s, Policy: ~2s, Template: ~2s, Generation: ~8s, Review: ~3s
        const timings = [2000, 2000, 2000, 8000, 3000];
        let timeoutIds: ReturnType<typeof setTimeout>[] = [];
        let cumulativeTime = 0;

        stages.forEach((_, idx) => {
            if (idx === 0) return; // already set to 0
            cumulativeTime += timings[idx - 1] || 3000;
            const tid = setTimeout(() => setCurrentStage(idx), cumulativeTime);
            timeoutIds.push(tid);
        });

        return () => timeoutIds.forEach(clearTimeout);
    }, [isActive, stages.length]);

    const getStageStatus = (idx: number) => {
        if (!isActive) return "idle";
        if (idx < currentStage) return "done";
        if (idx === currentStage) return "active";
        return "pending";
    };

    return (
        <div className="w-full my-6">
            {/* Header */}
            <div className="flex items-center justify-center mb-4">
                <div className="flex items-center gap-2">
                    <div className="h-2 w-2 rounded-full bg-primary animate-pulse" />
                    <p className="text-sm font-medium text-muted-foreground">
                        AI Agent Pipeline
                    </p>
                </div>
            </div>

            {/* Landscape Pipeline */}
            <div className="relative overflow-x-auto">
                <div className="flex items-center justify-between min-w-[600px] px-4">
                    {stages.map((stage, idx) => {
                        const status = getStageStatus(idx);
                        return (
                            <React.Fragment key={stage.id}>
                                {/* Stage Node */}
                                <div className="flex flex-col items-center gap-2 relative z-10 flex-1">
                                    {/* Circle */}
                                    <div
                                        className={cn(
                                            "w-12 h-12 rounded-full flex items-center justify-center transition-all duration-500 border-2",
                                            status === "done" &&
                                            "bg-emerald-500/15 border-emerald-500 text-emerald-600 dark:text-emerald-400 shadow-[0_0_12px_rgba(16,185,129,0.25)]",
                                            status === "active" &&
                                            "bg-primary/15 border-primary text-primary shadow-[0_0_16px_rgba(var(--primary-rgb,59,130,246),0.3)] animate-pulse",
                                            status === "pending" &&
                                            "bg-muted border-muted-foreground/20 text-muted-foreground/40",
                                            status === "idle" &&
                                            "bg-muted/50 border-muted-foreground/10 text-muted-foreground/30"
                                        )}
                                    >
                                        {status === "done" ? (
                                            <Check className="h-5 w-5" />
                                        ) : status === "active" ? (
                                            <Loader2 className="h-5 w-5 animate-spin" />
                                        ) : (
                                            <span className="text-lg">{stage.icon || "○"}</span>
                                        )}
                                    </div>

                                    {/* Label */}
                                    <div className="text-center">
                                        <p
                                            className={cn(
                                                "text-xs font-semibold transition-colors duration-300",
                                                status === "done" && "text-emerald-600 dark:text-emerald-400",
                                                status === "active" && "text-primary",
                                                status === "pending" && "text-muted-foreground/50",
                                                status === "idle" && "text-muted-foreground/30"
                                            )}
                                        >
                                            {stage.label}
                                        </p>
                                        <p
                                            className={cn(
                                                "text-[10px] mt-0.5 transition-colors duration-300 max-w-[100px]",
                                                status === "active"
                                                    ? "text-muted-foreground"
                                                    : "text-muted-foreground/40"
                                            )}
                                        >
                                            {stage.description}
                                        </p>
                                    </div>
                                </div>

                                {/* Connector Line */}
                                {idx < stages.length - 1 && (
                                    <div className="flex-shrink-0 w-12 h-0.5 relative -mt-8">
                                        {/* Background line */}
                                        <div className="absolute inset-0 bg-muted-foreground/10 rounded-full" />
                                        {/* Animated fill */}
                                        <div
                                            className={cn(
                                                "absolute inset-y-0 left-0 rounded-full transition-all duration-700 ease-out",
                                                currentStage > idx
                                                    ? "w-full bg-emerald-500"
                                                    : currentStage === idx
                                                        ? "w-1/2 bg-primary animate-pulse"
                                                        : "w-0 bg-transparent"
                                            )}
                                        />
                                    </div>
                                )}
                            </React.Fragment>
                        );
                    })}
                </div>
            </div>

            {/* Current Stage Status */}
            {isActive && currentStage >= 0 && currentStage < stages.length && (
                <div className="mt-4 flex items-center justify-center gap-2 text-sm text-muted-foreground animate-fade-in">
                    <Loader2 className="h-3.5 w-3.5 animate-spin text-primary" />
                    <span>
                        {stages[currentStage]?.icon} {stages[currentStage]?.description}...
                    </span>
                </div>
            )}
        </div>
    );
};

export { DEFAULT_STAGES, COMPLIANCE_STAGES, RESEARCH_STAGES, SUMMARY_STAGES };
export default PipelineViewer;
