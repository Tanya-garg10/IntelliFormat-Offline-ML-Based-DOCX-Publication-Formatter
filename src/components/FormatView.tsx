import React, { useState } from "react";
import {
  FileCheck2,
  Download,
  CheckCircle,
  AlertCircle,
  Sliders,
  ShieldCheck,
  BookOpen,
  ArrowDownToLine,
  Loader2,
} from "lucide-react";
import { FormattingStats, PublicationSpecs } from "../types";

interface FormatViewProps {
  onExecuteFormat: () => Promise<void>;
  formattingStats: FormattingStats | null;
  isLoading: boolean;
  specs: PublicationSpecs;
}

export const FormatView: React.FC<FormatViewProps> = ({
  onExecuteFormat,
  formattingStats,
  isLoading,
  specs,
}) => {
  const [downloadSuccess, setDownloadSuccess] = useState(false);

  const handleDownload = () => {
    const filename = formattingStats?.output_path || "output/formatted_book.docx";
    window.location.href = `/api/download?file=${encodeURIComponent(filename)}`;
    setDownloadSuccess(true);
    setTimeout(() => setDownloadSuccess(false), 4000);
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Title */}
      <div>
        <h2 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
          <FileCheck2 className="w-6 h-6 text-emerald-600" />
          Publication Typesetting Engine
        </h2>
        <p className="text-sm text-slate-500 mt-1">
          Applies academic monograph typography and geometry specifications via python-docx.
        </p>
      </div>

      {/* Specification Rules Checklist */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Page & Margins Spec Card */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-3">
          <div className="flex items-center justify-between border-b border-slate-100 pb-2">
            <span className="text-xs font-bold text-blue-600 uppercase tracking-wider">
              Page & Geometry Specifications
            </span>
            <span className="px-2 py-0.5 bg-blue-50 text-blue-700 text-xs font-semibold rounded">
              Standardized
            </span>
          </div>

          <ul className="space-y-2 text-xs text-slate-700">
            <li className="flex items-center justify-between">
              <span className="text-slate-500">Top & Bottom Margins:</span>
              <span className="font-semibold text-slate-900 font-mono">1.52 cm / 1.52 cm</span>
            </li>
            <li className="flex items-center justify-between">
              <span className="text-slate-500">Left & Right Margins:</span>
              <span className="font-semibold text-slate-900 font-mono">1.97 cm / 1.96 cm</span>
            </li>
            <li className="flex items-center justify-between">
              <span className="text-slate-500">Gutter Alignment:</span>
              <span className="font-semibold text-slate-900 font-mono">Left Orientation</span>
            </li>
            <li className="flex items-center justify-between">
              <span className="text-slate-500">Layout Format:</span>
              <span className="font-semibold text-slate-900 font-mono">Single-Column Monograph</span>
            </li>
          </ul>
        </div>

        {/* Typography & Spacing Spec Card */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-3">
          <div className="flex items-center justify-between border-b border-slate-100 pb-2">
            <span className="text-xs font-bold text-emerald-600 uppercase tracking-wider">
              Typography & Hierarchy Specs
            </span>
            <span className="px-2 py-0.5 bg-emerald-50 text-emerald-700 text-xs font-semibold rounded">
              Verified
            </span>
          </div>

          <ul className="space-y-2 text-xs text-slate-700">
            <li className="flex items-center justify-between">
              <span className="text-slate-500">Body Typography:</span>
              <span className="font-semibold text-slate-900 font-mono">Times New Roman 12 pt</span>
            </li>
            <li className="flex items-center justify-between">
              <span className="text-slate-500">Alignment & Spacing:</span>
              <span className="font-semibold text-slate-900 font-mono">Justified • 1.5 Line Spacing</span>
            </li>
            <li className="flex items-center justify-between">
              <span className="text-slate-500">First-Line Indent:</span>
              <span className="font-semibold text-slate-900 font-mono">1.27 cm (0.5 in)</span>
            </li>
            <li className="flex items-center justify-between">
              <span className="text-slate-500">Heading 1 / Subheading:</span>
              <span className="font-semibold text-slate-900 font-mono">16 pt Bold / 12 pt Bold</span>
            </li>
          </ul>
        </div>
      </div>

      {/* Strict Preservation Guarantee Banner */}
      <div className="p-4 bg-amber-50/70 border border-amber-200 rounded-xl flex items-start gap-3">
        <ShieldCheck className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
        <div className="text-xs text-amber-800 leading-relaxed">
          <span className="font-bold text-amber-900">Zero Content Modification Guarantee: </span>
          The formatting engine strictly updates style tags, run-level fonts, and paragraph properties.
          Original author text, words, punctuation, table cells, and figure images are never altered or paraphrased.
        </div>
      </div>

      {/* Action CTA & Progress */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-col items-center text-center space-y-4">
        {isLoading ? (
          <div className="w-full space-y-3 max-w-md py-4">
            <div className="flex items-center justify-center gap-2 text-blue-600 font-semibold text-sm">
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Applying publication typography and styles...</span>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
              <div className="bg-blue-600 h-2.5 rounded-full animate-pulse w-3/4"></div>
            </div>
            <p className="text-xs text-slate-500">
              Iterating paragraphs, standardizing margins, formatting tables & generating TOC
            </p>
          </div>
        ) : (
          <>
            <div>
              <h3 className="text-lg font-bold text-slate-900">
                Ready to Generate Publication Manuscript
              </h3>
              <p className="text-xs text-slate-500 mt-1 max-w-lg">
                Executes complete offline document formatting pass, enforces all page boundaries, and produces publication-ready DOCX.
              </p>
            </div>

            <div className="flex flex-wrap items-center justify-center gap-3">
              <button
                id="execute-format-btn"
                onClick={onExecuteFormat}
                className="px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-lg text-sm shadow-sm transition-all flex items-center gap-2"
              >
                <FileCheck2 className="w-4 h-4" />
                Format to Publication Specs
              </button>

              {formattingStats && (
                <button
                  id="download-docx-btn"
                  onClick={handleDownload}
                  className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg text-sm shadow-sm transition-all flex items-center gap-2"
                >
                  <ArrowDownToLine className="w-4 h-4" />
                  Download Formatted DOCX
                </button>
              )}
            </div>
          </>
        )}

        {downloadSuccess && (
          <div className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-3 py-1.5 rounded-md border border-emerald-200">
            Formatted DOCX file downloaded successfully!
          </div>
        )}
      </div>

      {/* Formatting Run Output Telemetry */}
      {formattingStats && (
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">
              Output Generation Telemetry
            </span>
            <span className="text-xs text-emerald-700 font-semibold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
              Execution Time: {formattingStats.elapsed_time_seconds}s
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
              <span className="text-slate-400">Paragraphs Formatted</span>
              <p className="text-base font-bold text-slate-900 mt-0.5">{formattingStats.paragraphs_formatted}</p>
            </div>
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
              <span className="text-slate-400">Tables Formatted</span>
              <p className="text-base font-bold text-slate-900 mt-0.5">{formattingStats.tables_formatted}</p>
            </div>
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
              <span className="text-slate-400">Table of Contents</span>
              <p className="text-base font-bold text-slate-900 mt-0.5">
                {formattingStats.toc_included ? "Included (Auto-generated)" : "Excluded"}
              </p>
            </div>
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
              <span className="text-slate-400">Output File Size</span>
              <p className="text-base font-bold text-slate-900 mt-0.5">
                {(formattingStats.file_size_bytes / 1024).toFixed(1)} KB
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
