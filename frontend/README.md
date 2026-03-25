# 🎭 OrchestAI | Market Intelligence Engine

**OrchestAI** is a premium, AI-powered competitive intelligence platform designed for B2B SaaS teams. It crawls competitor landing pages, tracks messaging shifts, detects pricing changes, and surfaces strategic whitespace—all powered by autonomous AI agents.

---

## ✨ Key Features

### 🔍 AI-Powered Competitor Discovery
Describe your product, and OrchestAI's discovery engine will automatically find and rank competitors by similarity. No more manually hunting for your market peers.

### 📊 Intelligence Dashboard
A high-fidelity dashboard giving you a real-time view of:
- **Traffic vs. Market Avg:** Benchmark your unique visitor growth against your top 5 competitors.
- **AI Diagnostics:** Strategic strength/vulnerability analysis based on live landing page data.
- **Sentiment Analysis:** (Coming Soon) Track brand perception shifts across G2 and Trustpilot.

### 📈 Market Momentum (Trends)
Visualize competitor activity volume. Detect when a market leader is pivoting their messaging or aggressively testing new pricing tiers.

### 📑 Strategy Reports
Synthesized executive reports compiled by our **Recommender Agent**, providing deep-dive teardowns into competitor onboarding, pricing studies, and knowledge management shifts.

---

## 🛠️ Technology Stack

- **Framework:** [Next.js 16](https://nextjs.org/) (App Router)
- **Styling:** [Tailwind CSS 4.0](https://tailwindcss.com/)
- **Authentication:** [Clerk](https://clerk.com/)
- **Visuals:** SVG-based custom coordinate charts (Recharts-inspired coordination)
- **Aesthetics:** Pearl white/Skyblue/Violet gradient themes with Glassmorphism.

---

## 🚀 Getting Started

### 1. Installation
Clone the repository and install dependencies:

```bash
cd frontend
pnpm install
```

### 2. Environment Setup
Create a `.env.local` file with your Clerk credentials:

```bash
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_pub_key
CLERK_SECRET_KEY=your_secret_key
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/login
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/signup
```

### 3. Run Locally
Start the development server with Turbopack for near-instant hot reloads:

```bash
pnpm run dev
```

Open [http://localhost:3000](http://localhost:3000) to access the engine.

---

## 📂 Architecture

- `/app`: Root-level clean routing (`/competitors`, `/discover`, `/insights`).
- `/app/components`: Reusable UI components including the `DashboardLayout` shell.
- `/public`: Static assets and icons.

---

## 🛡️ License
Distributed under the MIT License. See `LICENSE` for more information.
