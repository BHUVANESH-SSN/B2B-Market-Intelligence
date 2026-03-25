"""Diff agent for comparing extracted business sections."""

from __future__ import annotations


def diff_sections(
    current_sections: dict[str, list[str]],
    previous_sections: dict[str, list[str]] | None = None,
) -> dict[str, list[str]]:
    previous_sections = previous_sections or {}
    diffs: dict[str, list[str]] = {}

    section_names = set(current_sections) | set(previous_sections)
    for section_name in sorted(section_names):
        current_items = current_sections.get(section_name, [])
        previous_items = set(previous_sections.get(section_name, []))
        changes = [item for item in current_items if item not in previous_items]
        if changes:
            diffs[section_name] = changes

    return diffs
