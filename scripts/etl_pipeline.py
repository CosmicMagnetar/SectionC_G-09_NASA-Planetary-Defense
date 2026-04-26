"""Starter ETL pipeline for NST DVA Capstone 2.

This script is intentionally lightweight. Teams should adapt it to their own dataset,
but it provides a clean starting point for loading a raw CSV, standardizing columns,
and exporting a processed file for notebook and Tableau use.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Tuple

import pandas as pd


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert column names to a clean snake_case format."""
    cleaned = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    result = df.copy()
    result.columns = cleaned
    return result


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    """Apply a few safe default cleaning steps."""
    result = normalize_columns(df)
    result = result.drop_duplicates().reset_index(drop=True)

    for column in result.select_dtypes(include="object").columns:
        result[column] = result[column].astype("string").str.strip()

    return result


def build_clean_dataset(input_path: Path) -> pd.DataFrame:
    """Read a raw CSV file and return a cleaned dataframe."""
    df = pd.read_csv(input_path)
    return basic_clean(df)


def save_processed(df: pd.DataFrame, output_path: Path) -> None:
    """Write the cleaned dataframe to disk, creating the parent folder if needed."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Capstone 2 starter ETL pipeline.")
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Path to the raw CSV file in data/raw/.",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Path to the cleaned CSV file in data/processed/.",
    )
    return parser.parse_args()


def load_asteroid_close_approaches(raw_dir: Path) -> pd.DataFrame:
    """Load asteroid close approaches data from raw directory."""
    file_path = raw_dir / "asteroid_close_approaches_2015_2035.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(file_path)


def load_near_earth_asteroids(raw_dir: Path) -> pd.DataFrame:
    """Load near-earth asteroids data with mixed-type handling."""
    file_path = raw_dir / "near_earth_asteroids_2025.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(file_path, low_memory=False, dtype={"pdes": "string"})


def extract_all(raw_dir: Path) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load both raw datasets. Returns (close_approaches, near_earth_asteroids)."""
    close = load_asteroid_close_approaches(raw_dir)
    nea = load_near_earth_asteroids(raw_dir)
    return close, nea


def main() -> None:
    args = parse_args()
    cleaned_df = build_clean_dataset(args.input)
    save_processed(cleaned_df, args.output)
    print(f"Processed dataset saved to: {args.output}")
    print(f"Rows: {len(cleaned_df)} | Columns: {len(cleaned_df.columns)}")


if __name__ == "__main__":
    main()
