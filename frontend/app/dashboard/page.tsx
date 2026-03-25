"use client";


export default function Dashboard() {
    return (
        <div className="w-full h-full flex flex-col items-center justify-center p-10 animate-[fadeUp_0.8s_ease_both]">
            <div className="w-16 h-16 bg-slate-100 rounded-2xl flex items-center justify-center mb-6 shadow-inner ring-1 ring-slate-200">
                <svg className="w-8 h-8 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            </div>
            <h1 className="text-2xl font-bold text-slate-800 font-['Inter'] tracking-tight mb-2">Welcome to OrchestAI</h1>
            <p className="text-slate-500 text-[15px] font-medium max-w-sm text-center font-['Inter']">Select an option from the sidebar to add a company or begin tracking competitor signals.</p>
        </div>
    );
}
