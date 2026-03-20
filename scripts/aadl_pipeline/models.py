from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass
class RepoCandidate:
    repo_id: int
    full_name: str
    html_url: str
    api_url: str
    owner: str
    name: str
    default_branch: str
    fork: bool
    archived: bool
    disabled: bool
    private: bool
    language: Optional[str]
    description: Optional[str]
    license_key: Optional[str]
    license_name: Optional[str]
    stargazers_count: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SelectedRepo:
    repo_id: int
    full_name: str
    repo_url: str
    api_url: str
    owner: str
    name: str
    default_branch: str
    latest_commit_sha: str
    license_key: str
    license_name: str
    readme_language: Optional[str]
    selected_reason: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ExtractedModel:
    repo_id: int
    repo_full_name: str
    repo_url: str
    default_branch: str
    commit_sha: str
    license_key: str
    license_name: str
    source_file_path: str
    extracted_file_path: str
    extension: str
    sha256: str
    size_bytes: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ValidationResult:
    extracted_file_path: str
    valid: bool
    validator: str
    error_count: int
    warning_count: int
    errors_json: str
    warnings_json: str
    raw_stdout: str
    raw_stderr: str
    return_code: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
