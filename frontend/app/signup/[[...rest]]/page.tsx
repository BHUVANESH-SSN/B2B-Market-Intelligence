"use client";

import { SignUp } from "@clerk/nextjs";
import { useEffect, useRef } from "react";

interface Particle {
  angle: number;
  radius: number;
  speed: number;
  size: number;
  alpha: number;
  drift: number;
  radiusDrift: number;
  life: number;
  decay: number;
}

export default function SignUpPage() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const mouseRef = useRef({ x: 0, y: 0 });
  const glowRef = useRef({ x: 0, y: 0 });
  const rafRef = useRef<number>(0);

  const handleMouseMove = (event: React.MouseEvent) => {
    mouseRef.current = { x: event.clientX, y: event.clientY };
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) {
      return;
    }

    const ctx = canvas.getContext("2d");
    if (!ctx) {
      return;
    }

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);
    glowRef.current = { x: width / 2, y: height / 2 };
    mouseRef.current = { x: width / 2, y: height / 2 };

    const handleResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };

    window.addEventListener("resize", handleResize);

    const particles: Particle[] = Array.from({ length: 180 }, () => ({
      angle: Math.random() * Math.PI * 2,
      radius: 20 + Math.random() * 220,
      speed: 0.008 + Math.random() * 0.018,
      size: 1.5 + Math.random() * 3.5,
      alpha: 0.3 + Math.random() * 0.7,
      drift: (Math.random() - 0.5) * 0.003,
      radiusDrift: (Math.random() - 0.5) * 0.4,
      life: Math.random(),
      decay: 0.003 + Math.random() * 0.005,
    }));

    const fireColor = (ratio: number): [number, number, number] => {
      return [255, Math.round(255 * Math.pow(1 - ratio, 2.2) * 0.6), 0];
    };

    const draw = () => {
      const glow = glowRef.current;
      const mouse = mouseRef.current;

      glow.x += (mouse.x - glow.x) * 0.07;
      glow.y += (mouse.y - glow.y) * 0.07;

      ctx.clearRect(0, 0, width, height);

      const ambient = ctx.createRadialGradient(
        glow.x,
        glow.y,
        0,
        glow.x,
        glow.y,
        420,
      );
      ambient.addColorStop(0, "rgba(255,120,0,0.18)");
      ambient.addColorStop(0.4, "rgba(255,60,0,0.10)");
      ambient.addColorStop(1, "rgba(255,0,0,0)");
      ctx.fillStyle = ambient;
      ctx.fillRect(0, 0, width, height);

      for (const particle of particles) {
        particle.angle += particle.speed + particle.drift;
        particle.radius += particle.radiusDrift;

        if (particle.radius < 15) {
          particle.radius = 15;
        }

        if (particle.radius > 260) {
          particle.radius = 260;
        }

        particle.life -= particle.decay;
        if (particle.life <= 0) {
          particle.life = 0.6 + Math.random() * 0.4;
          particle.radius = 20 + Math.random() * 100;
          particle.angle = Math.random() * Math.PI * 2;
          particle.speed = 0.008 + Math.random() * 0.018;
          particle.drift = (Math.random() - 0.5) * 0.003;
          particle.radiusDrift = (Math.random() - 0.5) * 0.4;
        }

        const spiralFactor = 1 + particle.radius / 300;
        const x =
          glow.x + Math.cos(particle.angle * spiralFactor) * particle.radius;
        const y =
          glow.y +
          Math.sin(particle.angle * spiralFactor) * particle.radius * 0.9;
        const ratio = particle.radius / 260;
        const [r, g, b] = fireColor(ratio);
        const alpha = particle.alpha * particle.life * (1 - ratio * 0.6);

        ctx.beginPath();
        ctx.arc(x, y, particle.size * (1 - ratio * 0.4), 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${r},${g},${b},${alpha})`;
        ctx.fill();
      }

      const core = ctx.createRadialGradient(
        glow.x,
        glow.y,
        0,
        glow.x,
        glow.y,
        90,
      );
      core.addColorStop(0, "rgba(255,200,50,0.55)");
      core.addColorStop(0.3, "rgba(255,130,0,0.40)");
      core.addColorStop(0.7, "rgba(255,60,0,0.15)");
      core.addColorStop(1, "rgba(255,0,0,0)");
      ctx.fillStyle = core;
      ctx.fillRect(0, 0, width, height);

      rafRef.current = requestAnimationFrame(draw);
    };

    draw();

    return () => {
      cancelAnimationFrame(rafRef.current);
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return (
    <section
      onMouseMove={handleMouseMove}
      className="relative flex min-h-[calc(100vh-4rem)] flex-1 overflow-hidden bg-[#0B0F19] text-white"
    >
      <canvas
        ref={canvasRef}
        className="pointer-events-none absolute inset-0 z-0 h-full w-full"
      />

      <div className="relative z-10 hidden w-1/2 flex-col justify-center px-16 md:flex">
        <p className="mb-4 text-xs font-medium tracking-[0.3em] text-orange-400">
          GET STARTED
        </p>
        <h1 className="text-6xl font-bold leading-[1.05]">
          Build Your
          <br />
          Market
          <br />
          <span className="text-orange-500">Edge</span>
        </h1>
        <p className="mt-6 max-w-md text-lg text-slate-300">
          Create your account to unlock faster workflows for B2B research,
          competitive monitoring, and decision support.
        </p>
      </div>

      <div className="relative z-10 flex w-full items-center justify-center px-5 py-10 md:w-1/2 md:px-8">
        <div className="w-full max-w-[440px] rounded-3xl border border-white/10 bg-white/6 p-3 backdrop-blur-2xl">
          <SignUp
            path="/signup"
            routing="path"
            signInUrl="/login"
            appearance={{
              elements: {
                rootBox: "w-full",
                card: "w-full rounded-[20px] border border-white/10 bg-[#101826]/85 p-6 shadow-none",
                headerTitle: "text-white text-[1.55rem] font-semibold",
                headerSubtitle: "text-slate-400 text-sm",
                socialButtonsBlockButton:
                  "border border-white/10 bg-white/5 text-white hover:bg-white/10 shadow-none",
                socialButtonsBlockButtonText: "text-white font-medium",
                dividerLine: "bg-white/10",
                dividerText: "text-slate-500",
                formFieldLabel: "text-slate-200 text-sm",
                formFieldInput:
                  "h-11 rounded-xl border border-slate-700 bg-[#0f1724] text-white placeholder:text-slate-500 focus:border-orange-500 focus:ring-orange-500",
                footerActionLink: "text-orange-400 hover:text-orange-300",
                formButtonPrimary:
                  "h-11 rounded-xl bg-orange-500 text-white font-semibold hover:bg-orange-600 shadow-none",
                formFieldSuccessText: "text-emerald-400",
                formFieldErrorText: "text-red-400",
                otpCodeFieldInput:
                  "border border-slate-700 bg-[#0f1724] text-white",
              },
            }}
          />
        </div>
      </div>
    </section>
  );
}
