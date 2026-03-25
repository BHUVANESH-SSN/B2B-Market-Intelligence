"""CLI entrypoint for scraper and diff agents."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path

from scraper.diff_agent import diff_sections
from scraper.html_utils import extract_sections
from scraper.io_models import DiffPayload
from scraper.scraper_agent import fetch_page, hash_content, load_html_from_file, store_snapshot


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run scraper and diff agents.")
    parser.add_argument("--competitor", required=True, help="Competitor name")
    parser.add_argument("--input-file", help="Current HTML file path")
    parser.add_argument("--previous-file", help="Previous HTML file path")
    parser.add_argument("--url", help="Live URL to fetch with Playwright")
    parser.add_argument(
        "--output",
        default="outputs/latest_diff.json",
        help="Output JSON path for AI-agent-ready diff payload",
    )
    return parser.parse_args()


def _load_env_value(name: str, default: str) -> str:
    return os.getenv(name, default)


async def _load_current_html(args: argparse.Namespace) -> str:
    if args.input_file:
        return load_html_from_file(args.input_file)
    if args.url:
        return await fetch_page(args.url)
    raise ValueError("Provide either --input-file or --url")


def _write_output(path: str, payload: DiffPayload) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(payload.to_json(), encoding="utf-8")


async def main() -> None:
    args = _parse_args()
    snapshot_dir = _load_env_value("SNAPSHOT_DIR", "./snapshots")

    current_html = await _load_current_html(args)
    previous_html = load_html_from_file(args.previous_file) if args.previous_file else ""

    current_sections = extract_sections(current_html)
    previous_sections = extract_sections(previous_html) if previous_html else {}
    diffs = diff_sections(current_sections, previous_sections)

    store_snapshot(args.competitor, current_html, snapshot_dir)

    payload = DiffPayload(
        competitor=args.competitor,
        diffs=diffs,
        history_claims=[],
    )

    _write_output(args.output, payload)

    result = {
        "competitor": args.competitor,
        "hash": hash_content(current_html),
        "sections": current_sections,
        "diffs": diffs,
        "output_path": args.output,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
