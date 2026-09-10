import React from "react";
import {
  LayoutDashboard,
  Binary,
  FileCheck2,
  GitCompare,
  Gauge,
  Settings2,
  ShieldCheck,
  BookOpen,
} from "lucide-react";

export type NavPage = "dashboard" | "analyze" | "format" | "results" | "performance" | "settings";

interface SidebarProps {
  currentPage: NavPage;
  onPageSelect: (page: NavPage) => void;
  documentLoaded: boolean;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentPage,
  onPageSelect,
  documentLoaded,
}) => {
  const navItems: { id: NavPage; label: string; icon: React.ComponentType<{ className?: string }> }[] = [
    { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
    { id: "analyze", label: "Analyze Structure", icon: Binary },
    { id: "format", label: "Format Document", icon: FileCheck2 },
    { id: "results", label: "Before & After", icon: GitCompare },
    { id: "performance", label: "Performance (400p+)", icon: Gauge },
    { id: "settings", label: "Publication Specs", icon: Settings2 },
  ];

  return (
    <aside
      id="app-sidebar"
      className="w-64 bg-slate-900 text-slate-100 flex flex-col justify-between shrink-0 border-r border-slate-800 select-none"
    >
      <div>
        {/* Brand Header */}
        <div className="p-5 border-b border-slate-800/80 flex items-center space-x-3">
          <div className="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20">
            <BookOpen className="w-5 h-5" />
          </div>
          <div>
            <h1 className="font-bold text-base tracking-wide text-white flex items-center gap-1.5">
              IntelliFormat
            </h1>
            <p className="text-[11px] text-sky-400 font-medium tracking-tight">
              Offline DOCX Typesetting
            </p>
          </div>
        </div>

        {/* Navigation List */}
        <nav className="p-3 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentPage === item.id;
            return (
              <button
                key={item.id}
                id={`nav-btn-${item.id}`}
                onClick={() => onPageSelect(item.id)}
                className={`w-full flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? "bg-blue-600 text-white shadow-sm shadow-blue-600/30"
                    : "text-slate-400 hover:text-slate-100 hover:bg-slate-800/60"
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? "text-white" : "text-slate-400"}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Security & Offline Banner */}
      <div className="p-4 border-t border-slate-800">
        <div className="bg-emerald-950/40 border border-emerald-500/30 rounded-lg p-3">
          <div className="flex items-center space-x-2 text-emerald-400 font-semibold text-xs mb-1">
            <ShieldCheck className="w-4 h-4 shrink-0" />
            <span>100% OFFLINE SECURE</span>
          </div>
          <p className="text-[11px] text-emerald-200/80 leading-relaxed">
            Zero cloud APIs • No LLMs • Random Forest + Rule Heuristics
          </p>
        </div>
      </div>
    </aside>
  );
};
