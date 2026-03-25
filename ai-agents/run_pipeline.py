"""Local runner for the AI pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from backend.agents.orchestrator import run_pipeline
from backend.io_models import PipelineInput, PipelineOutput


DEFAULT_INPUT = {
    "competitor": "Acme",
    "diffs": {
        "pricing": [
            "Introduced annual discount for enterprise plan",
            "Added CTA for custom pricing demo",
        ],
        "hero": ["Replaced headline with automation-first message"],
        "features": ["Added Salesforce integration to workflow builder page"],
    },
    "history_claims": [],
}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the AI agents pipeline.")
    parser.add_argument(
        "--input",
        dest="input_path",
        help="Path to a JSON input file. If omitted, built-in sample input is used.",
    )
    parser.add_argument(
        "--output",
        dest="output_path",
        default="outputs/latest_report.json",
        help="Where to write the generated report JSON.",
    )
    return parser.parse_args()


def _load_input(input_path: str | None) -> PipelineInput:
    if input_path is None:
        return PipelineInput.from_dict(DEFAULT_INPUT)

    raw = Path(input_path).read_text(encoding="utf-8")
    return PipelineInput.from_json(raw)


def _build_payload(state: dict) -> PipelineOutput:
    payload = {
        "metadata": state.get("metadata", {}),
        "insights": [item.to_dict() for item in state.get("insights", [])],
        "recommendations": [item.to_dict() for item in state.get("recommendations", [])],
    }
    return PipelineOutput(**payload)


def _write_output(output_path: str, payload: PipelineOutput) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload.to_dict(), indent=2), encoding="utf-8")


def main() -> None:
    args = _parse_args()
    pipeline_input = _load_input(args.input_path)
    state = run_pipeline(
        competitor=pipeline_input.competitor,
        diffs=pipeline_input.diffs,
        history_claims=pipeline_input.history_claims,
    )
    payload = _build_payload(state)
    _write_output(args.output_path, payload)
    print(json.dumps(payload.to_dict(), indent=2))


if __name__ == "__main__":
    main()
