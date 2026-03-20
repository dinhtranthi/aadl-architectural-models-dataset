from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import GitHubConfig, PipelineConfig
from .pipeline import run_pipeline
from .utils import env_required


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Mine AADL model files from GitHub.")
    parser.add_argument("--outdir", type=Path, required=True, help="Directory for CSV/JSON outputs")
    parser.add_argument("--workdir", type=Path, required=True, help="Directory for clones and extracted files")
    parser.add_argument("--extensions", nargs="+", default=["aadl", "aadl2", "aaxl2"])
    parser.add_argument("--clone-workers", type=int, default=4)
    parser.add_argument("--validator-cmd", type=str, default=None)
    parser.add_argument("--per-page", type=int, default=100)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    gh_cfg = GitHubConfig(
        token=env_required("GITHUB_TOKEN"),
        per_page=args.per_page,
        timeout_seconds=args.timeout_seconds,
    )
    pipeline_cfg = PipelineConfig(
        outdir=args.outdir,
        workdir=args.workdir,
        extensions=args.extensions,
        clone_workers=args.clone_workers,
    )
    summary = run_pipeline(gh_cfg, pipeline_cfg, validator_cmd_template=args.validator_cmd)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
