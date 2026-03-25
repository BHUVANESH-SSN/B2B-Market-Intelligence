"use client";

import { useState } from "react";

// ── Mock AI Results ──────────────────────────────────────────────
const MOCK_RESULTS: Record<string, { name: string; domain: string; desc: string; similarity: number; category: string }[]> = {
    default: [
        { name: "Notion", domain: "notion.so", desc: "All-in-one workspace for notes, docs & databases", similarity: 95, category: "Productivity" },
        { name: "Evernote", domain: "evernote.com", desc: "Note-taking app with powerful organization tools", similarity: 90, category: "Productivity" },
        { name: "ClickUp", domain: "clickup.com", desc: "Project management + docs in one platform", similarity: 87, category: "Project Mgmt" },
        { name: "Obsidian", domain: "obsidian.md", desc: "Knowledge base on top of local Markdown files", similarity: 83, category: "Knowledge" },
        { name: "Coda", domain: "coda.io", desc: "Docs that unite words, data, and teams", similarity: 79, category: "Collaboration" },
    ],
};

function SimilarityBar({ pct }: { pct: number }) {
    const color = pct >= 90 ? "bg-emerald-500" : pct >= 80 ? "bg-violet-500" : "bg-orange-400";
    return (
        <div className="flex items-center gap-2">
            <div className="w-24 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                <div className={`h-full rounded-full ${color} transition-all duration-700`} style={{ width: `${pct}%` }} />
            </div>
            <span className="text-xs font-bold text-slate-600">{pct}%</span>
        </div>
    );
}

