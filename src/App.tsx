import React, { useState, useEffect } from "react";
import { Sidebar, NavPage } from "./components/Sidebar";
import { DashboardView } from "./components/DashboardView";
import { AnalyzeView } from "./components/AnalyzeView";
import { FormatView } from "./components/FormatView";
import { ResultsView } from "./components/ResultsView";
import { PerformanceView } from "./components/PerformanceView";
import { SettingsView } from "./components/SettingsView";
import {
  DocumentSummary,
  AnalysisResponse,
  FormattingStats,
  PublicationSpecs,
} from "./types";

const DEFAULT_SPECS: PublicationSpecs = {
  top_margin_cm: 1.52,
  bottom_margin_cm: 1.52,
  left_margin_cm: 1.97,
  right_margin_cm: 1.96,
  body_font_name: "Times New Roman",
  body_font_size: 12.0,
  body_line_spacing: 1.5,
  first_line_indent_cm: 1.27,
  include_toc: true,
};

export default function App() {
  const [currentPage, setCurrentPage] = useState<NavPage>("dashboard");
  const [currentFilePath, setCurrentFilePath] = useState<string>("samples/input.docx");
  const [summary, setSummary] = useState<DocumentSummary | null>(null);
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null);
  const [formattingStats, setFormattingStats] = useState<FormattingStats | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [specs, setSpecs] = useState<PublicationSpecs>(DEFAULT_SPECS);
  const [notification, setNotification] = useState<string | null>(null);

  // Load sample manuscript summary on initial mount
  useEffect(() => {
    fetchSummary("samples/input.docx");
  }, []);

  const showNotification = (msg: string) => {
    setNotification(msg);
    setTimeout(() => setNotification(null), 4000);
  };

  const fetchSummary = async (filePath: string) => {
    try {
      const res = await fetch(`/api/summary?file=${encodeURIComponent(filePath)}`);
      const data = await res.json();
      if (!data.error) {
        setSummary(data);
        setCurrentFilePath(filePath);
      }
    } catch (err) {
      console.error("Failed to load summary:", err);
    }
  };

  const handleUploadSuccess = (filePath: string, newSummary: DocumentSummary) => {
    setCurrentFilePath(filePath);
    setSummary(newSummary);
    setAnalysis(null);
    setFormattingStats(null);
    showNotification(`Manuscript "${newSummary.filename}" loaded successfully!`);
  };

  const handleLoadSample = () => {
    fetchSummary("samples/input.docx");
    showNotification("Loaded bundled sample manuscript (samples/input.docx)");
  };

  const handleRunAnalysis = async () => {
    setIsLoading(true);
    try {
      const res = await fetch(`/api/analyze?file=${encodeURIComponent(currentFilePath)}`);
      const data = await res.json();
      if (!data.error) {
        setAnalysis(data);
        showNotification("Document structure classified successfully!");
      }
    } catch (err: any) {
      console.error("Analysis failed:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleExecuteFormat = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("/api/format", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          file: currentFilePath,
          output: "output/formatted_book.docx",
          specs: specs,
          include_toc: specs.include_toc,
        }),
      });
      const data = await res.json();
      if (!data.error) {
        setFormattingStats(data);
        showNotification("Publication document formatted and ready for download!");
      }
    } catch (err) {
      console.error("Formatting failed:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-50 font-sans text-slate-800 antialiased">
      {/* Sidebar Navigation */}
      <Sidebar
        currentPage={currentPage}
        onPageSelect={(page) => setCurrentPage(page)}
        documentLoaded={summary !== null}
      />

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col min-w-0 overflow-y-auto">
        {/* Top Notification Bar if active */}
        {notification && (
          <div className="bg-blue-600 text-white text-xs font-semibold px-6 py-2 shadow-sm transition-all flex items-center justify-between">
            <span>{notification}</span>
            <button
              onClick={() => setNotification(null)}
              className="text-blue-200 hover:text-white ml-4"
            >
              ✕
            </button>
          </div>
        )}

        {/* View Routing */}
        <div className="p-6 md:p-8 flex-1">
          {currentPage === "dashboard" && (
            <DashboardView
              summary={summary}
              onUploadSuccess={handleUploadSuccess}
              onNavigate={(page) => {
                setCurrentPage(page);
                if (page === "analyze" && !analysis) {
                  handleRunAnalysis();
                }
              }}
              isLoading={isLoading}
              onLoadSample={handleLoadSample}
            />
          )}

          {currentPage === "analyze" && (
            <AnalyzeView
              analysis={analysis}
              onRunAnalysis={handleRunAnalysis}
              isLoading={isLoading}
            />
          )}

          {currentPage === "format" && (
            <FormatView
              onExecuteFormat={handleExecuteFormat}
              formattingStats={formattingStats}
              isLoading={isLoading}
              specs={specs}
            />
          )}

          {currentPage === "results" && (
            <ResultsView stats={formattingStats} analysis={analysis} />
          )}

          {currentPage === "performance" && <PerformanceView />}

          {currentPage === "settings" && (
            <SettingsView
              specs={specs}
              onUpdateSpecs={setSpecs}
              onResetDefaults={() => {
                setSpecs(DEFAULT_SPECS);
                showNotification("Publication specifications reset to standard defaults.");
              }}
            />
          )}
        </div>
      </main>
    </div>
  );
}
