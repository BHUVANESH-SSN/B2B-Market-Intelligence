"use client";

import { useState } from "react";

const REPORTS = [
    {
        id: "rep_1",
        title: "Q1 B2B SaaS Knowledge Management",
        description: "Executive summary of positioning shifts across Notion, Coda, and Evernote. Highlighting the trend towards local-first architecture and AI integration.",
        generated: "Today at 09:30 AM",
        agent: "Claude Sonnet 3.5 Recommender",
        pages: 12,
        size: "4.2 MB",
        status: "Ready"
    },
    {
        id: "rep_2",
        title: "Project Management Pricing Study",
        description: "Deep dive into ClickUp's new pricing model compared to Asana. Analyzes the impact of per-seat vs usage-based billing.",
        generated: "Mar 15, 2026",
        agent: "Claude Sonnet 3.5 Recommender",
        pages: 8,
        size: "2.8 MB",
        status: "Ready"
    },
    {
        id: "rep_3",
        title: "Onboarding Flow Teardowns",
        description: "Comparison of user onboarding sequences across top 5 tracked competitors. Focuses on 'Time to First Value'.",
        generated: "Feb 28, 2026",
        agent: "Scorer Agent",
        pages: 24,
        size: "12.4 MB",
        status: "Archived"
    }
];

export default function ReportsPage() {
    const [isGenerating, setIsGenerating] = useState(false);

    return (
        <div className="max-w-6xl mx-auto pb-10" style={{ fontFamily: "var(--font-inter), sans-serif" }}>

            <div className="flex flex-col md:flex-row items-end justify-between mb-10 gap-4">
                <div>
                    <div className="flex items-center gap-3 mb-2">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-500/20">
                            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                        </div>
                        <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Strategy Reports</h1>
                    </div>
                    <p className="text-[15px] font-medium text-slate-500 ml-13">Deep-dive synthesized executive reports compiled by the Recommender Agent.</p>
                </div>

                <button
                    onClick={() => setIsGenerating(true)}
                    disabled={isGenerating}
                    className={`px-6 py-3 rounded-xl font-bold text-[13px] shadow-md transition-all flex items-center gap-2 ${isGenerating
                            ? "bg-slate-100 text-slate-400 border border-slate-200 shadow-none cursor-wait"
                            : "bg-slate-900 hover:bg-slate-800 text-white shadow-slate-900/20 hover:shadow-lg hover:-translate-y-0.5"
                        }`}
                >
                    {isGenerating ? (
                        <>
                            <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" /><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" /></svg>
                            Agent is synthesizing Data...
                        </>
                    ) : (
                        <>
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M12 4v16m8-8H4" /></svg>
                            Generate New Report
                        </>
                    )}
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

                {/* Loading Skeleton */}
                {isGenerating && (
                    <div className="bg-white border-2 border-dashed border-violet-200 rounded-3xl p-6 shadow-sm flex flex-col items-center justify-center text-center animate-pulse h-[320px]">
                        <div className="w-16 h-16 rounded-full bg-violet-50 flex items-center justify-center mb-4">
                            <svg className="w-8 h-8 text-violet-500 animate-spin" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" /><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" /></svg>
                        </div>
                        <h3 className="font-bold text-slate-800 mb-2">Analyzing 320 Recent Signals</h3>
                        <p className="text-xs text-slate-400 font-medium px-4">The Recommender agent is compiling cross-domain trends and structuring the final executive PDF.</p>
                    </div>
                )}

                {REPORTS.map((report, i) => (
                    <div
                        key={report.id}
                        className="group relative bg-white border border-slate-200 hover:border-violet-300 rounded-3xl p-6 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 flex flex-col h-[320px] overflow-hidden"
                        style={{ animationDelay: `${i * 100}ms` }}
                    >
                        {/* Top decorative folder tab */}
                        <div className="absolute top-0 right-6 w-16 h-1.5 bg-violet-500 rounded-b-md opacity-0 group-hover:opacity-100 transition-opacity"></div>

                        <div className="flex items-start justify-between mb-4">
                            <div className="w-12 h-12 bg-slate-50 border border-slate-100 rounded-xl flex items-center justify-center text-violet-500 group-hover:bg-violet-50 transition-colors shrink-0 shadow-inner">
                                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                            </div>
                            <div className={`px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-widest border ${report.status === 'Ready'
                                    ? 'bg-emerald-50 text-emerald-600 border-emerald-200'
                                    : 'bg-slate-50 text-slate-400 border-slate-200'
                                }`}>
                                {report.status}
                            </div>
                        </div>

                        <h3 className="text-lg font-bold text-slate-900 mb-3 group-hover:text-violet-700 transition-colors leading-snug">{report.title}</h3>

                        <p className="text-[13px] text-slate-500 flex-1 leading-relaxed mb-6 font-medium">
                            {report.description}
                        </p>

                        <div className="space-y-4 pt-4 border-t border-slate-100 mt-auto">
                            <div className="flex items-center gap-3">
                                <div className="w-6 h-6 rounded-md bg-orange-100 text-orange-600 flex items-center justify-center shrink-0">
                                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                                </div>
                                <div>
                                    <div className="text-[9px] font-bold text-slate-400 uppercase tracking-widest">Compiled By</div>
                                    <div className="text-[11px] font-bold text-slate-700">{report.agent}</div>
                                </div>
                            </div>

                            <div className="flex items-center justify-between text-[11px] font-bold text-slate-400">
                                <div className="flex items-center gap-4">
                                    <span>{report.pages} Pages</span>
                                    <span>{report.size}</span>
                                </div>
                                <span>{report.generated}</span>
                            </div>
                        </div>

                        {/* Hover Actions Bar */}
                        <div className="absolute inset-x-0 bottom-0 p-4 bg-white/80 backdrop-blur-sm border-t border-slate-100 translate-y-full group-hover:translate-y-0 transition-transform duration-300 flex items-center gap-2">
                            <button className="flex-1 bg-violet-600 hover:bg-violet-700 text-white py-2.5 rounded-xl text-xs font-bold transition-colors">
                                View Report
                            </button>
                            <button className="w-10 h-10 bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-600 rounded-xl flex items-center justify-center transition-colors">
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
                            </button>
                        </div>

                    </div>
                ))}
            </div>

        </div>
    );
}
