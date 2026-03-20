# AADL GitHub Pipeline

A publishable Python package for mining AADL model files from GitHub, deduplicating them at file level, and validating them with an external OSATE-compatible command.

## What the pipeline does

1. Queries the GitHub REST API for repositories containing files with extensions `aadl`, `aadl2`, or `aaxl2`.
2. Exhaustively paginates search results and deduplicates repositories across extensions.
3. Filters repositories by the criteria described in the collection protocol:
   - exclude forks
   - exclude archived / disabled / private repositories
   - exclude repositories without accessible license metadata
   - keep repositories whose README appears to be English, or whose README language cannot be determined
4. Resolves the latest commit on the default branch.
5. Clones each selected repository and checks out that commit.
6. Extracts each AADL file as a single unit of analysis.
7. Preserves provenance metadata.
8. Removes duplicate files using SHA-256 hashing.
9. Optionally validates extracted files using an external validator command.


## Installation

Create a fresh environment and install in editable mode:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

For development tools:

```bash
pip install -e .[dev]
```

## Required environment variable

```bash
export GITHUB_TOKEN="<your-personal-access-token>"
```

## Run the full pipeline

```bash
aadl-github-pipeline \
  --outdir outputs \
  --workdir workspace \
  --clone-workers 4 \
  --extensions aadl aadl2 aaxl2
```

## Output files

- `repositories_raw.jsonl`: all repositories returned by the search step, before filtering
- `repositories_selected.csv`: repositories retained after filtering
- `models_all.csv`: all extracted file-level models
- `models_dedup.csv`: deduplicated models after SHA-256 filtering
- `validation_results.csv`: validator output per extracted model, if validation is enabled
- `models_valid.csv`: only models marked valid by the validator, if validation is enabled
- `summary.json`: summary counts

## Notes

- This package intentionally avoids `pandas`, so it does not pull in the `numpy` / `numexpr` stack.
- It supports Python 3.9+.
- The validation layer is adapter-based because OSATE execution differs across installations and operating systems.

