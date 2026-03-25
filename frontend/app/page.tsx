import Link from "next/link";
import { Show } from "@clerk/nextjs";

export default function Home() {
  return (
    <section className="flex flex-1 items-center justify-center bg-[linear-gradient(180deg,#fff7ed_0%,#ffffff_45%,#fff1e6_100%)] px-6 py-16">
      <div className="w-full max-w-4xl rounded-[32px] border border-orange-100 bg-white/90 p-10 shadow-[0_30px_80px_rgba(251,146,60,0.18)] backdrop-blur-sm md:p-16">
        <div className="space-y-6">
          <p className="text-sm font-semibold uppercase tracking-[0.35em] text-orange-500">
            B2B Market Intelligence
          </p>
          <h1 className="max-w-2xl text-4xl font-semibold tracking-tight text-slate-950 md:text-6xl">
            Turn fragmented signals into confident business decisions.
          </h1>
          <p className="max-w-xl text-lg leading-8 text-slate-600">
            Clerk authentication is now connected, so your team can move from
            public landing page to secure product flows cleanly.
          </p>
          <div className="flex flex-col gap-4 sm:flex-row">
            <Show when="signed-out">
              <Link
                className="inline-flex rounded-full bg-orange-500 px-6 py-3 font-medium text-white transition hover:bg-orange-600"
                href="/signup"
              >
                Create account
              </Link>
              <Link
                className="inline-flex rounded-full border border-slate-200 px-6 py-3 font-medium text-slate-700 transition hover:bg-slate-50"
                href="/login"
              >
                Sign in
              </Link>
            </Show>
            <Show when="signed-in">
              <Link
                className="inline-flex rounded-full bg-slate-950 px-6 py-3 font-medium text-white transition hover:bg-slate-800"
                href="/login"
              >
                Manage session
              </Link>
            </Show>
          </div>
        </div>
      </div>
    </section>
  );
}
