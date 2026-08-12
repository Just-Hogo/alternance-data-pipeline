import json
import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "create_raw_json.py"


def run_script(
    tmp_path: Path,
    payload: str,
    *,
    execution_id: str = "test-execution",
    execution_date: str = "2026_08_12",
) -> subprocess.CompletedProcess[str]:
    input_path = tmp_path / "lba_response.json"
    input_path.write_text(payload, encoding="utf-8")

    environment = os.environ.copy()
    environment["EXECUTION_ID"] = execution_id
    environment["EXECUTION_DATE"] = execution_date

    return subprocess.run(
        [sys.executable, str(SCRIPT_PATH), str(input_path)],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


def test_create_raw_json_preserves_the_json_payload(tmp_path: Path) -> None:
    payload = {
        "jobs": [
            {
                "identifier": {"id": "offer-123"},
                "offer": {"title": "Ingénieur données"},
            }
        ],
        "warnings": [],
    }

    result = run_script(
        tmp_path,
        json.dumps(payload, ensure_ascii=False),
    )

    assert result.returncode == 0, result.stderr

    output_path = tmp_path / "raw_2026_08_12_test-execution.json"
    assert output_path.is_file()
    assert json.loads(output_path.read_text(encoding="utf-8")) == payload
    assert "Ingénieur données" in output_path.read_text(encoding="utf-8")


def test_create_raw_json_uses_the_execution_context_in_the_filename(
    tmp_path: Path,
) -> None:
    result = run_script(
        tmp_path,
        '{"jobs": [], "warnings": []}',
        execution_id="kestra-456",
        execution_date="2026_09_01",
    )

    assert result.returncode == 0, result.stderr
    assert (tmp_path / "raw_2026_09_01_kestra-456.json").is_file()


def test_create_raw_json_rejects_invalid_json(tmp_path: Path) -> None:
    result = run_script(tmp_path, "not valid JSON")

    assert result.returncode != 0
    assert not list(tmp_path.glob("raw_*.json"))
