"use client";

import { useState } from "react";

export default function DashboardOverview() {
    const [hoveredDay, setHoveredDay] = useState<number | null>(null);

    // Mock Data for "You vs Market" Chart
    const TRAFFIC_DATA = [
        { day: "Mon", you: 4200, market: 3100 },
        { day: "Tue", you: 4800, market: 3400 },
        { day: "Wed", you: 4100, market: 3800 },
        { day: "Thu", you: 5900, market: 4000 },
        { day: "Fri", you: 6800, market: 4200 }, // Peak
        { day: "Sat", you: 5100, market: 2900 },
        { day: "Sun", you: 4900, market: 2700 },
    ];

    const maxVal = 7000;
    const svgHeight = 400; // Increased SVG units for 1:1 ratio
    const dataRange = 320; // unit range within SVG

    const pointsYou = TRAFFIC_DATA.map((d, i) => {
        const x = (i / (TRAFFIC_DATA.length - 1)) * 1000;
        const y = svgHeight - (d.you / maxVal) * dataRange;
        return `${x},${y}`;
    }).join(" ");

    const pointsMarket = TRAFFIC_DATA.map((d, i) => {
        const x = (i / (TRAFFIC_DATA.length - 1)) * 1000;
        const y = svgHeight - (d.market / maxVal) * dataRange;
        return `${x},${y}`;
    }).join(" ");

    return (
        <div className="max-w-6xl mx-auto pb-10 fade-in" style={{ fontFamily: "var(--font-inter), sans-serif" }}>

            {/* ── HEADER ── */}
            <div className="flex flex-col md:flex-row items-end justify-between mb-8 gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Your Company Overview</h1>
                    <p className="text-[15px] font-medium text-slate-500 mt-1">Acme Corp analytics and competitive standing.</p>
                </div>

                <div className="bg-white border border-slate-200 p-1 rounded-xl flex shadow-sm">
                    <button className="px-5 py-2 text-[13px] font-bold bg-slate-900 text-white rounded-lg shadow-md transition-all">This Week</button>
                    <button className="px-5 py-2 text-[13px] font-bold text-slate-500 hover:text-slate-900 rounded-lg transition-all hover:bg-slate-50">Last Month</button>
                </div>
            </div>

            {/* ── TOP KPIs ── */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                {[
                    { label: "Unique Visitors", value: "35.8K", trend: "+12.4%", up: true, icon: "M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" },
                    { label: "Active Users", value: "12.4K", trend: "+5.2%", up: true, icon: "M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" },
                    { label: "Bounce Rate", value: "42.1%", trend: "-2.1%", up: true, icon: "M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" },
                    { label: "Market Share Est.", value: "18.5%", trend: "+1.2%", up: true, icon: "M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" }
                ].map((kpi, i) => (
                    <div key={i} className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300">
                        <div className="flex items-start justify-between mb-4">
                            <div className="w-10 h-10 rounded-xl bg-violet-50 text-violet-600 flex items-center justify-center">
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d={kpi.icon} /></svg>
                            </div>
                            <span className={`flex items-center gap-1 text-[11px] font-bold px-2 py-1 rounded-md ${kpi.up ? 'bg-emerald-50 text-emerald-600 border border-emerald-100' : 'bg-red-50 text-red-600 border border-red-100'}`}>
                                {kpi.up ? '↑' : '↓'} {kpi.trend}
                            </span>
                        </div>
                        <div className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-1">{kpi.label}</div>
                        <div className="text-3xl font-black text-slate-800 tracking-tight">{kpi.value}</div>
                    </div>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

                {/* ── LEFT: TRAFFIC VS MARKET GRAPH ── */}
                <div className="lg:col-span-2 bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
                    <div className="flex items-center justify-between border-b border-slate-100 pb-4 mb-6">
                        <div>
                            <h3 className="font-bold text-slate-900 text-lg">Traffic vs. Competitor Average</h3>
                            <p className="text-xs text-slate-500 mt-1 font-medium">Acme Corp against the aggregated top 5 tracked competitors.</p>
                        </div>
                        <div className="flex items-center gap-4">
                            <div className="flex items-center gap-2">
                                <span className="w-3 h-3 rounded bg-violet-600 shadow-[0_0_8px_rgba(124,58,237,0.4)]"></span>
                                <span className="text-xs font-bold text-slate-600">You</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <span className="w-3 h-3 rounded border-2 border-slate-300 bg-white"></span>
                                <span className="text-xs font-bold text-slate-500">Market Avg</span>
                            </div>
                        </div>
                    </div>

                    <div className="relative w-full h-[220px] pl-10 pb-6 mt-4 group/chart">

                        {/* Interactive HTML Tooltip (Fixed Distortion) */}
                        {hoveredDay !== null && (
                            <div
                                className="absolute z-30 bg-slate-900 text-white p-3 rounded-xl shadow-xl border border-slate-700 pointer-events-none transition-all duration-200"
                                style={{
                                    left: `calc(40px + ${(hoveredDay / (TRAFFIC_DATA.length - 1)) * 100}% )`,
                                    top: `${(svgHeight - (TRAFFIC_DATA[hoveredDay].you / maxVal) * dataRange) / svgHeight * 220 - 64}px`, // Scale SVG Y to HTML container Y
                                    transform: 'translateX(-50%)'
                                }}
                            >
                                <div className="text-[10px] font-bold text-slate-400 uppercase mb-1">{TRAFFIC_DATA[hoveredDay].day} Dashboard</div>
                                <div className="text-xs font-bold whitespace-nowrap">You: {TRAFFIC_DATA[hoveredDay].you} | Mkt: {TRAFFIC_DATA[hoveredDay].market}</div>
                            </div>
                        )}

                        {/* Y Axis Grid */}
                        <div className="absolute left-[40px] right-0 top-0 bottom-6 flex flex-col justify-between z-0">
                            {[7000, 5250, 3500, 1750, 0].map((val) => (
                                <div key={val} className="w-full relative">
                                    <span className="absolute -left-10 -top-2 text-[10px] font-bold text-slate-400 font-mono w-8 text-right">{val >= 1000 ? (val / 1000) + 'k' : val}</span>
                                    <div className="w-full border-t-[1.5px] border-dashed border-slate-100 h-0"></div>
                                </div>
                            ))}
                        </div>

                        {/* SVG Canvas (Clean coordinate system) */}
                        <svg className="absolute inset-0 w-full h-full pb-6 pl-[40px] z-10 overflow-visible" preserveAspectRatio="none" viewBox="0 0 1000 400">
                            <defs>
                                <filter id="glowDark" x="-20%" y="-20%" width="140%" height="140%">
                                    <feGaussianBlur stdDeviation="3" result="blur" />
                                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                                </filter>
                                <linearGradient id="youArea" x1="0" x2="0" y1="0" y2="1">
                                    <stop offset="0%" stopColor="#7c3aed" stopOpacity="0.3" />
                                    <stop offset="100%" stopColor="#7c3aed" stopOpacity="0.0" />
                                </linearGradient>
                            </defs>

                            {/* Area Fills */}
                            <polygon points={`0,${svgHeight} ${pointsYou} 1000,${svgHeight}`} fill="url(#youArea)" />

                            {/* Market Trend Line */}
                            <polyline points={pointsMarket} fill="none" stroke="#cbd5e1" strokeWidth="3" strokeDasharray="6 6" strokeLinejoin="round" strokeLinecap="round" />

                            {/* You Trend Line */}
                            <polyline points={pointsYou} fill="none" stroke="#7c3aed" strokeWidth="4" strokeLinejoin="round" strokeLinecap="round" filter="url(#glowDark)" />

                            {/* Interactive Nodes */}
                            {TRAFFIC_DATA.map((d, i) => {
                                const x = (i / (TRAFFIC_DATA.length - 1)) * 1000;
                                const youY = svgHeight - (d.you / maxVal) * dataRange;
                                const marketY = svgHeight - (d.market / maxVal) * dataRange;
                                const isHovered = hoveredDay === i;

                                return (
                                    <g key={i} onMouseEnter={() => setHoveredDay(i)} onMouseLeave={() => setHoveredDay(null)} className="cursor-crosshair">
                                        {/* Invisible hover catch block */}
                                        <rect x={x - 40} y="0" width="80" height={svgHeight} fill="transparent" />

                                        <circle cx={x} cy={marketY} r="4" fill="#ffffff" stroke="#cbd5e1" strokeWidth="2" />
                                        <circle cx={x} cy={youY} r={isHovered ? "8" : "5"} fill="#ffffff" stroke="#7c3aed" strokeWidth={isHovered ? "4" : "3"} className="transition-all duration-200" />

                                        {isHovered && (
                                            <line x1={x} y1="0" x2={x} y2={svgHeight} stroke="#cbd5e1" strokeWidth="1" strokeDasharray="3 3" />
                                        )}
                                    </g>
                                );
                            })}
                        </svg>

                        {/* X Axis Labels */}
                        <div className="absolute bottom-0 left-[40px] right-0 flex justify-between text-[11px] font-bold text-slate-400 font-mono">
                            {TRAFFIC_DATA.map(d => (
                                <span key={d.day} className="-translate-x-1/2">{d.day}</span>
                            ))}
                        </div>
                    </div>
                </div>

                {/* ── RIGHT: YOUR AI DIAGNOSTIC ── */}
                <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl relative overflow-hidden flex flex-col h-full">
                    {/* Background decoration */}
                    <div className="absolute -top-20 -right-20 w-64 h-64 bg-violet-600/30 blur-3xl rounded-full"></div>

                    <div className="flex items-center gap-2 mb-6 relative z-10">
                        <svg className="w-5 h-5 text-violet-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                        <h3 className="font-bold text-white text-lg">Acme Corp Insights</h3>
                    </div>

                    <p className="text-[13px] text-slate-300 font-medium leading-relaxed mb-6 relative z-10 border-b border-slate-700 pb-6">
                        Our Analyst Agent has benchmarked your product description and traffic against your top 3 competitors (Notion, Evernote, ClickUp).
                    </p>

                    <div className="space-y-4 mb-auto relative z-10">
                        <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-xl p-4">
                            <div className="flex items-center gap-2 mb-1.5">
                                <span className="text-xs font-bold text-emerald-400 uppercase tracking-widest">Strength</span>
                            </div>
                            <p className="text-xs text-white font-medium leading-relaxed">
                                Traffic growth outpaces market average by 18% on Thursdays. Content marketing strategy is highly effective.
                            </p>
                        </div>

                        <div className="bg-orange-500/10 border border-orange-500/20 rounded-xl p-4">
                            <div className="flex items-center gap-2 mb-1.5">
                                <span className="text-xs font-bold text-orange-400 uppercase tracking-widest">Vulnerability</span>
                            </div>
                            <p className="text-xs text-white font-medium leading-relaxed">
                                Competitors are aggressively leaning into "Local First" capabilities. Your product lacks offline functionality messaging.
                            </p>
                        </div>
                    </div>

                    <button className="w-full mt-6 py-3 bg-white/10 hover:bg-white/20 text-white rounded-xl font-bold text-sm transition-colors border border-white/10 relative z-10">
                        View Full Comparative Teardown
                    </button>
                </div>

            </div>

        </div>
    );
}
