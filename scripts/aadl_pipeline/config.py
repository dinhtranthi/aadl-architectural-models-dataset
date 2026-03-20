from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import os
from typing import List


@dataclass
class GitHubConfig:
    token: str
    base_url: str = os.getenv("GITHUB_BASE_URL", "https://api.github.com")
    api_version: str = os.getenv("GITHUB_API_VERSION", "2022-11-28")
    per_page: int = 100
    timeout_seconds: int = 60
    user_agent: str = "aadl-corpus-miner/0.2"


@dataclass
class PipelineConfig:
    outdir: Path
    workdir: Path
    extensions: List[str] = field(default_factory=lambda: ["aadl", "aadl2", "aaxl2"])
    clone_workers: int = 4

    @property
    def clones_dir(self) -> Path:
        return self.workdir / "clones"

    @property
    def extracted_dir(self) -> Path:
        return self.workdir / "extracted_models"

    @property
    def temp_dir(self) -> Path:
        return self.workdir / "tmp"

    def normalized_extensions(self) -> list[str]:
        return [ext.lower().lstrip(".") for ext in self.extensions]

    def ensure_dirs(self) -> None:
        for path in [self.outdir, self.workdir, self.clones_dir, self.extracted_dir, self.temp_dir]:
            path.mkdir(parents=True, exist_ok=True)
