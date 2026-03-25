"""Run scraper output through the AI agents pipeline."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def _resolve_ai_python() -> str:
    venv_python = Path("ai-agents/.venv/bin/python")
    if venv_python.exists():
        return str(venv_python.resolve())
    return "python3"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run scraper output into AI agents.")
    parser.add_argument(
        "--input",
        default="scraper-agents/outputs/latest_diff.json",
        help="Path to scraper output JSON",
    )
    parser.add_argument(
        "--output",
        default="ai-agents/outputs/latest_report.json",
        help="Path to AI report JSON",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Scraper output not found: {input_path}")

    subprocess.run(
        [
            _resolve_ai_python(),
            "run_pipeline.py",
            "--input",
            str(input_path.resolve()),
            "--output",
            str(Path(args.output).resolve()),
        ],
        cwd=Path("ai-agents"),
        check=True,
    )


if __name__ == "__main__":
    main()
