"use client";

const MOCK_INSIGHTS = [
    {
        id: "ins_1",
        company: "Notion",
        category: "Pricing",
        title: "New AI Add-on Price Increase",
        description: "Notion has updated its pricing page. The AI add-on price has increased from $8 to $10 per user/month, signaling strong demand and value lock-in.",
        impact: "High",
        impactColor: "from-orange-400 to-red-500 text-white shadow-orange-500/30",
        date: "2 hours ago",
        icon: "💰"
    },
    {
        id: "ins_2",
        company: "ClickUp",
        category: "Features",
        title: "Launched Brain 3.0",
        description: "ClickUp Brain has been heavily promoted on their homepage. They added automated stand-up summaries and smart thread summarization.",
        impact: "Medium",
        impactColor: "from-blue-400 to-violet-500 text-white shadow-blue-500/30",
        date: "5 hours ago",
        icon: "✨"
    },
    {
        id: "ins_3",
        company: "Evernote",
        category: "Messaging",
        title: "Shifted focus to 'Local first'",
        description: "Evernote's hero copy changed from 'Tame your work, organize your life' to emphasizing local-first offline syncing capabilities. They are targeting power users.",
        impact: "Low",
        impactColor: "from-slate-300 to-slate-400 text-slate-800 shadow-slate-400/20",
        date: "1 day ago",
        icon: "📝"
    },
    {
        id: "ins_4",
        company: "Coda",
        category: "Features",
        title: "Two-way Sync Improvements",
        description: "Coda deployed a major update to their Salesforce and Jira packs, allowing instant bidirectional syncing.",
        impact: "Medium",
        impactColor: "from-blue-400 to-violet-500 text-white shadow-blue-500/30",
        date: "2 days ago",
        icon: "🔄"
    }
];

