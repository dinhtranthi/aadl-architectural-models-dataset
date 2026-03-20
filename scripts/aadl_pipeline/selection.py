from __future__ import annotations

from typing import Iterable

import requests

from .github_api import GitHubClient
from .language import detect_language
from .models import RepoCandidate, SelectedRepo


def select_repositories(candidates: Iterable[RepoCandidate], gh: GitHubClient) -> list[SelectedRepo]:
    selected: list[SelectedRepo] = []
    for repo in candidates:
        if repo.private or repo.archived or repo.disabled or repo.fork:
            continue

        license_key = repo.license_key
        license_name = repo.license_name
        if not license_key:
            try:
                license_key, license_name = gh.get_repo_license(repo.owner, repo.name)
            except requests.HTTPError:
                license_key, license_name = None, None
        if not license_key:
            continue

        readme_language = None
        try:
            readme_language = detect_language(gh.get_readme(repo.owner, repo.name))
        except requests.HTTPError:
            readme_language = None

        if readme_language not in (None, "en"):
            continue

        try:
            sha = gh.get_default_branch_head_sha(repo.owner, repo.name, repo.default_branch)
        except requests.HTTPError:
            continue

        selected.append(
            SelectedRepo(
                repo_id=repo.repo_id,
                full_name=repo.full_name,
                repo_url=repo.html_url,
                api_url=repo.api_url,
                owner=repo.owner,
                name=repo.name,
                default_branch=repo.default_branch,
                latest_commit_sha=sha,
                license_key=license_key,
                license_name=license_name or "UNKNOWN",
                readme_language=readme_language,
                selected_reason="fork_excluded_license_present_readme_english_or_unknown",
            )
        )
    return selected
