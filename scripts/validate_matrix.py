#!/usr/bin/env python3
"""Validate the subject-specific capability matrices."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX_DIR = ROOT / "data" / "capability_matrices"
CURRICULUM_PATH = ROOT / "data" / "curriculum" / "advanced_grade7.csv"
EXPECTED_MATRICES = {
    "algebra.csv",
    "geometry.csv",
    "probability_statistics.csv",
}
REQUIRED_COLUMNS = {
    "capability",
    "status",
    "level",
    "evidence",
    "next_gate",
}
ALLOWED = {"PASS", "WATCH", "TRAIN", "NEW"}
CURRICULUM_COLUMNS = {
    "domain",
    "sequence",
    "unit",
    "hours",
    "capabilities",
}
EXPECTED_HOURS = {
    "algebra": 136,
    "geometry": 102,
    "probability_statistics": 34,
}

matrix_paths = sorted(MATRIX_DIR.glob("*.csv"))
actual_names = {path.name for path in matrix_paths}
if actual_names != EXPECTED_MATRICES:
    missing = sorted(EXPECTED_MATRICES - actual_names)
    extra = sorted(actual_names - EXPECTED_MATRICES)
    raise SystemExit(f"matrix set mismatch: missing={missing}, extra={extra}")

seen_capabilities: dict[str, Path] = {}
counts: list[str] = []
total = 0

for matrix_path in matrix_paths:
    with matrix_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = set(reader.fieldnames or [])
        if fieldnames != REQUIRED_COLUMNS:
            raise SystemExit(
                f"{matrix_path.name}: expected columns {sorted(REQUIRED_COLUMNS)}, "
                f"got {sorted(fieldnames)}"
            )
        rows = list(reader)

    if not rows:
        raise SystemExit(f"{matrix_path.name} is empty")

    for line_number, row in enumerate(rows, start=2):
        capability = row["capability"].strip()
        if not capability:
            raise SystemExit(f"{matrix_path.name}:{line_number}: empty capability")
        if capability in seen_capabilities:
            previous = seen_capabilities[capability]
            raise SystemExit(
                f"{matrix_path.name}:{line_number}: duplicate capability "
                f"{capability!r}, already in {previous.name}"
            )
        seen_capabilities[capability] = matrix_path

        status = row["status"]
        if status not in ALLOWED:
            raise SystemExit(
                f"{matrix_path.name}:{line_number}: invalid status {status!r}"
            )
        try:
            level = int(row["level"])
        except ValueError as exc:
            raise SystemExit(
                f"{matrix_path.name}:{line_number}: level must be an integer"
            ) from exc
        if not (0 <= level <= 4):
            raise SystemExit(
                f"{matrix_path.name}:{line_number}: level must be between 0 and 4"
            )
        if not row["evidence"].strip() or not row["next_gate"].strip():
            raise SystemExit(
                f"{matrix_path.name}:{line_number}: evidence and next_gate are required"
            )

    total += len(rows)
    counts.append(f"{matrix_path.stem}={len(rows)}")

matrix_summary = (
    f"OK: {total} capabilities across 3 matrices ({', '.join(counts)})"
)

with CURRICULUM_PATH.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = set(reader.fieldnames or [])
    if fieldnames != CURRICULUM_COLUMNS:
        raise SystemExit(
            "advanced_grade7.csv: expected columns "
            f"{sorted(CURRICULUM_COLUMNS)}, got {sorted(fieldnames)}"
        )
    curriculum_rows = list(reader)

hours_by_domain = {domain: 0 for domain in EXPECTED_HOURS}
sequences_by_domain = {domain: [] for domain in EXPECTED_HOURS}

for line_number, row in enumerate(curriculum_rows, start=2):
    domain = row["domain"]
    if domain not in EXPECTED_HOURS:
        raise SystemExit(
            f"advanced_grade7.csv:{line_number}: invalid domain {domain!r}"
        )
    try:
        sequence = int(row["sequence"])
        hours = int(row["hours"])
    except ValueError as exc:
        raise SystemExit(
            f"advanced_grade7.csv:{line_number}: sequence and hours must be integers"
        ) from exc
    if sequence < 1 or hours < 1:
        raise SystemExit(
            f"advanced_grade7.csv:{line_number}: sequence and hours must be positive"
        )
    if not row["unit"].strip():
        raise SystemExit(f"advanced_grade7.csv:{line_number}: empty unit")

    capabilities = [
        item.strip() for item in row["capabilities"].split(";") if item.strip()
    ]
    if not capabilities:
        raise SystemExit(
            f"advanced_grade7.csv:{line_number}: no capabilities assigned"
        )
    for capability in capabilities:
        matrix_path = seen_capabilities.get(capability)
        if matrix_path is None:
            raise SystemExit(
                f"advanced_grade7.csv:{line_number}: unknown capability "
                f"{capability!r}"
            )
        expected_matrix = f"{domain}.csv"
        if matrix_path.name != expected_matrix:
            raise SystemExit(
                f"advanced_grade7.csv:{line_number}: {capability!r} belongs to "
                f"{matrix_path.name}, expected {expected_matrix}"
            )

    hours_by_domain[domain] += hours
    sequences_by_domain[domain].append(sequence)

for domain, expected_hours in EXPECTED_HOURS.items():
    actual_hours = hours_by_domain[domain]
    if actual_hours != expected_hours:
        raise SystemExit(
            f"advanced_grade7.csv: {domain} has {actual_hours} hours, "
            f"expected {expected_hours}"
        )
    sequences = sorted(sequences_by_domain[domain])
    expected_sequences = list(range(1, len(sequences) + 1))
    if sequences != expected_sequences:
        raise SystemExit(
            f"advanced_grade7.csv: {domain} sequences must be contiguous from 1, "
            f"got {sequences}"
        )

print(matrix_summary)
print(
    "OK: advanced grade 7 curriculum "
    "(algebra=136h, geometry=102h, probability_statistics=34h)"
)