export default function DiscoverPage() {
    const [productName, setProductName] = useState("");
    const [description, setDescription] = useState("");
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState<typeof MOCK_RESULTS["default"] | null>(null);
    const [added, setAdded] = useState<Set<string>>(new Set());

    const handleDiscover = () => {
        if (!productName.trim() && !description.trim()) return;
        setLoading(true);
        setResults(null);
        // Simulate AI delay
        setTimeout(() => {
            setLoading(false);
            setResults(MOCK_RESULTS.default);
        }, 1800);
    };

    const handleAdd = (name: string) => {
        setAdded(prev => new Set([...prev, name]));
    };

    const canSearch = productName.trim() || description.trim();

    return (
        <div className="max-w-3xl mx-auto py-10 px-4" style={{ fontFamily: "var(--font-inter), sans-serif" }}>

            {/* ── PAGE HEADER ─────────────────────────────────────────── */}
            <div className="mb-8">
                <div className="flex items-center gap-3 mb-2">
                    <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-violet-600 to-blue-500 flex items-center justify-center shadow-md">
                        <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                    </div>
                    <h1 className="text-2xl font-bold text-slate-800 tracking-tight">Find Competitors</h1>
                </div>
                <p className="text-slate-500 text-sm ml-12">
                    Describe your product and we&apos;ll automatically discover similar companies using AI.
                </p>
            </div>

            {/* ── INPUT CARD ──────────────────────────────────────────── */}
            <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6 mb-6">
                <div className="flex items-center gap-2 mb-5">
                    <span className="text-sm font-semibold text-slate-700">Tell us about your product</span>
                    <span className="text-xs text-slate-400">— use one or both fields</span>
                </div>

                {/* Product Name */}
                <div className="mb-4">
                    <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5">
                        Product Name
                    </label>
                    <input
                        type="text"
                        value={productName}
                        onChange={(e) => setProductName(e.target.value)}
                        placeholder="e.g. Notion, Slack, HubSpot..."
                        className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-800 placeholder-slate-400 outline-none focus:border-violet-500 focus:ring-2 focus:ring-violet-500/10 transition-all"
                    />
                </div>

                {/* Divider */}
                <div className="flex items-center gap-3 my-4">
                    <div className="flex-1 h-px bg-slate-100" />
                    <span className="text-xs font-semibold text-slate-400">OR</span>
                    <div className="flex-1 h-px bg-slate-100" />
                </div>

                {/* Description */}
                <div className="mb-6">
                    <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-1.5">
                        Product Description
                    </label>
                    <textarea
                        rows={3}
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        placeholder="e.g. AI-powered note-taking workspace for teams that combines docs, databases and wikis..."
                        className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-800 placeholder-slate-400 outline-none focus:border-violet-500 focus:ring-2 focus:ring-violet-500/10 transition-all resize-none"
                    />
                </div>

                {/* Submit Button */}
                <button
                    onClick={handleDiscover}
                    disabled={!canSearch || loading}
                    className={`w-full py-3.5 rounded-xl font-semibold text-sm flex items-center justify-center gap-2 transition-all shadow-md
            ${canSearch && !loading
                            ? "bg-slate-900 hover:bg-slate-800 text-white hover:shadow-lg"
                            : "bg-slate-100 text-slate-400 cursor-not-allowed shadow-none"
                        }`}
                >
                    {loading ? (
                        <>
                            <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
                            </svg>
                            Discovering competitors...
                        </>
                    ) : (
                        <>
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                            </svg>
                            Find Competitors
                        </>
                    )}
                </button>
            </div>

            {/* ── RESULTS ─────────────────────────────────────────────── */}
            {results && (
                <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
                    {/* Results Header */}
                    <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <span className="text-sm font-bold text-slate-800">
                                🔎 Suggested Competitors
                            </span>
                            <span className="bg-violet-100 text-violet-700 text-xs font-bold px-2 py-0.5 rounded-full">
                                {results.length} found
                            </span>
                        </div>
                        <span className="text-xs text-slate-400">AI-ranked by similarity</span>
                    </div>

                    {/* Result Rows */}
                    <div className="divide-y divide-slate-50">
                        {results.map((company, i) => (
                            <div
                                key={company.name}
                                className="flex items-center gap-4 px-6 py-4 hover:bg-slate-50 transition-colors group"
                                style={{ animationDelay: `${i * 80}ms` }}
                            >
                                {/* Rank */}
                                <div className="w-6 text-center text-xs font-bold text-slate-400">
                                    #{i + 1}
                                </div>

                                {/* Avatar */}
                                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-slate-100 to-slate-200 flex items-center justify-center text-slate-600 font-bold text-sm shrink-0 ring-1 ring-slate-200">
                                    {company.name[0]}
                                </div>

                                {/* Info */}
                                <div className="flex-1 min-w-0">
                                    <div className="flex items-center gap-2 mb-0.5">
                                        <span className="text-sm font-semibold text-slate-800">{company.name}</span>
                                        <span className="text-xs text-slate-400">{company.domain}</span>
                                        <span className="text-[10px] font-bold text-slate-500 bg-slate-100 px-1.5 py-0.5 rounded">
                                            {company.category}
                                        </span>
                                    </div>
                                    <p className="text-xs text-slate-500 truncate">{company.desc}</p>
                                </div>

                                {/* Similarity */}
                                <div className="shrink-0 text-right">
                                    <div className="text-[10px] text-slate-400 mb-1 font-medium">Similarity</div>
                                    <SimilarityBar pct={company.similarity} />
                                </div>

                                {/* Add Button */}
                                <div className="shrink-0">
                                    {added.has(company.name) ? (
                                        <span className="flex items-center gap-1.5 text-xs font-semibold text-emerald-600 bg-emerald-50 border border-emerald-200 px-3 py-2 rounded-lg">
                                            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M5 13l4 4L19 7" />
                                            </svg>
                                            Added
                                        </span>
                                    ) : (
                                        <button
                                            onClick={() => handleAdd(company.name)}
                                            className="flex items-center gap-1.5 text-xs font-semibold text-violet-700 bg-violet-50 hover:bg-violet-100 border border-violet-200 hover:border-violet-400 px-3 py-2 rounded-lg transition-all"
                                        >
                                            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M12 4v16m8-8H4" />
                                            </svg>
                                            Add
                                        </button>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Footer */}
                    <div className="px-6 py-3 bg-slate-50 border-t border-slate-100 flex items-center justify-between">
                        <span className="text-xs text-slate-400">Results generated by AI · Not real-time data</span>
                        <button
                            onClick={() => { setResults(null); setProductName(""); setDescription(""); setAdded(new Set()); }}
                            className="text-xs font-semibold text-slate-500 hover:text-slate-800 transition-colors"
                        >
                            Clear
                        </button>
                    </div>
                </div>
            )}

            {/* ── EMPTY STATE (before search) ─────────────────────────── */}
            {!results && !loading && (
                <div className="text-center py-12 text-slate-400">
                    <div className="w-14 h-14 bg-slate-100 rounded-2xl flex items-center justify-center mx-auto mb-4 ring-1 ring-slate-200">
                        <svg className="w-7 h-7 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                        </svg>
                    </div>
                    <p className="text-sm font-medium text-slate-500">Enter your product name or description above</p>
                    <p className="text-xs text-slate-400 mt-1">AI will suggest the most similar companies</p>
                </div>
            )}

        </div>
    );
}
