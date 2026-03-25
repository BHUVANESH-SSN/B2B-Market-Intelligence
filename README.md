# 🎭 OrchestAI | Market Intelligence Engine (Monorepo)

**OrchestAI** is an end-to-end B2B market intelligence platform that leverages AI agents and automated crawlers to monitor competitor activities.

## 📁 Repository Structure

- **[/frontend](file:///h:/B2B-Market-Intelligence/frontend)**: Next.js 16 dashboard with high-fidelity analytics and AI-driven competitor discovery tools. Built with Tailwind CSS 4 and Clerk.
- **[/backend](file:///h:/B2B-Market-Intelligence/backend)**: Python (FastAPI/Flask) service handling data persistence, API endpoints, and system coordination.
- **[/ai-agents](file:///h:/B2B-Market-Intelligence/ai-agents)**: Core intelligence layer where LLM agents (Recommender, Diagnosticians, Scorer) process raw competitor data into actionable strategy reports.
- **[/scraper-agents](file:///h:/B2B-Market-Intelligence/scraper-agents)**: Specialized crawling agents built to navigate landing pages, pricing tables, and social signals.

## 🚀 Development Workflow

### 1. Frontend
Run the dashboard to see live visualizations:
```bash
cd frontend
pnpm run dev
```

### 2. Connected Pipeline
A bridge script to test the interaction between all services:
```bash
python run_connected_pipeline.py
```

## 🔐 Configuration
Refer to individual directory `README` files for environment secrets and setup requirements.

---
© 2026 OrchestAI Team.
