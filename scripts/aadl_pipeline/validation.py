from __future__ import annotations

import json
import shlex
import subprocess
from pathlib import Path
from typing import Iterable

from .models import ValidationResult


def normalize_result(file_path: str, validator: str, completed: subprocess.CompletedProcess[str]) -> ValidationResult:
    valid = False
    errors = []
    warnings = []
    try:
        payload = json.loads((completed.stdout or "").strip() or "{}")
        valid = bool(payload.get("valid", False)) and completed.returncode == 0
        errors = payload.get("errors", []) or []
        warnings = payload.get("warnings", []) or []
    except json.JSONDecodeError:
        if completed.returncode == 0:
            valid = True

    return ValidationResult(
        extracted_file_path=file_path,
        valid=valid,
        validator=validator,
        error_count=len(errors),
        warning_count=len(warnings),
        errors_json=json.dumps(errors, ensure_ascii=False),
        warnings_json=json.dumps(warnings, ensure_ascii=False),
        raw_stdout=completed.stdout,
        raw_stderr=completed.stderr,
        return_code=completed.returncode,
    )


def validate_with_command(rows: Iterable[dict[str, str]], validator_cmd_template: str) -> list[ValidationResult]:
    results: list[ValidationResult] = []
    for row in rows:
        file_path = str(Path(row["extracted_file_path"]).resolve())
        command = validator_cmd_template.format(file=shlex.quote(file_path))
        completed = subprocess.run(command, shell=True, text=True, capture_output=True)
        results.append(normalize_result(file_path, "command", completed))
    return results
