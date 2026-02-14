import React from "react";
import AIForm from "@/components/AIForm";
import { useInView } from "react-intersection-observer";
import { cn } from "@/lib/utils";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Card } from "@/components/ui/card";

const ComplianceCheck = () => {
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  const [standards, setStandards] = React.useState<string[]>(['gdpr']);

  const handleCheckboxChange = (id: string, checked: boolean) => {
    setStandards(prev =>
      checked ? [...prev, id] : prev.filter(s => s !== id)
    );
  };

  const additionalFields = (
    <Card className="border border-border/60 p-6 mt-6 rounded-lg card-shadow">
      <div className="space-y-4">
        <div className="space-y-2">
          <Label className="text-base font-medium">Compliance Standards</Label>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-3">
            <div className="flex items-center space-x-2">
              <Checkbox
                id="gdpr"
                checked={standards.includes('gdpr')}
                onCheckedChange={(checked) => handleCheckboxChange('gdpr', checked as boolean)}
              />
              <Label htmlFor="gdpr" className="font-normal">GDPR</Label>
            </div>
            <div className="flex items-center space-x-2">
              <Checkbox
                id="hipaa"
                checked={standards.includes('hipaa')}
                onCheckedChange={(checked) => handleCheckboxChange('hipaa', checked as boolean)}
              />
              <Label htmlFor="hipaa" className="font-normal">HIPAA</Label>
            </div>
            <div className="flex items-center space-x-2">
              <Checkbox
                id="ccpa"
                checked={standards.includes('ccpa')}
                onCheckedChange={(checked) => handleCheckboxChange('ccpa', checked as boolean)}
              />
              <Label htmlFor="ccpa" className="font-normal">CCPA</Label>
            </div>
            <div className="flex items-center space-x-2">
              <Checkbox
                id="ferpa"
                checked={standards.includes('ferpa')}
                onCheckedChange={(checked) => handleCheckboxChange('ferpa', checked as boolean)}
              />
              <Label htmlFor="ferpa" className="font-normal">FERPA</Label>
            </div>
            <div className="flex items-center space-x-2">
              <Checkbox
                id="glba"
                checked={standards.includes('glba')}
                onCheckedChange={(checked) => handleCheckboxChange('glba', checked as boolean)}
              />
              <Label htmlFor="glba" className="font-normal">GLBA</Label>
            </div>
            <div className="flex items-center space-x-2">
              <Checkbox
                id="sox"
                checked={standards.includes('sox')}
                onCheckedChange={(checked) => handleCheckboxChange('sox', checked as boolean)}
              />
              <Label htmlFor="sox" className="font-normal">SOX</Label>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );

  return (
    <div className="container-tight py-16" ref={ref}>
      <div className={cn(
        "transition-all duration-500",
        inView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
      )}>
        <AIForm
          title="Compliance Check"
          description="Ensure your legal documents comply with relevant laws and regulations."
          placeholder="Paste your document here for compliance analysis..."
          taskType="compliance-check"
          additionalFields={additionalFields}
          additionalData={{ standards }}
        />
      </div>
    </div>
  );
};

export default ComplianceCheck;
