"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const pathname = usePathname();

    // Pages that SHOULD HAVE the dashboard layout
    const isAppPage = pathname.startsWith("/dashboard") ||
        pathname === "/competitors" ||
        pathname === "/insights" ||
        pathname === "/trends" ||
        pathname === "/reports" ||
        pathname === "/discover";

    if (!isAppPage) return <>{children}</>;

    const navLinks = [
        { name: "Dashboard", href: "/dashboard" },
        { name: "Competitors", href: "/competitors" },
        { name: "Insights", href: "/insights" },
        { name: "Trends", href: "/trends" },
        { name: "Reports", href: "/reports" },
    ];

    return (
        <div className="w-full h-screen bg-slate-50 relative text-slate-800 cursor-auto" style={{ fontFamily: "var(--font-inter), sans-serif" }}>

            {/* ── TOP NAVBAR ── */}
            <header className="absolute top-0 left-0 right-0 h-16 bg-white border-b border-slate-200 shadow-sm z-50 flex items-center px-6 gap-8">
                {/* Branding Logo */}
                <div className="flex items-center gap-2 mr-2">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-violet-600 to-orange-400 flex items-center justify-center text-white text-xs font-bold shadow-md">O</div>
                    <span className="text-lg font-bold tracking-wider hidden sm:block" style={{ fontFamily: "var(--font-bebas-neue), sans-serif" }}>ORCHESTAI</span>
                </div>

                {/* Nav Links */}
                <nav className="h-full flex items-center gap-8">
                    {navLinks.map((link) => {
                        const isActive = pathname === link.href;
                        return (
                            <Link
                                key={link.href}
                                href={link.href}
                                className={`h-full flex items-center text-sm font-semibold transition-all border-b-2 ${isActive
                                    ? "border-violet-600 text-violet-700"
                                    : "border-transparent text-slate-500 hover:text-slate-900"
                                    }`}
                            >
                                {link.name}
                            </Link>
                        );
                    })}
                </nav>
            </header>

            {/* ── SIDEBAR (Responsive Hover) ── */}
            <aside className="absolute top-16 bottom-0 left-0 w-[76px] hover:w-64 bg-white border-r border-slate-200 z-40 hidden md:flex flex-col overflow-x-hidden transition-all duration-300 group hover:shadow-2xl">

                <div className="flex-1 flex flex-col py-6 w-64">

                    {/* Logo Area */}
                    <div className="flex items-center gap-[18px] px-5 mb-8">
                        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-violet-600 to-orange-400 flex items-center justify-center text-white text-sm font-bold shadow-md shrink-0">O</div>
                        <span className="text-xl font-bold tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap" style={{ fontFamily: "var(--font-bebas-neue), sans-serif" }}>ORCHESTAI</span>
                    </div>

                    {/* ⚡ ACTIONS */}
                    <div className="mb-6 px-3.5">
                        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest font-mono mb-4 px-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap flex items-center">
                            <span className="text-violet-500 text-sm mr-2">⚡</span> Actions
                        </div>

                        {/* Expandable Buttons */}
                        <Link href="/discover" className="mb-3 bg-gradient-to-r from-violet-600 to-blue-600 hover:from-violet-700 hover:to-blue-700 text-white rounded-[14px] p-2.5 font-semibold text-[13px] flex items-center gap-3.5 shadow-md shadow-violet-500/20 transition-all duration-300 overflow-hidden w-[48px] group-hover:w-[228px]">
                            <svg className="w-7 h-7 shrink-0 p-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                            <span className="opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap">Find Competitors</span>
                        </Link>

                        <Link href="/competitors" className="bg-slate-900 hover:bg-slate-800 text-white rounded-[14px] p-2.5 mb-3 font-semibold text-[13px] flex items-center gap-3.5 shadow-md transition-all duration-300 overflow-hidden w-[48px] group-hover:w-[228px]">
                            <div className="w-7 h-7 shrink-0 flex items-center justify-center font-black text-xl">+</div>
                            <span className="opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap">Add Company</span>
                        </Link>

                        <button className="bg-slate-50 border border-slate-200 hover:border-violet-300 hover:bg-violet-50 text-violet-700 rounded-[14px] p-2.5 mb-3 font-semibold text-[13px] flex items-center gap-3.5 shadow-sm transition-all duration-300 overflow-hidden w-[48px] group-hover:w-[228px]">
                            <svg className="w-7 h-7 shrink-0 p-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                            <span className="opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap">Run Analysis</span>
                        </button>
                    </div>

                    {/* 🔍 UTILITY */}
                    <div className="px-3.5">
                        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest font-mono mb-4 px-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap flex items-center">
                            <span className="text-blue-500 text-sm mr-2">🔍</span> Utility
                        </div>

                        <button className="mb-3 bg-slate-50 hover:bg-slate-100 border border-slate-200 text-slate-500 rounded-[14px] p-2.5 font-semibold text-[13px] flex items-center gap-3.5 transition-all duration-300 overflow-hidden w-[48px] group-hover:w-[228px]">
                            <svg className="w-7 h-7 shrink-0 p-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                            <span className="opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap">Search</span>
                        </button>

                        <button className="bg-slate-50 hover:bg-white border border-slate-200 text-slate-700 rounded-[14px] p-2.5 font-semibold text-[13px] flex items-center justify-between transition-all duration-300 overflow-hidden w-[48px] group-hover:w-[228px]">
                            <div className="flex items-center gap-3.5">
                                <div className="relative shrink-0 w-7 h-7 flex items-center justify-center">
                                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
                                    <span className="absolute 1 top-0 right-0 group-hover:hidden w-2.5 h-2.5 bg-orange-500 rounded-full border-2 border-slate-50"></span>
                                </div>
                                <span className="opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap">Notifications</span>
                            </div>
                            <span className="bg-orange-100 text-orange-600 px-2 py-0.5 rounded text-[10px] font-bold opacity-0 group-hover:opacity-100 transition-opacity duration-200 shrink-0">12</span>
                        </button>
                    </div>

                    {/* Profile — absolute to bottom wrapper bounding box */}
                    <div className="absolute bottom-4 left-3.5 w-[48px] group-hover:w-[228px] border border-slate-100 bg-white hover:bg-slate-50 rounded-[16px] flex items-center p-1.5 transition-all duration-300 overflow-hidden shadow-sm cursor-pointer">
                        <div className="w-9 h-9 shrink-0 rounded-[10px] bg-emerald-100 flex items-center justify-center text-emerald-700 font-bold text-sm ring-1 ring-emerald-200">
                            JD
                        </div>
                        <div className="flex flex-col opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap ml-3">
                            <span className="text-[13px] font-bold text-slate-800 leading-none mb-1">John Doe</span>
                            <span className="text-[10px] font-semibold text-slate-500 leading-none">Acme Corp</span>
                        </div>
                    </div>

                </div>
            </aside>

            {/* ── MAIN CONTENT ── */}
            <main className="absolute top-16 bottom-0 right-0 left-0 md:left-[76px] overflow-y-auto bg-slate-50 p-8 z-10 transition-all duration-300 pt-6">
                {children}
            </main>

        </div>
    );
}
