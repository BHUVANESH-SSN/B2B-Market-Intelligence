"use client";

import Link from "next/link";
import { SignIn, SignOutButton, useAuth } from "@clerk/nextjs";
import { useEffect, useRef } from "react";

export default function LoginPage() {
  const { isSignedIn } = useAuth();
  const cursorRef = useRef<HTMLDivElement>(null);
  const cursorRingRef = useRef<HTMLDivElement>(null);
  const bgCanvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const cursor = cursorRef.current;
    const ring = cursorRingRef.current;
    if (!cursor || !ring) {
      return;
    }

    let mx = window.innerWidth / 2;
    let my = window.innerHeight / 2;
    let rx = mx;
    let ry = my;

    const handleMouseMove = (event: MouseEvent) => {
      mx = event.clientX;
      my = event.clientY;
      cursor.style.left = `${mx}px`;
      cursor.style.top = `${my}px`;
    };

    let ringAnimId = 0;
    const animateRing = () => {
      rx += (mx - rx) * 0.15;
      ry += (my - ry) * 0.15;
      ring.style.left = `${rx}px`;
      ring.style.top = `${ry}px`;
      ringAnimId = requestAnimationFrame(animateRing);
    };

    document.addEventListener("mousemove", handleMouseMove);
    animateRing();

    return () => {
      document.removeEventListener("mousemove", handleMouseMove);
      cancelAnimationFrame(ringAnimId);
    };
  }, []);

  useEffect(() => {
    const canvas = bgCanvasRef.current;
    if (!canvas) {
      return;
    }

    const ctx = canvas.getContext("2d");
    if (!ctx) {
      return;
    }

    const setCanvasSize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    setCanvasSize();

    const stars = Array.from({ length: 120 }, () => ({
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      r: Math.random() * 1.2 + 0.2,
      o: Math.random() * 0.5 + 0.1,
      vy: -(Math.random() * 0.15 + 0.05),
    }));

    let animId = 0;
    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      stars.forEach((star) => {
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(200,180,255,${star.o})`;
        ctx.fill();
        star.y += star.vy;
        if (star.y < 0) {
          star.y = canvas.height;
          star.x = Math.random() * canvas.width;
        }
      });
      animId = requestAnimationFrame(draw);
    };

    draw();
    window.addEventListener("resize", setCanvasSize);

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", setCanvasSize);
    };
  }, []);

  return (
    <>
      <div id="cursor" ref={cursorRef} />
      <div id="cursor-ring" ref={cursorRingRef} />

      <canvas id="bg-canvas" ref={bgCanvasRef} />
      <div className="grid-floor" />
      <div className="orb orb-left" />
      <div className="orb orb-right" />
      <div className="orb orb-top" />
      <div className="streak" />
      <div className="octa-wrap">
        <div className="octa">
          <div className="octa-face" />
          <div className="octa-face" />
          <div className="octa-face" />
          <div className="octa-face" />
        </div>
      </div>

      <section className="auth-shell relative z-10 flex min-h-screen flex-1 items-center overflow-hidden px-5 py-10 text-slate-900 md:px-8">
        <div className="mx-auto grid w-full max-w-6xl gap-10 md:grid-cols-[1fr_480px] md:items-center">
          <div className="hidden md:block">
            <p className="hero-eyebrow max-w-max">Market Intelligence Engine</p>
            <h1 className="hero-h1">
              <span className="line3">ORCHEST AI</span>
            </h1>
            <h2
              style={{
                fontFamily: "var(--font-bebas-neue), 'Bebas Neue', sans-serif",
                fontSize: "clamp(28px, 4vw, 46px)",
                letterSpacing: "0.04em",
                lineHeight: "1.1",
                color: "var(--white)",
                marginTop: "16px",
              }}
            >
              KNOW EVERY MOVE YOUR COMPETITORS MAKE
            </h2>
            <p className="hero-sub !mx-0 !max-w-xl !text-left">
              Sign in to continue tracking messaging shifts, pricing changes,
              and competitive whitespace from your live intelligence workspace.
            </p>
            <div className="hero-tracked !text-left">
              Tracking <span>Clearbit</span> · <span>ZoomInfo</span> ·{" "}
              <span>Apollo</span> · <span>HubSpot</span>
            </div>
          </div>

          <div className="w-full">
            {isSignedIn ? (
              <div className="w-full rounded-[20px] border border-[rgba(124,58,237,0.14)] bg-white/90 p-6 text-slate-900">
                <h2 className="text-[1.55rem] font-semibold text-slate-900">
                  You are already signed in
                </h2>
                <p className="mt-3 text-sm text-slate-600">
                  Your Clerk session is active. You can return to the main page
                  or sign out and log in with a different account.
                </p>
                <div className="mt-6 flex flex-col gap-3 sm:flex-row">
                  <Link
                    href="/dashboard"
                    className="inline-flex items-center justify-center rounded-xl bg-[linear-gradient(135deg,#7c3aed,#fb923c)] px-4 py-3 font-semibold text-white transition hover:translate-y-[-2px]"
                  >
                    Go to dashboard
                  </Link>
                  <SignOutButton>
                    <button className="cursor-pointer rounded-xl border border-[rgba(124,58,237,0.18)] px-4 py-3 font-semibold text-slate-700 transition hover:bg-[rgba(124,58,237,0.05)]">
                      Sign out
                    </button>
                  </SignOutButton>
                </div>
              </div>
            ) : (
              <SignIn
                path="/login"
                routing="path"
                signUpUrl="/signup"
                fallbackRedirectUrl="/dashboard"
                appearance={{
                  elements: {
                    rootBox: "w-full",
                    card:
                      "w-full rounded-[20px] border border-[rgba(124,58,237,0.14)] bg-white/90 p-6 shadow-none",
                    headerTitle:
                      "text-slate-900 text-[1.55rem] font-semibold",
                    headerSubtitle: "text-slate-600 text-sm",
                    socialButtonsBlockButton:
                      "border border-[rgba(124,58,237,0.16)] bg-white text-slate-900 hover:bg-[rgba(124,58,237,0.04)] shadow-none",
                    socialButtonsBlockButtonText:
                      "text-slate-900 font-medium",
                    dividerLine: "bg-[rgba(124,58,237,0.12)]",
                    dividerText: "text-slate-500",
                    formFieldLabel: "text-slate-700 text-sm",
                    formFieldInput:
                      "h-11 rounded-xl border border-[rgba(124,58,237,0.16)] bg-white text-slate-900 placeholder:text-slate-400 focus:border-violet-500 focus:ring-violet-500",
                    footerActionLink: "text-violet-700 hover:text-violet-600",
                    formButtonPrimary:
                      "h-11 rounded-xl bg-[linear-gradient(135deg,#7c3aed,#fb923c)] text-white font-semibold shadow-none hover:opacity-95",
                    formFieldSuccessText: "text-emerald-500",
                    formFieldErrorText: "text-red-500",
                    identityPreviewText: "text-slate-600",
                    identityPreviewEditButton:
                      "text-violet-700 hover:text-violet-600",
                    otpCodeFieldInput:
                      "border border-[rgba(124,58,237,0.16)] bg-white text-slate-900",
                  },
                }}
              />
            )}
          </div>
        </div>
      </section>
    </>
  );
}
