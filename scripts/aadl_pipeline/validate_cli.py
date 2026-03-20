from __future__ import annotations

import argparse
from pathlib import Path

from .csvio import read_csv_rows, write_csv_rows
from .pipeline import VALIDATION_FIELDS
from .validation import validate_with_command


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate extracted AADL models using an external command.")
    parser.add_argument("--models-csv", type=Path, required=True)
    parser.add_argument("--validator-cmd", type=str, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    rows = read_csv_rows(args.models_csv)
    results = validate_with_command(rows, args.validator_cmd)
    write_csv_rows(args.output_csv, [result.to_dict() for result in results], VALIDATION_FIELDS)
    print(f"Wrote {len(results)} validation rows to {args.output_csv}")


if __name__ == "__main__":
    main()
