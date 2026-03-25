"use client";

import { useState } from "react";

const DATA_POINTS = [
    { day: "Mar 1", value: 30, events: 2 },
    { day: "Mar 4", value: 45, events: 4 },
    { day: "Mar 7", value: 40, events: 3 },
    { day: "Mar 10", value: 65, events: 7 },
    { day: "Mar 13", value: 50, events: 5 },
    { day: "Mar 16", value: 85, events: 10 }, /* Peak */
    { day: "Mar 19", value: 70, events: 8 },
    { day: "Mar 22", value: 90, events: 12 },
    { day: "Mar 25", value: 110, events: 15 },
];

export default function TrendsPage() {
    const [hoveredNode, setHoveredNode] = useState<number | null>(null);

    // Simple normalization for much larger SVG space (prevents distortion)
    const maxVal = Math.max(...DATA_POINTS.map(d => d.value));
    const svgHeight = 400;
    const dataRange = 360; // Leave 40 units for padding

    const pointsString = DATA_POINTS.map((d, i) => {
        const x = (i / (DATA_POINTS.length - 1)) * 1000;
        const y = svgHeight - (d.value / maxVal) * dataRange;
        return `${x},${y}`;
    }).join(" ");

    const bgPointsString = `0,${svgHeight} ${pointsString} 1000,${svgHeight}`;

    return (
        <div className="max-w-6xl mx-auto pb-10" style={{ fontFamily: "var(--font-inter), sans-serif" }}>

            {/* ── HEADER ── */}
            <div className="flex flex-col md:flex-row items-end justify-between mb-10 gap-4">
                <div>
                    <div className="flex items-center gap-3 mb-2">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
                            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" /></svg>
                        </div>
                        <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Market Momentum</h1>
                    </div>
                    <p className="text-[15px] font-medium text-slate-500 ml-13">Visualize competitor activity volume and structural changes over time.</p>
                </div>

                {/* Toggle Range */}
                <div className="bg-white border border-slate-200 p-1 rounded-xl flex shadow-sm">
                    <button className="px-5 py-2 text-[13px] font-bold bg-slate-900 text-white rounded-lg shadow-md transition-all">Last 30 Days</button>
                    <button className="px-5 py-2 text-[13px] font-bold text-slate-500 hover:text-slate-900 rounded-lg transition-all hover:bg-slate-50">Quarter</button>
                    <button className="px-5 py-2 text-[13px] font-bold text-slate-500 hover:text-slate-900 rounded-lg transition-all hover:bg-slate-50">Year</button>
                </div>
            </div>

            {/* ── METRICS ROW ── */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm relative overflow-hidden group">
                    <div className="absolute right-0 top-0 w-32 h-32 bg-violet-500/10 rounded-full blur-3xl group-hover:bg-violet-500/20 transition-all"></div>
                    <div className="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-2 flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-violet-500 shadow-[0_0_8px_rgba(139,92,246,0.5)]"></span>
                        Total Volatility
                    </div>
                    <div className="text-4xl font-black text-slate-900 tracking-tight mb-2">High</div>
                    <div className="text-[13px] text-violet-600 font-semibold flex items-center gap-1.5">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" /></svg>
                        +24% vs Last Month
                    </div>
                </div>

                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm relative overflow-hidden group">
                    <div className="absolute right-0 top-0 w-32 h-32 bg-orange-500/10 rounded-full blur-3xl group-hover:bg-orange-500/20 transition-all"></div>
                    <div className="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-2">Primary Catalyst</div>
                    <div className="text-2xl font-bold text-slate-900 mb-1">Pricing Updates</div>
                    <div className="text-[13px] text-orange-600 font-semibold mb-2">3 major shifts detected</div>
                    <div className="text-[11px] font-semibold text-slate-500">Notion, ClickUp, Coda modified tiers</div>
                </div>

                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm relative overflow-hidden group">
                    <div className="absolute right-0 top-0 w-32 h-32 bg-emerald-500/10 rounded-full blur-3xl group-hover:bg-emerald-500/20 transition-all"></div>
                    <div className="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-2">Emerging Competitors</div>
                    <div className="text-4xl font-black text-slate-900 tracking-tight mb-2">+2</div>
                    <div className="text-[13px] font-semibold text-emerald-600 flex items-center gap-1.5">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                        Automatically Discovered
                    </div>
                </div>
            </div>

            {/* ── MAIN GRAPH ── */}
            <div className="bg-white border border-slate-200 rounded-2xl p-8 shadow-sm relative overflow-hidden">

                {/* Fixed HTML Tooltip */}
                {hoveredNode !== null && (
                    <div
                        className="absolute z-30 bg-[#1e293b] text-white p-3 rounded-xl shadow-2xl border border-slate-700 pointer-events-none transition-all duration-200"
                        style={{
                            left: `calc(72px + ${(hoveredNode / (DATA_POINTS.length - 1)) * 100}% )`,
                            top: `${(svgHeight - (DATA_POINTS[hoveredNode].value / maxVal) * dataRange) / svgHeight * 260 - 24}px`,
                            transform: 'translateX(-50%)'
                        }}
                    >
                        <div className="text-[10px] font-bold text-slate-400 uppercase mb-1">{DATA_POINTS[hoveredNode].day}</div>
                        <div className="text-xs font-bold whitespace-nowrap">{DATA_POINTS[hoveredNode].value} Updates ({DATA_POINTS[hoveredNode].events} events)</div>
                    </div>
                )}

                <div className="flex items-center justify-between border-b border-slate-100 pb-6 mb-6">
                    <h3 className="font-bold text-slate-900 text-lg">Product Changes Over Time</h3>
                    <div className="flex items-center gap-6">
                        <div className="flex items-center gap-2">
                            <span className="w-3 h-3 rounded-md bg-blue-500"></span>
                            <span className="text-[13px] font-bold text-slate-500">Total Updates</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <span className="w-3 h-3 rounded-md bg-orange-400"></span>
                            <span className="text-[13px] font-bold text-slate-500">Pricing Alterations</span>
                        </div>
                        <button className="ml-4 p-2 rounded-lg bg-slate-50 hover:bg-slate-100 text-slate-400 transition-colors">
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" /></svg>
                        </button>
                    </div>
                </div>

                {/* Chart Area */}
                <div className="relative w-full h-[260px] pl-10 pb-8 mt-4">

                    {/* Y Axis Grid */}
                    <div className="absolute left-[40px] right-0 top-0 bottom-8 flex flex-col justify-between z-0">
                        {[100, 75, 50, 25, 0].map((val) => (
                            <div key={val} className="w-full relative">
                                <span className="absolute -left-10 -top-2 text-[11px] font-bold text-slate-400 font-mono w-8 text-right">{val}</span>
                                <div className="w-full border-t-[1.5px] border-dashed border-slate-100 h-0"></div>
                            </div>
                        ))}
                    </div>

                    {/* SVG Canvas (Non-distorted coordinates) */}
                    <svg className="absolute inset-0 w-full h-full pb-8 pl-[40px] z-10 overflow-visible" preserveAspectRatio="none" viewBox="0 0 1000 400">
                        {/* Defs / Gradients */}
                        <defs>
                            <linearGradient id="chartG" x1="0" x2="0" y1="0" y2="1">
                                <stop offset="0%" stopColor="#3b82f6" stopOpacity="0.4" />
                                <stop offset="100%" stopColor="#3b82f6" stopOpacity="0.0" />
                            </linearGradient>
                            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                                <feGaussianBlur stdDeviation="3" result="blur" />
                                <feComposite in="SourceGraphic" in2="blur" operator="over" />
                            </filter>
                        </defs>

                        {/* Area Fill */}
                        <polygon points={bgPointsString} fill="url(#chartG)" />

                        {/* Main Line */}
                        <polyline
                            points={pointsString}
                            fill="none"
                            stroke="#3b82f6"
                            strokeWidth="4"
                            strokeLinejoin="round"
                            strokeLinecap="round"
                            filter="url(#glow)"
                        />

                        {/* Interactive Data Nodes */}
                        {DATA_POINTS.map((d, i) => {
                            const x = (i / (DATA_POINTS.length - 1)) * 1000;
                            const y = svgHeight - (d.value / maxVal) * dataRange;
                            const isHovered = hoveredNode === i;

                            return (
                                <g
                                    key={i}
                                    onMouseEnter={() => setHoveredNode(i)}
                                    onMouseLeave={() => setHoveredNode(null)}
                                    className="cursor-crosshair"
                                >
                                    {/* Transparent rect for larger hover area */}
                                    <rect x={x - 40} y="0" width="80" height={svgHeight} fill="transparent" />
                                    <circle
                                        cx={x} cy={y} r={isHovered ? "8" : "4"}
                                        fill="#ffffff"
                                        stroke={isHovered ? "#1d4ed8" : "#3b82f6"}
                                        strokeWidth={isHovered ? "4" : "3"}
                                        className="transition-all duration-300"
                                    />
                                    {/* Vertical Guide line */}
                                    {isHovered && (
                                        <line x1={x} y1="0" x2={x} y2={svgHeight} stroke="#cbd5e1" strokeWidth="1" strokeDasharray="3 3" />
                                    )}
                                </g>
                            );
                        })}
                    </svg>

                    {/* X Axis Labels */}
                    <div className="absolute bottom-0 left-[40px] right-0 flex justify-between text-[11px] font-bold text-slate-400 font-mono">
                        {DATA_POINTS.map(d => (
                            <span key={d.day} className="-translate-x-1/2">{d.day}</span>
                        ))}
                    </div>
                </div>

            </div>

        </div>
    );
}
