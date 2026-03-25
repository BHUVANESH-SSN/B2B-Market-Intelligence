# AI Agents

This folder is your dedicated workspace for the AI/Intelligence part of the project.

## What lives here

- `backend/agents/analyst_agent.py` - turns diffs into structured insights
- `backend/agents/scorer_agent.py` - scores insights deterministically
- `backend/agents/recommender_agent.py` - turns insights into action items
- `backend/agents/orchestrator.py` - runs the full AI pipeline
- `backend/prompts.py` - prompt templates and prompt builders
- `tests/test_agents.py` - baseline tests for agent behavior

## Current mode

The pipeline works in a fallback local mode even before the scraper, API, and real LLM wiring are finished.

## Run from this folder

```bash
cd ai-agents
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python3 -m compileall backend tests
python3 run_pipeline.py --input examples/sample_input.json --output outputs/latest_report.json
```

If you want to use the scraper output directly, run:

```bash
python3 run_pipeline.py --input ../scraper-agents/outputs/latest_diff.json --output outputs/latest_report.json
```

## Integration contract

Your expected input is a JSON file with:

```json
{
  "competitor": "Acme",
  "diffs": {
    "pricing": ["Introduced annual discount for enterprise plan"],
    "hero": ["Replaced headline with automation-first message"]
  },
  "history_claims": ["Older insight text if you want novelty scoring to down-rank repeats"]
}
```

Your output is:

- structured insights
- scored priorities
- recommendations
- saved JSON report in `outputs/latest_report.json`

## What To Give The AI Agents

The scraper or diff pipeline should send you:

- `competitor`: the competitor name
- `diffs`: semantic website changes grouped by section
- `history_claims`: optional prior claims for novelty scoring

Good `diffs` input looks like:

```json
{
  "pricing": [
    "Introduced annual discount for enterprise plan",
    "Added CTA for custom pricing demo"
  ],
  "hero": [
    "Replaced headline with automation-first message"
  ],
  "features": [
    "Added Salesforce integration to workflow builder page"
  ]
}
```

Avoid sending:

- raw full HTML
- noisy nav/footer text
- duplicate lines
- unrelated page content with no business change

## Next steps

1. Align this JSON schema with the scraper and backend teammates.
2. Feed real semantic diffs from Person 3 into `examples/sample_input.json` shape.
3. Expose `run_pipeline()` through the shared API/task runner.

## Config

- `ANTHROPIC_API_KEY` enables Anthropic calls
- `OPENAI_API_KEY` enables OpenAI calls
- `GROQ_API_KEY` enables Groq calls
- `LLM_PROVIDER` chooses which provider to use
- `ANALYST_MODEL` controls the analyst model
- `RECOMMENDER_MODEL` controls the recommender model

## Groq Setup

If Groq is your only API provider, set your `.env` like this:

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
ANALYST_MODEL=openai/gpt-oss-20b
RECOMMENDER_MODEL=openai/gpt-oss-20b
```
