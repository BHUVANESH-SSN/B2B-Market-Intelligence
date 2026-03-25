# Scraper Agents

This folder is your dedicated workspace for scraping, snapshot storage, section extraction, and semantic diffs.

## What this does

- reads a local HTML file or a live URL
- extracts useful business sections from the page
- stores raw HTML snapshots
- computes semantic diffs between snapshots
- outputs clean JSON for the AI agents team

## Run from this folder

```bash
cd scraper-agents
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python3 run_scraper.py --input-file examples/current_page.html --competitor Acme
```

## Input Contract

You can give this scraper layer:

- a local HTML file with `--input-file`
- a live URL with `--url`
- an optional previous HTML file with `--previous-file`

## Output Contract

This layer outputs JSON shaped like:

```json
{
  "competitor": "Acme",
  "diffs": {
    "hero": ["Changed headline text"],
    "pricing": ["Added annual discount"],
    "features": ["Added Salesforce integration"]
  },
  "history_claims": []
}
```

That output is meant to feed directly into the AI agents folder.
