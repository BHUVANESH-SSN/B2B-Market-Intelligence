"use client";
import { useState } from "react";

const COMPETITORS = [
    {
        id: "comp_1",
        name: "Notion",
        url: "https://notion.so",
        description: "The all-in-one workspace for your notes, tasks, wikis, and databases. Highly customizable block-based architecture.",
        status: "Active Tracking",
        lastScraped: "2 hours ago",
        changeCount: 14
    },
    {
        id: "comp_2",
        name: "Evernote",
        url: "https://evernote.com",
        description: "Note taking app that helps you capture and prioritize ideas, projects and to-do lists, so nothing falls through the cracks.",
        status: "Active Tracking",
        lastScraped: "5 hours ago",
        changeCount: 3
    },
    {
        id: "comp_3",
        name: "ClickUp",
        url: "https://clickup.com",
        description: "One app to replace them all. It's the future of work. More than just task management - offers docs, reminders, goals, calendars.",
        status: "Active Tracking",
        lastScraped: "1 day ago",
        changeCount: 28
    }
];

export default function CompetitorsPage() {
    const [showAddForm, setShowAddForm] = useState(false);
    const [newUrl, setNewUrl] = useState("");
    const [newDesc, setNewDesc] = useState("");
    const [isAdding, setIsAdding] = useState(false);

    const handleAdd = () => {
        if (!newUrl) return;
        setIsAdding(true);
        setTimeout(() => {
            setIsAdding(false);
            setShowAddForm(false);
            setNewUrl("");
            setNewDesc("");
        }, 1200);
    };

    return (
        <div className="max-w-5xl mx-auto pb-10" style={{ fontFamily: "var(--font-inter), sans-serif" }}>

            {/* ── HEADER ── */}
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-slate-800 tracking-tight">Tracked Competitors</h1>
                    <p className="text-sm text-slate-500 mt-1">Manage the companies you are monitoring for feature and pricing changes.</p>
                </div>
                <button
                    onClick={() => setShowAddForm(!showAddForm)}
                    className="bg-slate-900 hover:bg-slate-800 text-white px-5 py-2.5 rounded-xl font-bold text-sm shadow-md transition-all flex items-center gap-2"
                >
                    {showAddForm ? (
                        <>Cancel</>
                    ) : (
                        <>
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M12 4v16m8-8H4" /></svg>
                            Add Competitor
                        </>
                    )}
                </button>
            </div>

            {/* ── ADD COMPETITOR FORM ── */}
            {showAddForm && (
                <div className="bg-white border-2 border-dashed border-violet-200 rounded-2xl p-6 mb-8 shadow-sm flex flex-col md:flex-row gap-6 animate-[fadeUp_0.3s_ease_both]">
                    <div className="flex-1">
                        <label className="block text-[11px] font-bold text-slate-500 uppercase tracking-widest mb-1.5">Competitor URL</label>
                        <input
                            type="url"
                            placeholder="e.g. https://asana.com"
                            value={newUrl}
                            onChange={(e) => setNewUrl(e.target.value)}
                            className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-[13px] outline-none focus:border-violet-500 transition-colors"
                        />
                    </div>
                    <div className="flex-[2]">
                        <label className="block text-[11px] font-bold text-slate-500 uppercase tracking-widest mb-1.5">Product Description (Optional AI Hint)</label>
                        <input
                            type="text"
                            placeholder="e.g. A project management tool focused on agile software teams."
                            value={newDesc}
                            onChange={(e) => setNewDesc(e.target.value)}
                            className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-[13px] outline-none focus:border-violet-500 transition-colors"
                        />
                    </div>
                    <div className="flex items-end">
                        <button
                            onClick={handleAdd}
                            disabled={isAdding || !newUrl}
                            className={`px-8 py-3 rounded-xl font-bold text-[13px] transition-all flex items-center gap-2 ${isAdding || !newUrl ? "bg-slate-100 text-slate-400 cursor-not-allowed" : "bg-violet-600 hover:bg-violet-700 text-white shadow-md shadow-violet-500/20"
                                }`}
                        >
                            {isAdding ? "Adding..." : "Track"}
                        </button>
                    </div>
                </div>
            )}

            {/* ── GRID ── */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {COMPETITORS.map((comp) => (
                    <div key={comp.id} className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm hover:shadow-md hover:border-violet-300 transition-all group flex flex-col h-full">

                        {/* Card Header */}
                        <div className="flex items-start justify-between mb-4">
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center text-lg font-bold text-slate-600 ring-1 ring-slate-200">
                                    {comp.name.charAt(0)}
                                </div>
                                <div>
                                    <h3 className="font-bold text-slate-800">{comp.name}</h3>
                                    <a href={comp.url} target="_blank" rel="noreferrer" className="text-xs text-blue-500 hover:text-blue-700 hover:underline">
                                        {comp.url.replace('https://', '')}
                                    </a>
                                </div>
                            </div>
                            <button className="text-slate-400 hover:text-slate-600 transition-colors">
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" /></svg>
                            </button>
                        </div>

                        {/* Description */}
                        <p className="text-sm text-slate-600 leading-relaxed mb-6 flex-1">
                            {comp.description}
                        </p>

                        {/* Footer Metrics */}
                        <div className="pt-4 border-t border-slate-100 flex items-center justify-between mt-auto">
                            <div className="flex items-center gap-1.5">
                                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                                <span className="text-xs font-semibold text-slate-500">{comp.status}</span>
                            </div>

                            <div className="flex items-center gap-3">
                                {comp.changeCount > 0 && (
                                    <span className="bg-orange-50 text-orange-600 text-[10px] font-bold px-2 py-0.5 rounded border border-orange-100">
                                        {comp.changeCount} new signals
                                    </span>
                                )}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
