import React, { useState } from "react";
import {
  ClassificationItem,
  AnalysisResponse,
} from "../types";
import {
  Binary,
  Search,
  CheckCircle2,
  Cpu,
  Sliders,
  Filter,
  Layers,
} from "lucide-react";

interface AnalyzeViewProps {
  analysis: AnalysisResponse | null;
  onRunAnalysis: () => void;
  isLoading: boolean;
}

export const AnalyzeView: React.FC<AnalyzeViewProps> = ({
  analysis,
  onRunAnalysis,
  isLoading,
}) => {
  const [searchFilter, setSearchFilter] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("ALL");

  const classifications = analysis?.classifications || [];
  const distribution = analysis?.class_distribution || {};

  const filteredItems = classifications.filter((item) => {
    const matchesSearch = item.clean_text.toLowerCase().includes(searchFilter.toLowerCase());
    const matchesCategory = selectedCategory === "ALL" || item.final_class === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const getBadgeStyle = (cls: string) => {
    switch (cls) {
      case "TITLE":
        return "bg-purple-100 text-purple-800 border-purple-200";
      case "AUTHOR":
        return "bg-indigo-100 text-indigo-800 border-indigo-200";
      case "CHAPTER_HEADING":
        return "bg-blue-100 text-blue-800 border-blue-200 font-bold";
      case "SUBHEADING":
        return "bg-sky-100 text-sky-800 border-sky-200";
      case "CAPTION":
        return "bg-amber-100 text-amber-800 border-amber-200";
      case "REFERENCE":
        return "bg-rose-100 text-rose-800 border-rose-200";
      case "NUMBERED_LIST":
      case "BULLET_LIST":
        return "bg-emerald-100 text-emerald-800 border-emerald-200";
      default:
        return "bg-slate-100 text-slate-700 border-slate-200";
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* View Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Binary className="w-6 h-6 text-blue-600" />
            Structural Classification & Feature Engine
          </h2>
          <p className="text-sm text-slate-500 mt-1">
            Hybrid Random Forest (36 features) + Deterministic Document Object Model heuristics.
          </p>
        </div>

        <button
          onClick={onRunAnalysis}
          disabled={isLoading}
          className="px-4 py-2.5 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium rounded-lg text-sm shadow-sm transition-colors flex items-center justify-center gap-2"
        >
          <Cpu className="w-4 h-4" />
          {isLoading ? "Classifying Structure..." : "Re-Run Classification"}
        </button>
      </div>

      {/* Distribution Chips */}
      {Object.keys(distribution).length > 0 && (
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center space-x-2 text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">
            <Layers className="w-4 h-4 text-blue-600" />
            <span>Detected Structural Distribution</span>
          </div>

          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setSelectedCategory("ALL")}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
                selectedCategory === "ALL"
                  ? "bg-slate-900 text-white border-slate-900 shadow-sm"
                  : "bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100"
              }`}
            >
              All Elements ({classifications.length})
            </button>

            {Object.entries(distribution).map(([cls, count]) => (
              <button
                key={cls}
                onClick={() => setSelectedCategory(cls)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all flex items-center gap-1.5 ${
                  selectedCategory === cls
                    ? "bg-blue-600 text-white border-blue-600 shadow-sm"
                    : "bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100"
                }`}
              >
                <span>{cls.replace("_", " ")}</span>
                <span
                  className={`px-1.5 py-0.2 rounded text-[10px] font-bold ${
                    selectedCategory === cls ? "bg-blue-800 text-white" : "bg-slate-200 text-slate-700"
                  }`}
                >
                  {count}
                </span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Search & Filter Bar */}
      <div className="flex items-center gap-3 bg-white p-3 rounded-xl border border-slate-200 shadow-sm">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Search paragraph text or keywords..."
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            className="w-full pl-9 pr-4 py-1.5 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <span className="text-xs text-slate-500 font-medium px-2">
          Showing {filteredItems.length} of {classifications.length}
        </span>
      </div>

      {/* Structure Classification Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto max-h-[500px]">
          <table className="w-full text-left border-collapse">
            <thead className="bg-slate-50 text-slate-600 text-xs uppercase font-semibold border-b border-slate-200 sticky top-0 z-10">
              <tr>
                <th className="p-3 w-16 text-center">Idx</th>
                <th className="p-3 w-40">Class</th>
                <th className="p-3 w-28 text-center">Confidence</th>
                <th className="p-3 w-52">Decision Source</th>
                <th className="p-3">Paragraph Snippet</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-sm">
              {filteredItems.length === 0 ? (
                <tr>
                  <td colSpan={5} className="p-8 text-center text-slate-400">
                    No matching paragraphs found.
                  </td>
                </tr>
              ) : (
                filteredItems.map((item) => (
                  <tr key={item.paragraph_index} className="hover:bg-slate-50/70 transition-colors">
                    <td className="p-3 text-center font-mono text-xs text-slate-400">
                      #{item.paragraph_index + 1}
                    </td>
                    <td className="p-3">
                      <span
                        className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-semibold border ${getBadgeStyle(
                          item.final_class
                        )}`}
                      >
                        {item.final_class}
                      </span>
                    </td>
                    <td className="p-3 text-center">
                      <span className="inline-flex items-center gap-1 font-mono text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                        <CheckCircle2 className="w-3 h-3" />
                        {item.confidence_percent}%
                      </span>
                    </td>
                    <td className="p-3 text-xs text-slate-600">
                      <div className="font-medium text-slate-700">{item.decision_source}</div>
                      <div className="text-[11px] text-slate-400 truncate max-w-xs">{item.reason}</div>
                    </td>
                    <td className="p-3 text-xs text-slate-700 font-serif leading-relaxed">
                      <p className="line-clamp-2">{item.clean_text}</p>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
