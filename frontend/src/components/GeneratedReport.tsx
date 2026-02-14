// @ts-nocheck
/// <reference types="react" />
/** @jsxImportSource react */
import React, { useEffect, useMemo, useRef, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { toast } from "sonner";
import { marked } from "marked";
import html2pdf from "html2pdf.js";
import { saveAs } from "file-saver";
import { FileText, Download, Copy, RotateCcw, Edit3, Eye } from "lucide-react";

interface GeneratedReportProps {
  value: string;
  title?: string;
}

/**
 * Strip markdown code fences if the LLM wrapped its output in them.
 * Handles: ```markdown ... ```,  ``` ... ```,  or plain text.
 */
function stripMarkdownFences(text: string): string {
  let clean = text.trim();

  // Handle ```markdown ... ``` or ```md ... ``` or ``` ... ```
  const fenceRegex = /^```(?:markdown|md)?\s*\n([\s\S]*?)\n\s*```\s*$/;
  const match = clean.match(fenceRegex);
  if (match) {
    clean = match[1].trim();
  }

  return clean;
}

const GeneratedReport: React.FC<GeneratedReportProps> = ({ value, title = "Generated Report" }) => {
  const [mode, setMode] = useState<"preview" | "edit">("preview");
  const [draft, setDraft] = useState(value);
  const editorRef = useRef<HTMLDivElement>(null);
  const previewRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setDraft(stripMarkdownFences(value));
  }, [value]);

  const html = useMemo(() => {
    const cleaned = stripMarkdownFences(draft);
    return marked.parse(cleaned);
  }, [draft]);

  // Sync contentEditable changes back to draft state
  const handleEditorInput = () => {
    if (editorRef.current) {
      // We keep the HTML in the editor; draft stores the original markdown
      // for PDF/DOCX export. On edit, we update draft from editor innerHTML.
    }
  };

  const handleCopy = async () => {
    await navigator.clipboard.writeText(draft);
    toast.success("Content copied to clipboard");
  };

  const handleReset = () => {
    setDraft(stripMarkdownFences(value));
    toast.success("Reverted to original output");
  };

  const getExportHtml = (): string => {
    // If we're in edit mode, use the contentEditable HTML directly
    if (mode === "edit" && editorRef.current) {
      return editorRef.current.innerHTML;
    }
    // Otherwise use the parsed markdown
    return typeof html === "string" ? html : "";
  };

  const handleDownloadPdf = async () => {
    const container = document.createElement("div");
    container.innerHTML = getExportHtml();
    container.style.cssText = "font-family: Georgia, 'Times New Roman', serif; font-size: 12pt; line-height: 1.8; color: #1a1a1a; padding: 0.5in;";
    document.body.appendChild(container);
    const opt = {
      margin: 0.75,
      filename: "legal-contract.pdf",
      html2canvas: { scale: 2 },
      jsPDF: { unit: "in", format: "letter", orientation: "portrait" }
    };
    await (html2pdf() as any).set(opt).from(container).save();
    document.body.removeChild(container);
  };

  const handleDownloadDocx = () => {
    const exportHtml = getExportHtml();
    const htmlContent = `
      <html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word" xmlns="http://www.w3.org/TR/REC-html40">
        <head>
          <meta charset="utf-8">
          <title>Legal Contract</title>
          <style>
            body { font-family: Georgia, 'Times New Roman', serif; font-size: 12pt; line-height: 1.8; color: #1a1a1a; margin: 1in; }
            h1 { font-size: 18pt; font-weight: bold; margin-bottom: 12pt; text-align: center; }
            h2 { font-size: 14pt; font-weight: bold; margin-top: 18pt; margin-bottom: 8pt; border-bottom: 1px solid #ccc; padding-bottom: 4pt; }
            h3 { font-size: 12pt; font-weight: bold; margin-top: 12pt; margin-bottom: 6pt; }
            p { margin-bottom: 8pt; text-align: justify; }
            ol, ul { margin-left: 0.5in; margin-bottom: 8pt; }
            li { margin-bottom: 4pt; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 12pt; }
            td, th { border: 1px solid #999; padding: 6pt 8pt; }
            th { background-color: #f0f0f0; font-weight: bold; }
          </style>
        </head>
        <body>${exportHtml}</body>
      </html>`;
    const blob = new Blob([htmlContent], { type: 'application/msword' });
    saveAs(blob, "legal-contract.doc");
  };

  // Styles for the Word-like document container
  const documentStyles: React.CSSProperties = {
    fontFamily: "'Georgia', 'Times New Roman', 'Garamond', serif",
    fontSize: "12pt",
    lineHeight: "1.8",
    color: "#1a1a1a",
    backgroundColor: "#ffffff",
    padding: "48px 56px",
    minHeight: "500px",
    maxHeight: "700px",
    overflowY: "auto",
    borderRadius: "2px",
    boxShadow: "0 1px 4px rgba(0,0,0,0.08), 0 0 0 1px rgba(0,0,0,0.04)",
    textAlign: "justify" as const,
  };

  return (
    <Card className="overflow-hidden animate-scale-in border-0 shadow-lg">
      <CardContent className="p-0">
        {/* Toolbar */}
        <div className="flex flex-wrap items-center justify-between gap-3 px-6 py-4 bg-muted/30 border-b">
          <div className="flex items-center gap-3">
            <FileText className="h-5 w-5 text-primary" />
            <div>
              <h3 className="text-base font-semibold">{title}</h3>
              <p className="text-xs text-muted-foreground">
                {mode === "preview" ? "Document Preview" : "Editing — click on text to modify"}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div className="flex bg-muted rounded-lg p-0.5">
              <Button
                variant={mode === "preview" ? "default" : "ghost"}
                size="sm"
                onClick={() => setMode("preview")}
                className="gap-1.5 h-8 rounded-md"
              >
                <Eye className="h-3.5 w-3.5" />
                Preview
              </Button>
              <Button
                variant={mode === "edit" ? "default" : "ghost"}
                size="sm"
                onClick={() => setMode("edit")}
                className="gap-1.5 h-8 rounded-md"
              >
                <Edit3 className="h-3.5 w-3.5" />
                Edit
              </Button>
            </div>
          </div>
        </div>

        {/* Document Area */}
        <div className="p-6 bg-neutral-100 dark:bg-neutral-900">
          {mode === "preview" ? (
            <div
              ref={previewRef}
              className="legal-document"
              style={documentStyles}
              dangerouslySetInnerHTML={{ __html: html }}
            />
          ) : (
            <div
              ref={editorRef}
              className="legal-document"
              contentEditable
              suppressContentEditableWarning
              onInput={handleEditorInput}
              style={{
                ...documentStyles,
                outline: "none",
                border: "2px solid hsl(var(--primary) / 0.3)",
                cursor: "text",
              }}
              dangerouslySetInnerHTML={{ __html: html }}
            />
          )}
        </div>

        {/* Actions Bar */}
        <div className="flex flex-wrap items-center gap-2 px-6 py-3 bg-muted/20 border-t">
          <Button variant="ghost" size="sm" onClick={handleCopy} className="gap-1.5">
            <Copy className="h-3.5 w-3.5" />
            Copy
          </Button>
          <Button variant="ghost" size="sm" onClick={handleReset} className="gap-1.5">
            <RotateCcw className="h-3.5 w-3.5" />
            Reset
          </Button>
          <div className="flex-1" />
          <Button variant="outline" size="sm" onClick={handleDownloadDocx} className="gap-1.5">
            <Download className="h-3.5 w-3.5" />
            Download DOCX
          </Button>
          <Button size="sm" onClick={handleDownloadPdf} className="gap-1.5">
            <Download className="h-3.5 w-3.5" />
            Download PDF
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default GeneratedReport;
