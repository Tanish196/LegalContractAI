import React from "react";
import AIForm from "@/components/AIForm";
import { useInView } from "react-intersection-observer";
import { cn } from "@/lib/utils";

const LegalResearch = () => {
    const { ref, inView } = useInView({
        triggerOnce: true,
        threshold: 0.1,
    });

    return (
        <div className="legal-bg py-20 px-4 sm:px-6 lg:px-8" ref={ref}>
            <div className={cn(
                "transition-all duration-500 max-w-4xl mx-auto",
                inView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
            )}>
                <AIForm
                    title="Legal Research (BETA)"
                    description="Ask complex legal questions and get answers backed by statutes and case law."
                    placeholder="e.g. What are the penalties for data breach under the DPDP Act 2023?"
                    taskType="legal-research"
                />
            </div>
        </div>
    );
};

export default LegalResearch;
