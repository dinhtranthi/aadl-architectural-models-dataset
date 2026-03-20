from __future__ import annotations

import time
from typing import Any, Generator, Optional

import requests
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from .config import GitHubConfig
from .models import RepoCandidate


class GitHubRateLimitError(RuntimeError):
    pass


class GitHubClient:
    def __init__(self, config: GitHubConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {config.token}",
                "X-GitHub-Api-Version": config.api_version,
                "User-Agent": config.user_agent,
            }
        )

    def _sleep_for_rate_limit_if_needed(self, response: requests.Response) -> None:
        remaining = response.headers.get("x-ratelimit-remaining")
        reset = response.headers.get("x-ratelimit-reset")
        retry_after = response.headers.get("retry-after")

        if response.status_code not in (403, 429):
            return
        if retry_after:
            time.sleep(int(retry_after) + 1)
            return
        if remaining == "0" and reset:
            wait_seconds = max(int(reset) - int(time.time()), 0) + 1
            time.sleep(wait_seconds)
            return
        time.sleep(60)

    @retry(
        retry=retry_if_exception_type((requests.RequestException, GitHubRateLimitError)),
        wait=wait_exponential(multiplier=1, min=2, max=60),
        stop=stop_after_attempt(8),
        reraise=True,
    )
    def _request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        response = self.session.request(method, url, timeout=self.config.timeout_seconds, **kwargs)
        if response.status_code in (403, 429):
            self._sleep_for_rate_limit_if_needed(response)
            raise GitHubRateLimitError(f"Rate-limited calling {url}: {response.status_code}")
        response.raise_for_status()
        return response

    def search_code_repositories(self, extensions: list[str]) -> Generator[RepoCandidate, None, None]:
        seen_repo_ids: set[int] = set()
        for extension in extensions:
            page = 1

            #quick test
            MAX_PAGES = 1

            while page <= MAX_PAGES:
                response = self._request(
                    "GET",
                    f"{self.config.base_url}/search/code",
                    params={
                        "q": f"extension:{extension}",
                        "per_page": self.config.per_page,
                        "page": page,
                    },
                )
                items = response.json().get("items", [])
                if not items:
                    break
                for item in items:
                    repo = item["repository"]
                    repo_id = int(repo["id"])
                    if repo_id in seen_repo_ids:
                        continue
                    seen_repo_ids.add(repo_id)
                    license_info = repo.get("license") or {}
                    yield RepoCandidate(
                        repo_id=repo_id,
                        full_name=repo["full_name"],
                        html_url=repo["html_url"],
                        api_url=repo["url"],
                        owner=repo["owner"]["login"],
                        name=repo["name"],
                        default_branch=repo.get("default_branch", "main"),
                        fork=bool(repo.get("fork", False)),
                        archived=bool(repo.get("archived", False)),
                        disabled=bool(repo.get("disabled", False)),
                        private=bool(repo.get("private", False)),
                        language=repo.get("language"),
                        description=repo.get("description"),
                        license_key=license_info.get("key"),
                        license_name=license_info.get("name"),
                        stargazers_count=int(repo.get("stargazers_count", 0)),
                    )
                if len(items) < self.config.per_page:
                    break
                page += 1

    def get_readme(self, owner: str, repo: str) -> Optional[str]:
        response = self._request(
            "GET",
            f"{self.config.base_url}/repos/{owner}/{repo}/readme",
            headers={"Accept": "application/vnd.github.raw+json"},
        )
        return response.text

    def get_default_branch_head_sha(self, owner: str, repo: str, branch: str) -> str:
        response = self._request("GET", f"{self.config.base_url}/repos/{owner}/{repo}/commits/{branch}")
        return response.json()["sha"]

    def get_repo_license(self, owner: str, repo: str) -> tuple[Optional[str], Optional[str]]:
        response = self._request("GET", f"{self.config.base_url}/repos/{owner}/{repo}/license")
        payload = response.json()
        license_info = payload.get("license") or {}
        return license_info.get("key"), license_info.get("name")
