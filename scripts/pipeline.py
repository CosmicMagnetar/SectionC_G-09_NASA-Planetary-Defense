"""Full ETL pipeline orchestrator for asteroid datasets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Handle both module and direct execution
try:
    from . import cleaning, etl_pipeline
except ImportError:
    import cleaning, etl_pipeline


def run_full_pipeline(raw_dir: Path, processed_dir: Path, verbose: bool = True) -> dict:
    """Execute ETL pipeline: extract raw data and clean into processed datasets.

    Returns a dict with file paths.
    """
    raw_dir = Path(raw_dir)
    processed_dir = Path(processed_dir)

    if verbose:
        print("=" * 60)
        print("NASA Asteroid ETL Pipeline")
        print("=" * 60)

    # Stage 1: Extract
    if verbose:
        print("\n[1/2] Extracting raw datasets...")
    close_raw, nea_raw = etl_pipeline.extract_all(raw_dir)
    if verbose:
        print(f"  ✓ Loaded {len(close_raw):,} close approaches")
        print(f"  ✓ Loaded {len(nea_raw):,} NEA objects")

    # Stage 2: Clean
    if verbose:
        print("\n[2/2] Cleaning datasets...")
    close_clean, nea_clean = cleaning.clean_all(close_raw, nea_raw)
    cleaning.save_cleaned_datasets(close_clean, nea_clean, processed_dir)

    if verbose:
        print("\n" + "=" * 60)
        print("Pipeline complete! ✓")
        print("=" * 60)

    return {
        "files": {
            "close_approaches_clean": str(processed_dir / "close_approaches_clean.csv"),
            "near_earth_asteroids_clean": str(processed_dir / "near_earth_asteroids_clean.csv"),
        },
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run the full NASA asteroid analysis pipeline (extract → clean → analyze → Tableau prep)"
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
        help="Path to save JSON summary of analysis results (optional)",
    )
    return parser.parse_args()


def main() -> None:
    """CLI entry point."""
    args = parse_args()
    results = run_full_pipeline(args.raw_dir, args.processed_dir, verbose=not args.no_verbose)

    if args.summary_json:
        summary_json = {
            "close_summary": results["close_summary"],
            "nea_summary": results["nea_summary"],
            "cross_summary": results["cross_summary"],
            "test_results": results["test_results"],
        }
        with open(args.summary_json, "w") as f:
            json.dump(summary_json, f, indent=2, default=str)
        print(f"\nAnalysis summary saved to: {args.summary_json}")


if __name__ == "__main__":
    main()
