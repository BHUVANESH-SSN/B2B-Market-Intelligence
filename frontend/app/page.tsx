"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { MouseEvent as ReactMouseEvent, useEffect, useRef, useState } from "react";

export default function Home() {
  const router = useRouter();
  const [isHoveringButton, setIsHoveringButton] = useState(false);
  const cursorRef = useRef<HTMLDivElement>(null);
  const cursorRingRef = useRef<HTMLDivElement>(null);
  const bgCanvasRef = useRef<HTMLCanvasElement>(null);
  const ptCanvasRef = useRef<HTMLCanvasElement>(null);

  // Parallax elements
  const hcRef = useRef<HTMLDivElement>(null);
  const orbLeftRef = useRef<HTMLDivElement>(null);
  const orbRightRef = useRef<HTMLDivElement>(null);
  const cardsRef = useRef<(HTMLDivElement | null)[]>([]);

  // Particles array ref for the burst effect
  const particlesRef = useRef<any[]>([]);

  useEffect(() => {
    // ── CURSOR ──
    const cursor = cursorRef.current;
    const ring = cursorRingRef.current;
    if (!cursor || !ring) return;

    let mx = window.innerWidth / 2, my = window.innerHeight / 2, rx = mx, ry = my;

    const handleMouseMove = (e: MouseEvent) => {
      mx = e.clientX;
      my = e.clientY;
      if (cursor) {
        cursor.style.left = mx + 'px';
        cursor.style.top = my + 'px';
      }

      // Parallax calculations
      const cx = window.innerWidth / 2, cy = window.innerHeight / 2;
      const dx = (e.clientX - cx) / cx, dy = (e.clientY - cy) / cy;

      if (orbLeftRef.current) orbLeftRef.current.style.transform = `translate(${dx * 25}px,${dy * 20}px)`;
      if (orbRightRef.current) orbRightRef.current.style.transform = `translate(${dx * -25}px,${dy * -20}px)`;
      if (hcRef.current) hcRef.current.style.transform = `translate(${dx * 8}px,${dy * 6}px)`;

      cardsRef.current.forEach(card => {
        if (!card) return;
        const spd = parseFloat(card.dataset.speed || "0.05");
        card.style.transform = `translate(${dx * spd * 200}px,${dy * spd * 200}px)`;
      });
    };

    let ringAnimId: number;
    function animRing() {
      rx += (mx - rx) * 0.15;
      ry += (my - ry) * 0.15;
      if (ring) {
        ring.style.left = rx + 'px';
        ring.style.top = ry + 'px';
      }
      ringAnimId = requestAnimationFrame(animRing);
    }

    document.addEventListener('mousemove', handleMouseMove);
    animRing();

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      cancelAnimationFrame(ringAnimId);
    };
  }, []);

  // ── BACKGROUND PARTICLES (STARS) ──
  useEffect(() => {
    const bgC = bgCanvasRef.current;
    if (!bgC) return;
    const bgCtx = bgC.getContext('2d');
    if (!bgCtx) return;

    bgC.width = window.innerWidth;
    bgC.height = window.innerHeight;

    const stars = Array.from({ length: 120 }, () => ({
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      r: Math.random() * 1.2 + 0.2,
      o: Math.random() * 0.5 + 0.1,
      vy: -(Math.random() * 0.15 + 0.05)
    }));

    let animId: number;
    function drawBg() {
      if (!bgCtx || !bgC) return;
      bgCtx.clearRect(0, 0, bgC.width, bgC.height);
      stars.forEach(s => {
        bgCtx.beginPath();
        bgCtx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        bgCtx.fillStyle = `rgba(200,180,255,${s.o})`;
        bgCtx.fill();
        s.y += s.vy;
        if (s.y < 0) {
          s.y = bgC.height;
          s.x = Math.random() * bgC.width;
        }
      });
      animId = requestAnimationFrame(drawBg);
    }
    drawBg();

    const handleResize = () => {
      if (bgC) { bgC.width = window.innerWidth; bgC.height = window.innerHeight; }
      if (ptCanvasRef.current) { ptCanvasRef.current.width = window.innerWidth; ptCanvasRef.current.height = window.innerHeight; }
    };
    window.addEventListener('resize', handleResize);

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  // ── PARTICLE BURST ENGINE ──
  useEffect(() => {
    const ptC = ptCanvasRef.current;
    if (!ptC) return;
    const ptCtx = ptC.getContext('2d');
    if (!ptCtx) return;

    ptC.width = window.innerWidth;
    ptC.height = window.innerHeight;

    let animId: number;
    function drawParticles() {
      if (!ptCtx || !ptC) return;
      ptCtx.clearRect(0, 0, ptC.width, ptC.height);
      particlesRef.current = particlesRef.current.filter(p => p.life > 0);
      particlesRef.current.forEach(p => {
        ptCtx.beginPath();
        ptCtx.arc(p.x, p.y, p.r * p.life, 0, Math.PI * 2);
        ptCtx.fillStyle = p.color;
        ptCtx.globalAlpha = p.life;
        ptCtx.fill();
        ptCtx.globalAlpha = 1;
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.12;
        p.life -= 0.03;
      });
      animId = requestAnimationFrame(drawParticles);
    }
    drawParticles();

    return () => cancelAnimationFrame(animId);
  }, []);

  const triggerParticles = (e: ReactMouseEvent<HTMLElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;

    for (let i = 0; i < 18; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = Math.random() * 5 + 2;
      const colorType = Math.random() > 0.5 ? '124,58,237' : '251,146,60'; // violet or coral
      particlesRef.current.push({
        x: cx,
        y: cy,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        life: 1,
        color: `rgba(${colorType}, 1)`,
        r: Math.random() * 3 + 1
      });
    }
  };

  // ── REVEAL ON SCROLL ──
  useEffect(() => {
    const revEls = document.querySelectorAll('.reveal');
    const obs = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
        }
      });
    }, { threshold: 0.15 });

    revEls.forEach(el => obs.observe(el));
    return () => obs.disconnect();
  }, []);

  const [btnText, setBtnText] = useState('Get Early Access →');
  const [btnStyle, setBtnStyle] = useState({});

  const handleHeroSubmit = (e: ReactMouseEvent<HTMLButtonElement>) => {
    triggerParticles(e);
    const email = (document.getElementById('hero-email') as HTMLInputElement)?.value;
    if (email) {
      setBtnText("✓ You're on the list!");
      setBtnStyle({ background: 'linear-gradient(135deg,#16a34a,#0f6e56)' });
      setTimeout(() => {
        setBtnText('Get Early Access →');
        setBtnStyle({});
      }, 3000);
    }
  };

  return (
    <>
      <div id="cursor" ref={cursorRef}></div>
      <div id="cursor-ring" ref={cursorRingRef}></div>

      {/* BACKGROUND */}
      <canvas id="bg-canvas" ref={bgCanvasRef}></canvas>
      <canvas id="particle-canvas" ref={ptCanvasRef}></canvas>
      <div className="grid-floor" id="grid-floor"></div>
      <div className="orb orb-left" id="orb-left" ref={orbLeftRef}></div>
      <div className="orb orb-right" id="orb-right" ref={orbRightRef}></div>
      <div className="orb orb-top"></div>
      <div className="streak"></div>

      {/* WIREFRAME OCTAHEDRON */}
      <div className="octa-wrap">
        <div className="octa">
          <div className="octa-face"></div><div className="octa-face"></div>
          <div className="octa-face"></div><div className="octa-face"></div>
        </div>
      </div>

      {/* FLOATING AUTH BUTTONS */}
      <div style={{ position: 'fixed', top: '24px', right: '48px', zIndex: 100, display: 'flex', gap: '24px', alignItems: 'center' }}>
        <Link href="#" style={{ fontSize: '13px', color: 'var(--muted)', textDecoration: 'none', fontWeight: 500, letterSpacing: '0.04em' }}>Sign In</Link>
        <Link href="/onboarding" className="btn-primary" style={{ padding: '10px 24px', borderRadius: '99px', fontSize: '13px' }}>Sign Up</Link>
      </div>

      {/* HERO */}
      <section className="hero" id="hero">

        {/* Floating Persona Cards */}
        <div className="persona-card c1 parallax-fast" data-speed="0.06" ref={el => { cardsRef.current[0] = el }}>
          <div className="persona-top">
            <div className="persona-avatar" style={{ background: 'rgba(124,58,237,0.15)', color: '#a78bfa' }}>SR</div>
            <div>
              <div className="persona-name">Sarah Ren</div>
              <div className="persona-role">VP Marketing · Clearbit</div>
            </div>
          </div>
          <div className="persona-alert">
            <div className="persona-alert-text">
              Hero changed to "AI-native data"
              <div className="badge-detected">DETECTED</div>
            </div>
          </div>
          <div className="persona-time">2h ago</div>
        </div>

        <div className="persona-card c2 parallax-fast" data-speed="0.055" ref={el => { cardsRef.current[1] = el }}>
          <div className="persona-top">
            <div className="persona-avatar" style={{ background: 'rgba(251,146,60,0.12)', color: '#fb923c' }}>MC</div>
            <div>
              <div className="persona-name">Marcus Chen</div>
              <div className="persona-role">Growth Lead · Apollo.io</div>
            </div>
          </div>
          <div className="persona-alert">
            <div className="persona-alert-text">
              Pricing page removed free tier
              <div className="badge-detected">CHANGE</div>
            </div>
          </div>
          <div className="persona-time">5h ago</div>
        </div>

        <div className="persona-card c3 parallax-fast" data-speed="0.07" ref={el => { cardsRef.current[2] = el }}>
          <div className="persona-top">
            <div className="persona-avatar" style={{ background: 'rgba(68,138,255,0.12)', color: '#448aff' }}>JR</div>
            <div>
              <div className="persona-name">James Rowan</div>
              <div className="persona-role">RevOps · ZoomInfo</div>
            </div>
          </div>
          <div className="persona-alert">
            <div className="persona-alert-text">
              SOC 2 badge added above CTA
              <div className="badge-detected badge-live">LIVE</div>
            </div>
          </div>
          <div className="persona-time">1d ago</div>
        </div>

        <div className="persona-card c4 parallax-fast" data-speed="0.05" ref={el => { cardsRef.current[3] = el }}>
          <div className="persona-top">
            <div className="persona-avatar" style={{ background: 'rgba(74,222,128,0.1)', color: '#4ade80' }}>EW</div>
            <div>
              <div className="persona-name">Emily Watson</div>
              <div className="persona-role">PMM · HubSpot</div>
            </div>
          </div>
          <div className="persona-alert">
            <div className="persona-alert-text">
              New SMB segment page launched
              <div className="badge-detected">NEW</div>
            </div>
          </div>
          <div className="persona-time">2d ago</div>
        </div>

        {/* Main Hero Content */}
        <div className="parallax-slow" data-speed="0.02" id="hero-content" ref={hcRef}>
          <div className="hero-eyebrow">Market Intelligence Engine</div>
          <h1 className="hero-h1" style={{ fontSize: "clamp(80px, 15vw, 180px)", marginBottom: "0" }}>
            <span className="line3">ORCHESTAI</span>
          </h1>
          <h2 style={{
            fontFamily: "var(--font-bebas-neue), 'Bebas Neue', sans-serif",
            fontSize: "clamp(28px, 4vw, 46px)",
            letterSpacing: "0.04em",
            lineHeight: "1.1",
            color: "var(--white)",
            marginBottom: "16px",
            marginTop: "16px",
            animation: "fadeUp 0.8s ease 0.6s both"
          }}>
            KNOW EVERY MOVE YOUR COMPETITORS MAKE<br />BEFORE THEY MAKE IT
          </h2>
          <p className="hero-sub">OrchestAI crawls competitor landing pages, detects pricing shifts, tracks messaging changes, and surfaces strategic whitespace — powered by AI agents running 24/7.</p>
          <div className="hero-cta-row">
            <div className="input-wrap">
              <input className="hero-input" type="email" placeholder="you@company.com" id="hero-email" />
            </div>
            <button className="btn-primary" id="hero-btn" style={btnStyle} onClick={handleHeroSubmit}>{btnText}</button>
          </div>
          <div className="hero-tracked">
            Tracking <span>Clearbit</span> · <span>ZoomInfo</span> · <span>Apollo</span> · <span>HubSpot</span> · <span>Cognism</span>
          </div>
        </div>
      </section>

      {/* LOGOS */}
      <div className="logos-strip">
        <span className="logos-label">Tracks competitors across</span>
        <span className="logo-item">G2</span>
        <span className="logo-item">TRUSTPILOT</span>
        <span className="logo-item">GARTNER</span>
        <span className="logo-item">PRODUCT HUNT</span>
        <span className="logo-item">REDDIT</span>
        <span className="logo-item">LINKEDIN</span>
      </div>

      {/* HOW IT WORKS */}
      <section className="section" id="how">
        <div className="reveal">
          <div className="section-tag">How it works</div>
          <h2 className="section-h2">INTELLIGENCE<br />ON AUTOPILOT</h2>
          <p className="section-sub">Four AI agents work in sequence — crawling, diffing, analyzing, and recommending — so your team focuses on strategy, not surveillance.</p>
        </div>
        <div className="how-grid">
          <div className="how-card reveal">
            <div className="edge-glow"></div>
            <div className="how-num">01</div>
            <div className="how-icon">
              <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" /></svg>
            </div>
            <div className="how-title">Crawl Agent</div>
            <div className="how-desc">Continuously scrapes landing pages, pricing pages, review platforms, and ad libraries. Stores timestamped HTML snapshots for every competitor.</div>
          </div>
          <div className="how-card reveal" style={{ transitionDelay: '0.1s' }}>
            <div className="edge-glow"></div>
            <div className="how-num">02</div>
            <div className="how-icon">
              <svg viewBox="0 0 24 24"><path d="M9 3H5a2 2 0 0 0-2 2v4m6-6h10a2 2 0 0 1 2 2v4M9 3v18m0 0h10a2 2 0 0 0 2-2V9M9 21H5a2 2 0 0 1-2-2V9m0 0h18" /></svg>
            </div>
            <div className="how-title">Diff Engine</div>
            <div className="how-desc">Semantic diff between snapshots filters out nav noise and detects real changes — new claims, revised headlines, added CTAs, removed pricing tiers.</div>
          </div>
          <div className="how-card reveal" style={{ transitionDelay: '0.2s' }}>
            <div className="edge-glow"></div>
            <div className="how-num">03</div>
            <div className="how-icon">
              <svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" /></svg>
            </div>
            <div className="how-title">Analyst Agent</div>
            <div className="how-desc">Claude-powered analyst scores each insight for novelty, frequency, and relevance. Every claim is traced back to a source URL and timestamp.</div>
          </div>
        </div>
      </section>

      {/* DASHBOARD PREVIEW */}
      <section className="preview-section reveal">
        <div className="preview-label">Live intelligence feed</div>
        <div className="preview-screen">
          <div className="screen-bar">
            <div className="screen-dot" style={{ background: '#ff5f57' }}></div>
            <div className="screen-dot" style={{ background: '#ffbd2e' }}></div>
            <div className="screen-dot" style={{ background: '#28c840' }}></div>
            <div className="screen-url">app.orchestai.com/dashboard</div>
          </div>
          <div className="dash-metrics">
            <div className="dash-metric"><div className="dm-label">Competitors tracked</div><div className="dm-val" style={{ color: '#a78bfa' }}>8</div><div className="dm-sub">+2 this week</div></div>
            <div className="dash-metric"><div className="dm-label">Changes detected</div><div className="dm-val" style={{ color: '#fb923c' }}>24</div><div className="dm-sub">↑ 6 since yesterday</div></div>
            <div className="dash-metric"><div className="dm-label">New claims</div><div className="dm-val" style={{ color: '#448aff' }}>11</div><div className="dm-sub">↑ 3 today</div></div>
            <div className="dash-metric"><div className="dm-label">Whitespace gaps</div><div className="dm-val" style={{ color: '#4ade80' }}>5</div><div className="dm-sub">High opportunity</div></div>
          </div>
          <div className="dash-row">
            <div className="dash-card">
              <div className="dc-title">Top strategic insights</div>
              <div className="insight-mini"><div className="im-dot" style={{ background: '#e24b4a' }}></div><div className="im-text">"AI-native" used by 5 of 8 competitors — angle saturating</div></div>
              <div className="insight-mini"><div className="im-dot" style={{ background: '#ef9f27' }}></div><div className="im-text">3 competitors removed pricing transparency — quote-only shift</div></div>
              <div className="insight-mini"><div className="im-dot" style={{ background: '#4ade80' }}></div><div className="im-text">No competitor targets RevOps teams — whitespace open</div></div>
            </div>
            <div className="dash-card">
              <div className="dc-title">Recent competitor changes</div>
              <div className="comp-mini"><div className="cm-av" style={{ background: 'rgba(124,58,237,0.15)', color: '#a78bfa' }}>CL</div><div className="cm-name">Clearbit</div><div className="cm-badge" style={{ background: 'rgba(251,146,60,0.1)', color: '#fb923c', fontSize: '9px' }}>Pricing</div></div>
              <div className="comp-mini"><div className="cm-av" style={{ background: 'rgba(68,138,255,0.12)', color: '#448aff' }}>ZI</div><div className="cm-name">ZoomInfo</div><div className="cm-badge" style={{ background: 'rgba(68,138,255,0.1)', color: '#448aff', fontSize: '9px' }}>Messaging</div></div>
              <div className="comp-mini"><div className="cm-av" style={{ background: 'rgba(74,222,128,0.1)', color: '#4ade80' }}>AP</div><div className="cm-name">Apollo.io</div><div className="cm-badge" style={{ background: 'rgba(74,222,128,0.1)', color: '#4ade80', fontSize: '9px' }}>Trust</div></div>
            </div>
          </div>
        </div>
      </section>

      {/* WHITESPACE SECTION */}
      <section className="whitespace-section">
        <div className="reveal">
          <div className="section-tag">Whitespace Detection</div>
          <h2 className="section-h2">FIND THE GAPS<br />NO ONE OWNS</h2>
          <p className="section-sub">OrchestAI scores uncontested positioning gaps so your team knows exactly where to plant your flag before competitors do.</p>
        </div>
        <div className="ws-gaps reveal">
          <div className="ws-gap-item"><span className="ws-gap-text">Operations & RevOps targeting</span><div className="ws-bar-wrap"><div className="ws-bar" style={{ width: '96%' }}></div></div><span className="ws-score">96</span></div>
          <div className="ws-gap-item"><span className="ws-gap-text">Transparent ROI with benchmarks</span><div className="ws-bar-wrap"><div className="ws-bar" style={{ width: '84%' }}></div></div><span className="ws-score">84</span></div>
          <div className="ws-gap-item"><span className="ws-gap-text">SMB self-serve onboarding</span><div className="ws-bar-wrap"><div className="ws-bar" style={{ width: '79%' }}></div></div><span className="ws-score">79</span></div>
          <div className="ws-gap-item"><span className="ws-gap-text">Industry-specific landing pages</span><div className="ws-bar-wrap"><div className="ws-bar" style={{ width: '71%' }}></div></div><span className="ws-score">71</span></div>
          <div className="ws-gap-item"><span className="ws-gap-text">Community-led growth signals</span><div className="ws-bar-wrap"><div className="ws-bar" style={{ width: '65%' }}></div></div><span className="ws-score">65</span></div>
        </div>
      </section>

      {/* FOOTER */}
      <footer>
        <div className="footer-logo">ORCHEST<span>AI</span></div>
        <div className="footer-copy">© 2025 OrchestAI · Market Intelligence Engine · Built for Track 2</div>
        <div className="footer-glow"></div>
      </footer>
    </>
  );
}
