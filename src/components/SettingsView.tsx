import React from "react";
import { Settings2, RotateCcw, Check, Shield } from "lucide-react";
import { PublicationSpecs } from "../types";

interface SettingsViewProps {
  specs: PublicationSpecs;
  onUpdateSpecs: (newSpecs: PublicationSpecs) => void;
  onResetDefaults: () => void;
}

export const SettingsView: React.FC<SettingsViewProps> = ({
  specs,
  onUpdateSpecs,
  onResetDefaults,
}) => {
  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Title */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Settings2 className="w-6 h-6 text-blue-600" />
            Publication & Typesetting Settings
          </h2>
          <p className="text-sm text-slate-500 mt-1">
            Configure document geometry, typography, and headings. Standard publication specifications are preserved by default.
          </p>
        </div>

        <button
          onClick={onResetDefaults}
          className="px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold transition-colors flex items-center gap-1.5"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          Reset to Defaults
        </button>
      </div>

      {/* Margin Settings Card */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-4">
        <h3 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-2">
          Page Dimensions & Margin Boundaries (Centimeters)
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div>
            <label className="block text-slate-600 font-medium mb-1">Top Margin (cm)</label>
            <input
              type="number"
              step="0.01"
              value={specs.top_margin_cm}
              onChange={(e) => onUpdateSpecs({ ...specs, top_margin_cm: parseFloat(e.target.value) || 1.52 })}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg font-mono"
            />
            <span className="text-[11px] text-slate-400 mt-0.5 block">Standard: 1.52 cm</span>
          </div>

          <div>
            <label className="block text-slate-600 font-medium mb-1">Bottom Margin (cm)</label>
            <input
              type="number"
              step="0.01"
              value={specs.bottom_margin_cm}
              onChange={(e) => onUpdateSpecs({ ...specs, bottom_margin_cm: parseFloat(e.target.value) || 1.52 })}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg font-mono"
            />
            <span className="text-[11px] text-slate-400 mt-0.5 block">Standard: 1.52 cm</span>
          </div>

          <div>
            <label className="block text-slate-600 font-medium mb-1">Left Margin (cm)</label>
            <input
              type="number"
              step="0.01"
              value={specs.left_margin_cm}
              onChange={(e) => onUpdateSpecs({ ...specs, left_margin_cm: parseFloat(e.target.value) || 1.97 })}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg font-mono"
            />
            <span className="text-[11px] text-slate-400 mt-0.5 block">Standard: 1.97 cm</span>
          </div>

          <div>
            <label className="block text-slate-600 font-medium mb-1">Right Margin (cm)</label>
            <input
              type="number"
              step="0.01"
              value={specs.right_margin_cm}
              onChange={(e) => onUpdateSpecs({ ...specs, right_margin_cm: parseFloat(e.target.value) || 1.96 })}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg font-mono"
            />
            <span className="text-[11px] text-slate-400 mt-0.5 block">Standard: 1.96 cm</span>
          </div>
        </div>
      </div>

      {/* Typography Settings Card */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-4">
        <h3 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-2">
          Typography & Paragraph Spacing
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div>
            <label className="block text-slate-600 font-medium mb-1">Font Family</label>
            <input
              type="text"
              disabled
              value="Times New Roman (Locked to Specification)"
              className="w-full px-3 py-2 bg-slate-100 border border-slate-200 rounded-lg text-slate-500 font-serif"
            />
          </div>

          <div>
            <label className="block text-slate-600 font-medium mb-1">Body Font Size (pt)</label>
            <input
              type="number"
              disabled
              value="12.0"
              className="w-full px-3 py-2 bg-slate-100 border border-slate-200 rounded-lg text-slate-500 font-mono"
            />
          </div>

          <div>
            <label className="block text-slate-600 font-medium mb-1">Body Line Spacing</label>
            <input
              type="number"
              step="0.1"
              value={specs.body_line_spacing}
              onChange={(e) => onUpdateSpecs({ ...specs, body_line_spacing: parseFloat(e.target.value) || 1.5 })}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg font-mono"
            />
            <span className="text-[11px] text-slate-400 mt-0.5 block">Standard: 1.5 line spacing</span>
          </div>

          <div>
            <label className="block text-slate-600 font-medium mb-1">First-line Indentation (cm)</label>
            <input
              type="number"
              step="0.01"
              value={specs.first_line_indent_cm}
              onChange={(e) => onUpdateSpecs({ ...specs, first_line_indent_cm: parseFloat(e.target.value) || 1.27 })}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg font-mono"
            />
            <span className="text-[11px] text-slate-400 mt-0.5 block">Standard: 1.27 cm (0.5 inch)</span>
          </div>
        </div>
      </div>

      {/* Options & Table of Contents */}
      <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm space-y-3">
        <h3 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-2">
          Structural Table of Contents Generation
        </h3>

        <div className="flex items-center justify-between text-xs pt-1">
          <div>
            <div className="font-semibold text-slate-900">Auto-Generate Table of Contents</div>
            <div className="text-slate-500">
              Builds a structured Table of Contents from detected Chapter Headings and Subheadings.
            </div>
          </div>
          <input
            type="checkbox"
            checked={specs.include_toc}
            onChange={(e) => onUpdateSpecs({ ...specs, include_toc: e.target.checked })}
            className="w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"
          />
        </div>
      </div>
    </div>
  );
};
