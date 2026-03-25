export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="h-screen w-full bg-slate-50 flex flex-col overflow-hidden">

            {/* ── TOP NAVBAR ── */}
            <header className="shrink-0 h-14 bg-white border-b border-slate-200/80 px-6 flex items-center z-50">
                <div className="flex items-center gap-10 h-full">
                    {/* Logo */}
                    <div className="flex items-center gap-3 text-xl text-slate-800 tracking-wider cursor-pointer" style={{ fontFamily: "var(--font-bebas-neue)" }}>
                        <div className="w-7 h-7 rounded-md bg-gradient-to-br from-violet-600 to-orange-400 flex items-center justify-center text-white text-[13px] font-bold shadow-sm shadow-violet-500/20" style={{ fontFamily: "var(--font-inter)" }}>O</div>
                        ORCHESTAI
                    </div>

                    {/* Main Navigation */}
                    <nav className="hidden md:flex items-center gap-8 text-[13px] font-medium text-slate-500 h-full" style={{ fontFamily: "var(--font-inter)" }}>
                        <a href="#" className="text-violet-700 border-b-2 border-violet-600 h-full flex items-center transition-colors">Dashboard</a>
                        <a href="#" className="hover:text-slate-800 h-full flex items-center transition-colors relative">
                            Competitors
                            <span className="absolute top-[35%] -right-2.5 w-1 h-1 bg-orange-500 rounded-full animate-pulse"></span>
                        </a>
                        <a href="#" className="hover:text-slate-800 h-full flex items-center transition-colors">Insights</a>
                        <a href="#" className="hover:text-slate-800 h-full flex items-center transition-colors">Trends</a>
                        <a href="#" className="hover:text-slate-800 h-full flex items-center transition-colors">Reports</a>
                    </nav>
                </div>
            </header>

            {/* ── LOWER CONTAINER ── */}
            <div className="flex flex-1 overflow-hidden">

                {/* ── SIDEBAR ── */}
                <aside className="w-[280px] bg-white/50 border-r border-slate-200/80 flex flex-col p-6 hidden lg:flex backdrop-blur-md z-40">

                    {/* ⚡ ACTIONS */}
                    <div className="mb-8">
                        <div className="text-[11px] font-bold text-slate-400 uppercase tracking-widest font-mono mb-4 px-1 flex items-center gap-2">
                            <span className="text-violet-500 text-sm">⚡</span> Actions
                        </div>

                        <div className="flex flex-col gap-3">
                            <button className="w-full bg-slate-900 hover:bg-slate-800 text-white rounded-xl py-3.5 font-semibold text-[13px] flex items-center justify-center gap-2 transition-all shadow-md hover:shadow-lg hover:-translate-y-[1px]" style={{ fontFamily: "var(--font-inter)" }}>
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M12 4v16m8-8H4"></path></svg>
                                Add Company
                            </button>

                            <button className="w-full bg-white border border-slate-200 hover:border-violet-300 hover:bg-violet-50 text-violet-700 rounded-xl py-3.5 font-semibold text-[13px] flex items-center justify-center gap-2 transition-all shadow-sm" style={{ fontFamily: "var(--font-inter)" }}>
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                Run Analysis
                            </button>
                        </div>
                    </div>

                    {/* 🔍 UTILITY */}
                    <div className="flex-1 flex flex-col">
                        <div className="text-[11px] font-bold text-slate-400 uppercase tracking-widest font-mono mb-4 px-1 flex items-center gap-2">
                            <span className="text-blue-500 text-sm">🔍</span> Utility
                        </div>

                        <div className="flex flex-col gap-4">
                            {/* Search Input */}
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                                    <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                                </div>
                                <input
                                    type="text"
                                    placeholder="Search intelligence..."
                                    className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-[13px] text-slate-700 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-violet-500/20 focus:border-violet-500 transition-all shadow-sm"
                                    style={{ fontFamily: "var(--font-inter)" }}
                                />
                            </div>

                            {/* Notifications */}
                            <button className="flex items-center justify-between w-full px-4 py-3 bg-white border border-slate-200 rounded-xl hover:border-slate-300 transition-colors shadow-sm group">
                                <div className="flex items-center gap-3 text-[13px] font-medium text-slate-600 group-hover:text-slate-800" style={{ fontFamily: "var(--font-inter)" }}>
                                    <svg className="w-4 h-4 text-slate-400 group-hover:text-violet-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
                                    Notifications
                                </div>
                                <span className="bg-orange-100 text-orange-600 px-2 py-0.5 rounded text-[10px] font-bold">12</span>
                            </button>
                        </div>

                        {/* Profile Section (Pushed to bottom) */}
                        <div className="mt-auto bg-white border border-slate-200 rounded-xl p-3 flex items-center gap-3 cursor-pointer hover:border-violet-300 transition-colors shadow-sm group">
                            <div className="w-9 h-9 rounded-lg bg-emerald-100 flex items-center justify-center text-emerald-700 font-bold text-xs ring-1 ring-emerald-200">
                                JD
                            </div>
                            <div className="flex flex-col">
                                <span className="text-[13px] font-semibold text-slate-800 leading-tight group-hover:text-violet-700 transition-colors" style={{ fontFamily: "var(--font-inter)" }}>John Doe</span>
                                <span className="text-[11px] text-slate-500">Acme Corp</span>
                            </div>
                            <div className="ml-auto text-slate-400 group-hover:text-violet-500">
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"></path></svg>
                            </div>
                        </div>
                    </div>
                </aside>

                {/* ── MAIN CONTENT AREA ── */}
                <main className="flex-1 overflow-y-auto w-full">
                    {children}
                </main>

            </div>
        </div>
    );
}
