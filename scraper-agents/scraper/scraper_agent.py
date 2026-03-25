"""Scraper agent for loading HTML from file or URL and storing snapshots."""

from __future__ import annotations

import hashlib
import os
from datetime import UTC, datetime
from pathlib import Path


def hash_content(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def load_html_from_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


async def fetch_page(url: str) -> str:
    from playwright.async_api import async_playwright

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.route(
            "**/*",
            lambda route: route.abort()
            if route.request.resource_type in {"image", "media", "font"}
            else route.continue_(),
        )
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        html = await page.content()
        await browser.close()
        return html


def store_snapshot(competitor: str, html: str, snapshot_dir: str) -> str:
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    safe_name = competitor.lower().replace(" ", "_")
    directory = Path(snapshot_dir)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{safe_name}_{timestamp}.html"
    path.write_text(html, encoding="utf-8")
    return os.fspath(path)
