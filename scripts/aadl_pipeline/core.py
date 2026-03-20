from __future__ import annotations


def deduplicate_model_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    sorted_rows = sorted(
        rows,
        key=lambda row: (str(row.get("repo_full_name", "")), str(row.get("source_file_path", ""))),
    )
    seen_hashes: set[str] = set()
    deduplicated: list[dict[str, object]] = []
    for row in sorted_rows:
        sha256 = str(row["sha256"])
        if sha256 in seen_hashes:
            continue
        seen_hashes.add(sha256)
        deduplicated.append(row)
    return deduplicated


def filter_valid_models(
    model_rows: list[dict[str, object]], validation_rows: list[dict[str, object]]
) -> list[dict[str, object]]:
    validity_by_path = {
        str(row["extracted_file_path"]): str(row["valid"]).lower() == "true" for row in validation_rows
    }
    return [row for row in model_rows if validity_by_path.get(str(row["extracted_file_path"]), False)]
