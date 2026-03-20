from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import shutil

import git

from .config import PipelineConfig
from .models import ExtractedModel, SelectedRepo
from .utils import safe_repo_dirname, sha256_file


def clone_repo_at_commit(repo: SelectedRepo, config: PipelineConfig) -> Path:
    target_dir = config.clones_dir / safe_repo_dirname(repo.full_name)
    if not target_dir.exists():
        git.Repo.clone_from(repo.repo_url, target_dir, branch=repo.default_branch, single_branch=True)
    repo_obj = git.Repo(target_dir)
    repo_obj.git.checkout(repo.latest_commit_sha)
    return target_dir


def extract_from_repo(repo: SelectedRepo, clone_dir: Path, config: PipelineConfig) -> list[ExtractedModel]:
    extracted: list[ExtractedModel] = []
    repo_out = config.extracted_dir / safe_repo_dirname(repo.full_name)
    repo_out.mkdir(parents=True, exist_ok=True)
    allowed_extensions = set(config.normalized_extensions())

    for path in clone_dir.rglob("*"):
        if not path.is_file():
            continue
        suffix = path.suffix.lower().lstrip(".")
        if suffix not in allowed_extensions:
            continue
        rel_path = path.relative_to(clone_dir)
        destination = repo_out / rel_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
        extracted.append(
            ExtractedModel(
                repo_id=repo.repo_id,
                repo_full_name=repo.full_name,
                repo_url=repo.repo_url,
                default_branch=repo.default_branch,
                commit_sha=repo.latest_commit_sha,
                license_key=repo.license_key,
                license_name=repo.license_name,
                source_file_path=str(rel_path).replace("\\", "/"),
                extracted_file_path=str(destination.resolve()),
                extension=suffix,
                sha256=sha256_file(destination),
                size_bytes=destination.stat().st_size,
            )
        )
    return extracted


def clone_and_extract_all(repos: list[SelectedRepo], config: PipelineConfig) -> list[ExtractedModel]:
    extracted: list[ExtractedModel] = []
    with ThreadPoolExecutor(max_workers=config.clone_workers) as executor:
        futures = {executor.submit(clone_repo_at_commit, repo, config): repo for repo in repos}
        for future in as_completed(futures):
            repo = futures[future]
            clone_dir = future.result()
            extracted.extend(extract_from_repo(repo, clone_dir, config))
    return extracted
