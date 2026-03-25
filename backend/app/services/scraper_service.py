from __future__ import annotations

import sys
from pathlib import Path

from app.core.config import settings
from app.db.schemas.analysis import ScraperResult


def _bootstrap_scraper_imports() -> None:
    scraper_root = Path(settings.scraper_agents_dir)
    scraper_root_str = str(scraper_root)
    if scraper_root_str not in sys.path:
        sys.path.insert(0, scraper_root_str)


def run_scraper_pipeline(
    *,
    competitor_name: str,
    url: str | None,
    current_html: str | None,
    previous_html: str | None,
) -> ScraperResult:
    _bootstrap_scraper_imports()

    from scraper.diff_agent import diff_sections
    from scraper.html_utils import extract_sections
    from scraper.scraper_agent import fetch_page, hash_content, store_snapshot

    if current_html is None:
        if not url:
            raise ValueError("A URL or current_html must be provided.")
        import asyncio

        current_html = asyncio.run(fetch_page(url))

    current_sections = extract_sections(current_html)
    previous_sections = extract_sections(previous_html) if previous_html else {}
    diffs = diff_sections(current_sections, previous_sections)

    snapshot_path = store_snapshot(
        competitor_name,
        current_html,
        str(settings.snapshot_storage_dir),
    )
    return ScraperResult(
        current_html=current_html,
        current_sections=current_sections,
        previous_sections=previous_sections,
        diffs=diffs,
        snapshot_path=snapshot_path,
        content_hash=hash_content(current_html),
    )