export default function InsightsPage() {
    return (
        <div className="max-w-5xl mx-auto pb-10" style={{ fontFamily: "var(--font-inter), sans-serif" }}>

            {/* ── HEADER ── */}
            <div className="flex flex-col md:flex-row items-start md:items-end justify-between mb-10 gap-4">
                <div>
                    <div className="flex items-center gap-3 mb-2">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-600 to-orange-400 flex items-center justify-center shadow-lg shadow-violet-500/20">
                            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                        </div>
                        <h1 className="text-3xl font-bold text-slate-900 tracking-tight">AI Analyst Insights</h1>
                    </div>
                    <p className="text-[15px] font-medium text-slate-500 ml-13">Real-time intelligence categorized by pricing, features, and messaging shifts.</p>
                </div>

                {/* Filters */}
                <div className="flex bg-white border border-slate-200 p-1 rounded-xl shadow-sm">
                    <button className="px-5 py-2 bg-slate-900 text-white rounded-lg text-xs font-bold shadow-md transition-all">All Streams</button>
                    <button className="px-5 py-2 text-slate-500 hover:text-slate-800 rounded-lg text-xs font-bold transition-all hover:bg-slate-50">Pricing</button>
                    <button className="px-5 py-2 text-slate-500 hover:text-slate-800 rounded-lg text-xs font-bold transition-all hover:bg-slate-50">Features</button>
                    <button className="px-5 py-2 text-slate-500 hover:text-slate-800 rounded-lg text-xs font-bold transition-all hover:bg-slate-50">Messaging</button>
                </div>
            </div>

            <div className="flex gap-8">

                {/* ── LEFT: TIMELINE FEED ── */}
                <div className="flex-1 space-y-6 relative border-l-2 border-slate-100 pl-8 ml-4">

                    {MOCK_INSIGHTS.map((insight, i) => (
                        <div
                            key={insight.id}
                            className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm hover:shadow-xl hover:-translate-y-1 hover:border-violet-300 transition-all duration-300 group relative"
                            style={{ animationDelay: `${i * 100}ms` }}
                        >
                            {/* Timeline Connector Dot */}
                            <div className="absolute top-8 -left-[41px] w-4 h-4 rounded-full bg-white border-4 border-violet-500 shadow-sm z-10 transition-transform group-hover:scale-125"></div>

                            <div className="flex items-start justify-between mb-4">
                                <div className="flex items-center gap-3">
                                    <div className="w-12 h-12 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-center text-xl shadow-inner group-hover:bg-violet-50 transition-colors">
                                        {insight.icon}
                                    </div>
                                    <div>
                                        <div className="flex items-center gap-2 mb-0.5">
                                            <span className="text-sm font-bold text-slate-900">{insight.company}</span>
                                            <span className="w-1.5 h-1.5 rounded-full bg-slate-300"></span>
                                            <span className="text-xs font-bold text-violet-600 bg-violet-50 px-2 py-0.5 rounded-md uppercase tracking-wide">
                                                {insight.category}
                                            </span>
                                        </div>
                                        <div className="text-[11px] text-slate-400 font-semibold">{insight.date}</div>
                                    </div>
                                </div>

                                {/* Impact Badge */}
                                <div className={`px-3 py-1 bg-gradient-to-r rounded-lg font-bold text-[10px] uppercase tracking-widest shadow-md flex items-center gap-1 ${insight.impactColor}`}>
                                    {insight.impact} IMPACT
                                </div>
                            </div>

                            <div className="pl-[60px]">
                                <h3 className="font-bold text-slate-800 text-lg mb-2 group-hover:text-violet-700 transition-colors">{insight.title}</h3>
                                <p className="text-slate-500 text-[14px] leading-relaxed mb-4 font-medium">
                                    {insight.description}
                                </p>

                                {/* AI Justification Box */}
                                <div className="bg-slate-50 border border-slate-100 rounded-xl p-4 flex gap-3 opacity-0 h-0 overflow-hidden group-hover:opacity-100 group-hover:h-auto group-hover:mt-4 transition-all duration-300">
                                    <svg className="w-5 h-5 text-violet-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
                                    <div>
                                        <div className="text-[11px] font-bold text-violet-600 uppercase tracking-widest mb-1">AI Analysis</div>
                                        <p className="text-xs text-slate-600 font-medium leading-relaxed">
                                            This change strongly correlates with competitor strategy shifts seen in Q4. Recommend adjusting our positioning matrix to emphasize cost-efficiency.
                                        </p>
                                    </div>
                                </div>
                            </div>

                        </div>
                    ))}
                </div>

                {/* ── RIGHT: SUMMARY PANEL ── */}
                <div className="w-[300px] shrink-0 hidden lg:block">
                    <div className="sticky top-24 bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
                        <h3 className="font-bold text-slate-800 mb-4 text-sm uppercase tracking-widest border-b border-slate-100 pb-3">Intelligence Summary</h3>

                        <div className="space-y-4 mb-6">
                            <div className="flex justify-between items-center">
                                <span className="text-sm font-medium text-slate-500">Unread Signals</span>
                                <span className="w-6 h-6 rounded-full bg-violet-100 text-violet-700 flex items-center justify-center text-xs font-bold">4</span>
                            </div>
                            <div className="flex justify-between items-center">
                                <span className="text-sm font-medium text-slate-500">High Impact</span>
                                <span className="w-6 h-6 rounded-full bg-orange-100 text-orange-600 flex items-center justify-center text-xs font-bold">1</span>
                            </div>
                            <div className="flex justify-between items-center">
                                <span className="text-sm font-medium text-slate-500">Companies Tracked</span>
                                <span className="text-sm font-bold text-slate-800">12</span>
                            </div>
                        </div>

                        <button className="w-full py-3 bg-violet-600 hover:bg-violet-700 text-white rounded-xl font-bold text-sm transition-all shadow-md shadow-violet-500/20">
                            Run Real-time Scan
                        </button>
                    </div>
                </div>

            </div>
        </div>
    );
}
