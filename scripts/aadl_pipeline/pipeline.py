from __future__ import annotations

import json
from pathlib import Path

from .config import GitHubConfig, PipelineConfig
from .core import deduplicate_model_rows, filter_valid_models
from .csvio import write_csv_rows
from .github_api import GitHubClient
from .selection import select_repositories
from .utils import write_jsonl
from .validation import validate_with_command


REPOSITORY_FIELDS = [
    "repo_id",
    "full_name",
    "repo_url",
    "api_url",
    "owner",
    "name",
    "default_branch",
    "latest_commit_sha",
    "license_key",
    "license_name",
    "readme_language",
    "selected_reason",
]

MODEL_FIELDS = [
    "repo_id",
    "repo_full_name",
    "repo_url",
    "default_branch",
    "commit_sha",
    "license_key",
    "license_name",
    "source_file_path",
    "extracted_file_path",
    "extension",
    "sha256",
    "size_bytes",
]

VALIDATION_FIELDS = [
    "extracted_file_path",
    "valid",
    "validator",
    "error_count",
    "warning_count",
    "errors_json",
    "warnings_json",
    "raw_stdout",
    "raw_stderr",
    "return_code",
]


def run_pipeline(gh_cfg: GitHubConfig, cfg: PipelineConfig, validator_cmd_template: str | None = None) -> dict[str, object]:
    cfg.ensure_dirs()
    github = GitHubClient(gh_cfg)

    candidates = list(github.search_code_repositories(cfg.normalized_extensions()))

    #only for quick test
    candidates = candidates[:3]

    write_jsonl(cfg.outdir / "repositories_raw.jsonl", (candidate.to_dict() for candidate in candidates))

    selected = select_repositories(candidates, github)
    selected_rows = [repo.to_dict() for repo in selected]
    write_csv_rows(cfg.outdir / "repositories_selected.csv", selected_rows, REPOSITORY_FIELDS)

    from .clone_extract import clone_and_extract_all

    extracted = clone_and_extract_all(selected, cfg)
    model_rows = [model.to_dict() for model in extracted]
    write_csv_rows(cfg.outdir / "models_all.csv", model_rows, MODEL_FIELDS)

    deduplicated_rows = deduplicate_model_rows(model_rows)
    write_csv_rows(cfg.outdir / "models_dedup.csv", deduplicated_rows, MODEL_FIELDS)

    valid_rows = deduplicated_rows
    if validator_cmd_template:
        validation_results = validate_with_command(deduplicated_rows, validator_cmd_template)
        validation_rows = [result.to_dict() for result in validation_results]
        write_csv_rows(cfg.outdir / "validation_results.csv", validation_rows, VALIDATION_FIELDS)
        valid_rows = filter_valid_models(deduplicated_rows, validation_rows)

    write_csv_rows(cfg.outdir / "models_valid.csv", valid_rows, MODEL_FIELDS)

    summary = {
        "repositories_raw": len(candidates),
        "repositories_selected": len(selected_rows),
        "models_all": len(model_rows),
        "models_dedup": len(deduplicated_rows),
        "models_valid": len(valid_rows),
        "validation_executed": bool(validator_cmd_template),
        "outdir": str(cfg.outdir.resolve()),
    }
    (cfg.outdir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
