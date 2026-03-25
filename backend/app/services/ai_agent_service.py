from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from app.core.config import settings
from app.db.schemas.analysis import AIReportResult


def _resolve_python_executable(agent_dir: Path) -> str:
    candidates = [
        agent_dir / ".venv" / "Scripts" / "python.exe",
        agent_dir / ".venv" / "bin" / "python",
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return sys.executable


def run_ai_pipeline(payload: dict) -> AIReportResult:
    agent_dir = Path(settings.ai_agents_dir)
    python_exec = _resolve_python_executable(agent_dir)
    settings.runtime_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(dir=settings.runtime_dir) as tmp_dir:
        tmp_path = Path(tmp_dir)
        input_path = tmp_path / "ai_input.json"
        output_path = tmp_path / "ai_output.json"
        input_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

        completed = subprocess.run(
            [
                python_exec,
                "run_pipeline.py",
                "--input",
                str(input_path),
                "--output",
                str(output_path),
            ],
            cwd=agent_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                "AI pipeline failed: "
                f"{completed.stderr.strip() or completed.stdout.strip() or 'unknown error'}"
            )

        if not output_path.exists():
            raise RuntimeError("AI pipeline did not write an output report.")

        payload = json.loads(output_path.read_text(encoding="utf-8"))
        return AIReportResult(**payload)
