"""Full ETL pipeline orchestrator for NASA Planetary Defense datasets.

Stages:
    1. Extract — load both raw CSVs with column renames applied
    2. Clean   — apply dataset-specific cleaning + derived columns
    3. Save    — write all 2 analysis-ready CSVs to data/processed/

Usage:
    python scripts/05_final_load_prep.py
    python scripts/05_final_load_prep.py --raw-dir data/raw --processed-dir data/processed
    python scripts/05_final_load_prep.py --summary-json reports/pipeline_summary.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Handle both module and direct execution
import importlib
try:
    # If run as module (python -m scripts.05_final_load_prep)
    cleaning = importlib.import_module(".02_cleaning", package="scripts")
    etl_pipeline = importlib.import_module(".01_extraction", package="scripts")
except ImportError:
    # If run directly (python scripts/05_final_load_prep.py)
    cleaning = importlib.import_module("02_cleaning")
    etl_pipeline = importlib.import_module("01_extraction")


def run_full_pipeline(
    raw_dir: Path, processed_dir: Path, verbose: bool = True
) -> dict:
    """Execute the full ETL pipeline: extract → clean → save 2 datasets.

    Args:
        raw_dir:       Path to raw CSV files (data/raw/)
        processed_dir: Path to write cleaned CSVs (data/processed/)
        verbose:       Whether to print progress messages

    Returns:
        Summary dict with row counts, column counts, and file paths.
    """
    raw_dir = Path(raw_dir)
    processed_dir = Path(processed_dir)

    if verbose:
        print("=" * 65)
        print("  NASA Planetary Defense — ETL Pipeline")
        print("  NST DVA Capstone 2")
        print("=" * 65)

    # ------------------------------------------------------------------
    # Stage 1: Extract
    # ------------------------------------------------------------------
    if verbose:
        print("\n[1/2] Extracting & loading raw datasets...")

    close_raw, nea_raw = etl_pipeline.extract_all(raw_dir)

    if verbose:
        print(f"  ✓ Close Approaches: {len(close_raw):,} rows × "
              f"{len(close_raw.columns)} cols")
        print(f"  ✓ NEA Catalogue:    {len(nea_raw):,} rows × "
              f"{len(nea_raw.columns)} cols")
        print(f"\n  Column renames applied:")
        print(f"    NEA  — e.g. H→absolute_magnitude_h, e→orbital_eccentricity,")
        print(f"           a→semi_major_axis_au, i→orbital_inclination_deg,")
        print(f"           q→perihelion_dist_au, ad→aphelion_dist_au,")
        print(f"           per→orbital_period_days, n→mean_motion_deg_per_day")
        print(f"    CLOSE— dist_km→distance_km, v_rel_kmh→velocity_relative_km_h")

    # ------------------------------------------------------------------
    # Stage 2: Clean
    # ------------------------------------------------------------------
    if verbose:
        print("\n[2/2] Cleaning datasets & deriving analysis columns...")

    close_clean, nea_clean = cleaning.clean_all(close_raw, nea_raw)

    if verbose:
        print(f"\n  After cleaning:")
        print(f"    Close Approaches: {len(close_clean):,} rows × "
              f"{len(close_clean.columns)} cols")
        print(f"    NEA Catalogue:    {len(nea_clean):,} rows × "
              f"{len(nea_clean.columns)} cols")
        print(f"\n  Saving 2 processed datasets to: {processed_dir}")

    saved_paths = cleaning.save_cleaned_datasets(close_clean, nea_clean, processed_dir)

    # ------------------------------------------------------------------
    # Summary statistics
    # ------------------------------------------------------------------
    nea_hazardous_count = int(
        nea_clean["is_potentially_hazardous"]
        .astype(str).str.lower().isin(["true", "1"]).sum()
    ) if "is_potentially_hazardous" in nea_clean.columns else 0

    future_count = int(
        close_clean["is_future"].astype(str).str.lower().eq("true").sum()
    ) if "is_future" in close_clean.columns else int(
        (close_clean["approach_year"] >= 2025).sum()
        if "approach_year" in close_clean.columns else 0
    )

    summary = {
        "datasets": {
            "nea_catalogue": {
                "rows": len(nea_clean),
                "columns": len(nea_clean.columns),
                "file": saved_paths.get("nea_catalogue", ""),
            },
            "close_approaches": {
                "rows": len(close_clean),
                "columns": len(close_clean.columns),
                "file": saved_paths.get("close_approaches", ""),
            },
        },
        "nea_hazardous_count": nea_hazardous_count,
        "close_approaches_future_count": future_count,
        "nea_rename_map": etl_pipeline.NEA_RENAME_MAP,
        "close_rename_map": etl_pipeline.CLOSE_RENAME_MAP,
        "output_dir": str(processed_dir),
    }

    if verbose:
        print("\n" + "=" * 65)
        print("  Pipeline complete ✓")
        print(f"  PHAs in NEA catalogue: {nea_hazardous_count:,}")
        print(f"  Future close approaches (≥2025): {future_count:,}")
        print("=" * 65 + "\n")

    return summary


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Run the full NASA Planetary Defense ETL pipeline.\n"
            "Produces 2 analysis-ready CSVs in data/processed/."
        )
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=Path.cwd() / "data" / "raw",
        help="Path to raw data directory (default: ./data/raw)",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=Path.cwd() / "data" / "processed",
        help="Path to output processed data directory (default: ./data/processed)",
    )
    parser.add_argument(
        "--no-verbose",
        action="store_true",
        help="Suppress progress messages",
    )
    parser.add_argument(
        "--summary-json",
        type=Path,
        help="Path to save JSON pipeline summary (optional)",
    )
    return parser.parse_args()


def main() -> None:
    """CLI entry point."""
    args = parse_args()
    summary = run_full_pipeline(
        args.raw_dir, args.processed_dir, verbose=not args.no_verbose
    )

    if args.summary_json:
        args.summary_json.parent.mkdir(parents=True, exist_ok=True)
        with open(args.summary_json, "w") as f:
            json.dump(summary, f, indent=2, default=str)
        print(f"Pipeline summary saved to: {args.summary_json}")


if __name__ == "__main__":
    main()
