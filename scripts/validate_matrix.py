#!/usr/bin/env python3
"""Small sanity check for capability_matrix.csv."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "capability_matrix.csv"
ALLOWED = {"PASS", "WATCH", "TRAIN", "NEW"}

with MATRIX.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

if not rows:
    raise SystemExit("capability_matrix.csv is empty")

for i, row in enumerate(rows, start=2):
    status = row.get("status", "")
    if status not in ALLOWED:
        raise SystemExit(f"line {i}: invalid status {status!r}")
    try:
        level = int(row.get("level", ""))
    except ValueError as exc:
        raise SystemExit(f"line {i}: level must be an integer") from exc
    if not (0 <= level <= 4):
        raise SystemExit(f"line {i}: level must be between 0 and 4")

print(f"OK: {len(rows)} capabilities")
