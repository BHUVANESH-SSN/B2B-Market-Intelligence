"""HTML cleaning and section extraction helpers."""

from __future__ import annotations

from bs4 import BeautifulSoup
from bs4 import FeatureNotFound


NOISE_SELECTORS = [
    "script",
    "style",
    "noscript",
    "svg",
    "img",
    "nav",
    "footer",
    "header .menu",
    ".cookie",
    ".cookies",
    ".cookie-banner",
    ".newsletter",
]


def _clean_text(text: str) -> str:
    return " ".join(text.split())


def _collect_list_items(root: BeautifulSoup, limit: int = 8) -> list[str]:
    items: list[str] = []
    for node in root.select("li"):
        text = _clean_text(node.get_text(" ", strip=True))
        if text and text not in items:
            items.append(text)
        if len(items) >= limit:
            break
    return items


def extract_sections(html: str) -> dict[str, list[str]]:
    try:
        soup = BeautifulSoup(html, "lxml")
    except FeatureNotFound:
        soup = BeautifulSoup(html, "html.parser")

    for selector in NOISE_SELECTORS:
        for node in soup.select(selector):
            node.decompose()

    sections: dict[str, list[str]] = {}

    hero_node = soup.find(["main", "section", "body"])
    hero_lines: list[str] = []
    if hero_node is not None:
        hero_heading = hero_node.find(["h1", "h2"])
        if hero_heading:
            hero_lines.append(_clean_text(hero_heading.get_text(" ", strip=True)))
        hero_paragraph = hero_node.find("p")
        if hero_paragraph:
            hero_lines.append(_clean_text(hero_paragraph.get_text(" ", strip=True)))
    if hero_lines:
        sections["hero"] = hero_lines

    pricing_lines: list[str] = []
    for node in soup.find_all(["section", "div"], string=False):
        text = _clean_text(node.get_text(" ", strip=True))
        lower = text.lower()
        if any(keyword in lower for keyword in ("pricing", "plan", "billing", "$", "demo")):
            if text and text not in pricing_lines:
                pricing_lines.append(text[:280])
        if len(pricing_lines) >= 6:
            break
    if pricing_lines:
        sections["pricing"] = pricing_lines

    feature_lines = _collect_list_items(soup)
    if feature_lines:
        sections["features"] = feature_lines

    cta_lines: list[str] = []
    for node in soup.find_all(["a", "button"]):
        text = _clean_text(node.get_text(" ", strip=True))
        if text and len(text) <= 80 and text not in cta_lines:
            cta_lines.append(text)
        if len(cta_lines) >= 8:
            break
    if cta_lines:
        sections["ctas"] = cta_lines

    if not sections:
        body_text = _clean_text(soup.get_text(" ", strip=True))
        sections["other"] = [body_text[:500]] if body_text else []

    return sections
