"use client";

import { useState } from "react";

export default function Onboarding() {
    const [step, setStep] = useState(1);
    const [companyUrl, setCompanyUrl] = useState("");
    const [competitors, setCompetitors] = useState(["", "", ""]);

    const updateCompetitor = (index: number, value: string) => {
        const newComps = [...competitors];
        newComps[index] = value;
        setCompetitors(newComps);
    };

    return (
        <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-6 relative overflow-hidden">

            {/* Background Decor */}
            <div className="absolute top-[-20%] left-[-10%] w-[600px] h-[600px] bg-violet-400/20 blur-[120px] rounded-full pointer-events-none"></div>
            <div className="absolute bottom-[-20%] right-[-10%] w-[600px] h-[600px] bg-orange-400/15 blur-[120px] rounded-full pointer-events-none"></div>

            <div className="w-full max-w-xl bg-white/80 backdrop-blur-2xl border border-slate-200/60 shadow-2xl rounded-3xl p-10 z-10 animate-[fadeUp_0.6s_ease_out]">

                {/* Header */}
                <div className="mb-10 text-center">
                    <div className="w-16 h-16 bg-gradient-to-br from-violet-600 to-orange-400 rounded-2xl mx-auto flex items-center justify-center text-white text-2xl font-bold font-['Bebas_Neue'] shadow-xl shadow-violet-500/20 mb-6">O</div>
                    <h1 className="text-2xl font-bold text-slate-900 font-['Inter'] tracking-tight">
                        {step === 1 ? "Let's calibrate your engine." : "Who are we tracking?"}
                    </h1>
                    <p className="text-slate-500 mt-2 text-[15px]">
                        {step === 1
                            ? "First, tell OrchestAI where your company lives so we know your baseline."
                            : "Provide URLs for the top competitors you want our crawl agents to monitor 24/7."}
                    </p>
                </div>

                {/* Step 1: Own Company URL */}
                {step === 1 && (
                    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <div>
                            <label className="block text-[13px] font-bold text-slate-700 uppercase tracking-widest mb-3">Your Product URL</label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                    <svg className="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"></path></svg>
                                </div>
                                <input
                                    type="url"
                                    value={companyUrl}
                                    onChange={(e) => setCompanyUrl(e.target.value)}
                                    className="w-full pl-12 pr-4 py-4 bg-slate-50 border border-slate-200 rounded-xl text-[15px] font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500 transition-all shadow-sm"
                                    placeholder="https://acme.com"
                                />
                            </div>
                            <p className="text-[12px] text-slate-400 mt-3 flex items-center gap-1.5">
                                <svg className="w-3.5 h-3.5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                We use this to analyze your whitespace vs competitors.
                            </p>
                        </div>
                        <button
                            onClick={() => setStep(2)}
                            disabled={!companyUrl}
                            className="w-full py-4 mt-4 bg-gradient-to-r from-violet-600 to-orange-500 text-white rounded-xl font-bold text-[15px] shadow-lg shadow-violet-500/25 hover:shadow-xl hover:shadow-violet-500/40 hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:pointer-events-none"
                        >
                            Continue →
                        </button>
                    </div>
                )}

                {/* Step 2: Competitor URLs */}
                {step === 2 && (
                    <div className="space-y-5 animate-in fade-in slide-in-from-right-8 duration-500">
                        <div>
                            <label className="block text-[13px] font-bold text-slate-700 uppercase tracking-widest mb-4 flex items-center gap-2">
                                Competitor URLs
                                <span className="bg-slate-100 text-slate-500 px-2 py-0.5 rounded text-[10px] normal-case tracking-normal border border-slate-200">Start with up to 3</span>
                            </label>

                            <div className="space-y-3">
                                {competitors.map((comp, index) => (
                                    <div key={index} className="relative flex items-center group">
                                        <div className="absolute left-4 text-slate-300 font-mono text-[11px] font-bold">{index + 1}</div>
                                        <input
                                            type="url"
                                            value={comp}
                                            onChange={(e) => updateCompetitor(index, e.target.value)}
                                            className="w-full pl-10 pr-4 py-3.5 bg-slate-50 border border-slate-200 rounded-xl text-[14px] font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500 transition-all group-hover:border-slate-300"
                                            placeholder={`e.g. https://competitor-${index + 1}.com`}
                                        />
                                    </div>
                                ))}
                            </div>

                            <p className="text-[12px] text-slate-400 mt-4 flex items-start gap-1.5 leading-relaxed">
                                <svg className="w-4 h-4 text-violet-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                                URLs are strictly required. Company names can be ambiguous ("Apple" vs "Apple Records"), but URLs guarantee our Crawl Agents strike the exact target.
                            </p>
                        </div>

                        <div className="flex gap-3 mt-4 pt-4 border-t border-slate-100">
                            <button
                                onClick={() => setStep(1)}
                                className="px-6 py-4 bg-white border border-slate-200 text-slate-600 rounded-xl font-semibold text-[14px] hover:bg-slate-50 transition-colors"
                            >
                                Back
                            </button>
                            <button
                                className="flex-1 py-4 bg-slate-900 text-white rounded-xl font-bold text-[15px] shadow-lg shadow-slate-900/20 hover:shadow-xl hover:-translate-y-0.5 transition-all text-center flex items-center justify-center gap-2"
                                onClick={() => window.location.href = '/dashboard'}
                            >
                                Deploy Crawl Agents
                                <svg className="w-4 h-4 text-violet-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                            </button>
                        </div>
                    </div>
                )}

            </div>

            <div className="mt-8 flex items-center gap-2 text-[12px] text-slate-400 font-mono tracking-widest uppercase">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> System Secure
            </div>
        </div>
    );
}
