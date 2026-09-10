import React, { useRef, useState } from "react";
import {
  UploadCloud,
  FileText,
  FileCheck,
  Table2,
  Image as ImageIcon,
  BookMarked,
  ArrowRight,
  Sparkles,
  Loader2,
  HardDriveDownload,
} from "lucide-react";
import { DocumentSummary } from "../types";

interface DashboardViewProps {
  summary: DocumentSummary | null;
  onUploadSuccess: (filePath: string, summary: DocumentSummary) => void;
  onNavigate: (page: "analyze" | "format") => void;
  isLoading: boolean;
  onLoadSample: () => void;
}

export const DashboardView: React.FC<DashboardViewProps> = ({
  summary,
  onUploadSuccess,
  onNavigate,
  isLoading,
  onLoadSample,
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const handleFileUpload = async (file: File) => {
    if (!file.name.endsWith(".docx")) {
      setUploadError("Only Microsoft Word (.docx) documents are supported.");
      return;
    }
    setUploadError(null);
    setUploading(true);

    const formData = new FormData();
    formData.append("manuscript", file);

    try {
      const res = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (data.success && data.summary) {
        onUploadSuccess(data.file_path, data.summary);
      } else {
        setUploadError(data.error || "Failed to process uploaded file.");
      }
    } catch (err: any) {
      setUploadError(err.message || "Upload network failure.");
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Title Bar */}
      <div>
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
          Manuscript Ingestion & Dashboard
        </h2>
        <p className="text-sm text-slate-500 mt-1">
          Upload unformatted Word documents for offline structural analysis and academic publication formatting.
        </p>
      </div>

      {/* Upload Box */}
      <div
        id="manuscript-drop-zone"
        onDragOver={(e) => {
          e.preventDefault();
          setDragActive(true);
        }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`cursor-pointer rounded-xl border-2 border-dashed p-8 transition-all text-center flex flex-col items-center justify-center ${
          dragActive
            ? "border-blue-500 bg-blue-50/70"
            : "border-slate-300 bg-white hover:border-blue-400 hover:bg-slate-50/50"
        } shadow-sm`}
      >
        <input
          type="file"
          ref={fileInputRef}
          accept=".docx"
          className="hidden"
          onChange={(e) => {
            if (e.target.files?.[0]) {
              handleFileUpload(e.target.files[0]);
            }
          }}
        />

        <div className="w-14 h-14 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center mb-3">
          {uploading ? (
            <Loader2 className="w-7 h-7 animate-spin" />
          ) : (
            <UploadCloud className="w-7 h-7" />
          )}
        </div>

        <h3 className="text-base font-semibold text-slate-800">
          {uploading
            ? "Analyzing Document Structure..."
            : "Click to upload or drag & drop Word manuscript (.docx)"}
        </h3>
        <p className="text-xs text-slate-500 mt-1 max-w-md">
          Supports 400+ page voluminous academic books and conference monographs with complete offline preservation guarantees.
        </p>

        <div className="mt-4 flex items-center gap-3">
          <button
            type="button"
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors shadow-sm"
          >
            Browse DOCX File
          </button>
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              onLoadSample();
            }}
            className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5"
          >
            <Sparkles className="w-4 h-4 text-blue-600" />
            Load Sample Manuscript
          </button>
        </div>
      </div>

      {uploadError && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-xs text-red-700">
          {uploadError}
        </div>
      )}

      {/* Summary Metadata Cards */}
      {summary && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider">
              Document Telemetry & Metadata
            </h3>
            <span className="text-xs font-mono text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
              {summary.filename} ({(summary.file_size_bytes / 1024).toFixed(1)} KB)
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
              <div className="flex items-center space-x-2 text-slate-500 mb-1">
                <BookMarked className="w-4 h-4 text-blue-600" />
                <span className="text-xs font-medium">Est. Pages</span>
              </div>
              <p className="text-2xl font-bold text-slate-900">{summary.estimated_pages}</p>
            </div>

            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
              <div className="flex items-center space-x-2 text-slate-500 mb-1">
                <FileText className="w-4 h-4 text-emerald-600" />
                <span className="text-xs font-medium">Paragraphs</span>
              </div>
              <p className="text-2xl font-bold text-slate-900">{summary.paragraph_count}</p>
            </div>

            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
              <div className="flex items-center space-x-2 text-slate-500 mb-1">
                <Table2 className="w-4 h-4 text-amber-600" />
                <span className="text-xs font-medium">Tables</span>
              </div>
              <p className="text-2xl font-bold text-slate-900">{summary.table_count}</p>
            </div>

            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
              <div className="flex items-center space-x-2 text-slate-500 mb-1">
                <ImageIcon className="w-4 h-4 text-violet-600" />
                <span className="text-xs font-medium">Figures</span>
              </div>
              <p className="text-2xl font-bold text-slate-900">{summary.image_count}</p>
            </div>

            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
              <div className="flex items-center space-x-2 text-slate-500 mb-1">
                <FileCheck className="w-4 h-4 text-sky-600" />
                <span className="text-xs font-medium">Words</span>
              </div>
              <p className="text-2xl font-bold text-slate-900">{summary.total_words}</p>
            </div>
          </div>

          {/* Action CTAs */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            <button
              id="action-btn-analyze"
              onClick={() => onNavigate("analyze")}
              className="p-5 bg-white hover:bg-blue-50/50 border border-slate-200 hover:border-blue-300 rounded-xl shadow-sm text-left transition-all group flex items-start justify-between"
            >
              <div>
                <span className="text-xs font-bold text-blue-600 uppercase tracking-wider">Step 1</span>
                <h4 className="text-base font-bold text-slate-900 group-hover:text-blue-600 transition-colors">
                  Analyze Document Structure
                </h4>
                <p className="text-xs text-slate-500 mt-1">
                  Run 36-feature vector extraction and Random Forest + rule engine classification.
                </p>
              </div>
              <ArrowRight className="w-5 h-5 text-slate-400 group-hover:text-blue-600 group-hover:translate-x-1 transition-all shrink-0 mt-2" />
            </button>

            <button
              id="action-btn-format"
              onClick={() => onNavigate("format")}
              className="p-5 bg-white hover:bg-emerald-50/50 border border-slate-200 hover:border-emerald-300 rounded-xl shadow-sm text-left transition-all group flex items-start justify-between"
            >
              <div>
                <span className="text-xs font-bold text-emerald-600 uppercase tracking-wider">Step 2</span>
                <h4 className="text-base font-bold text-slate-900 group-hover:text-emerald-600 transition-colors">
                  Format to Publication Specs
                </h4>
                <p className="text-xs text-slate-500 mt-1">
                  Apply Times New Roman, 1.5 spacing, 1.52cm margins, and generate publication DOCX.
                </p>
              </div>
              <ArrowRight className="w-5 h-5 text-slate-400 group-hover:text-emerald-600 group-hover:translate-x-1 transition-all shrink-0 mt-2" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
