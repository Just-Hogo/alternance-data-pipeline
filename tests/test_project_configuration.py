import json
import re
import subprocess
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FLOW_DIRECTORY = PROJECT_ROOT / "flows"
SQL_DIRECTORY = PROJECT_ROOT / "sql" / "initialization"
READ_EXPRESSION = re.compile(r"read\(['\"]([^'\"]+)['\"]\)")


def load_flow(path: Path) -> dict:
    content = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(content, dict), f"{path} ne contient pas un objet YAML"
    return content


def test_search_configuration_is_valid_json() -> None:
    path = PROJECT_ROOT / "config" / "search_config.json"
    configuration = json.loads(path.read_text(encoding="utf-8"))

    lba_configuration = configuration["la_bonne_alternance"]
    assert lba_configuration["rome_codes"]
    assert all(isinstance(code, str) for code in lba_configuration["rome_codes"])
    assert lba_configuration["max_offer_age_hours"] > 0


def test_all_flow_files_have_the_required_top_level_properties() -> None:
    flow_paths = sorted(FLOW_DIRECTORY.glob("*.yml"))
    assert flow_paths, "Aucun flow Kestra trouvé"

    for path in flow_paths:
        flow = load_flow(path)
        assert flow.get("id"), f"id absent dans {path}"
        assert flow.get("namespace"), f"namespace absent dans {path}"
        assert isinstance(flow.get("tasks"), list), f"tasks invalide dans {path}"
        assert flow["tasks"], f"Aucune tâche dans {path}"


def test_every_namespace_read_expression_targets_an_existing_file() -> None:
    missing_references: list[str] = []

    for path in sorted(FLOW_DIRECTORY.glob("*.yml")):
        content = path.read_text(encoding="utf-8")
        for reference in READ_EXPRESSION.findall(content):
            referenced_path = PROJECT_ROOT / reference.lstrip("/")
            if not referenced_path.is_file():
                missing_references.append(f"{path.name}: {reference}")

    assert not missing_references, "Références absentes :\n" + "\n".join(
        missing_references
    )


def test_database_initialization_flow_uses_all_sql_files_in_order() -> None:
    flow_path = FLOW_DIRECTORY / "initialize_alternance_database.yml"
    flow_content = flow_path.read_text(encoding="utf-8")

    referenced_files = READ_EXPRESSION.findall(flow_content)
    expected_files = [
        path.relative_to(PROJECT_ROOT).as_posix()
        for path in sorted(SQL_DIRECTORY.glob("*.sql"))
    ]

    assert referenced_files == expected_files


def test_kestraignore_only_exposes_namespace_file_directories() -> None:
    path = PROJECT_ROOT / ".kestraignore"
    rules = [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]

    assert rules == [
        "*",
        "!config/",
        "!config/**",
        "!scripts/",
        "!scripts/**",
        "!sql/",
        "!sql/**",
    ]


def is_ignored_by_git(relative_path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "--quiet", "--no-index", relative_path],
        cwd=PROJECT_ROOT,
        check=False,
    )
    return result.returncode == 0


def test_gitignore_protects_secrets_but_keeps_the_example() -> None:
    assert is_ignored_by_git(".env")
    assert is_ignored_by_git(".env_encoded")
    assert not is_ignored_by_git(".env.example")


def test_secret_environment_files_are_not_tracked() -> None:
    result = subprocess.run(
        ["git", "ls-files", "--", ".env", ".env_encoded"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    assert not result.stdout.strip()
