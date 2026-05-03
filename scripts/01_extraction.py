"""ETL pipeline for NASA Planetary Defense — NST DVA Capstone 2.

Handles loading, column normalization, and proper full-name renaming for:
  - asteroid_close_approaches_2015_2035.csv
  - near_earth_asteroids_2025.csv

Abbreviated JPL column names (H, e, a, i, q, ad, per, n, etc.) are mapped
to fully descriptive snake_case names for analysis and Tableau clarity.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Tuple

import pandas as pd

# ---------------------------------------------------------------------------
# Column rename maps  (raw name → fully descriptive name)
# ---------------------------------------------------------------------------

# Near-Earth Asteroids — JPL SBDB abbreviated orbital & physical fields
NEA_RENAME_MAP: dict[str, str] = {
    # Identifiers
    "spkid": "spk_id",
    "pdes": "primary_designation",
    "pha": "is_potentially_hazardous",
    # Physical properties
    "H": "absolute_magnitude_h",
    "rot_per": "rotation_period_hours",
    # Orbital elements
    "e": "orbital_eccentricity",
    "a": "semi_major_axis_au",
    "i": "orbital_inclination_deg",
    "q": "perihelion_dist_au",
    "ad": "aphelion_dist_au",
    "per": "orbital_period_days",
    "per_y": "orbital_period_years",
    "n": "mean_motion_deg_per_day",
    # MOID (Minimum Orbit Intersection Distance)
    "moid_au": "min_orbit_intersection_dist_au",
    "moid_km": "min_orbit_intersection_dist_km",
    "moid_lunar_distances": "moid_lunar_distances",
    # Observation metadata
    "data_arc": "data_arc_days",
    "condition_code": "orbital_condition_code",
}

# Close Approaches — rename ambiguous/abbreviated fields
CLOSE_RENAME_MAP: dict[str, str] = {
    "dist_km": "distance_km",
    "dist_lunar": "distance_lunar_distances",
    "v_rel_kmh": "velocity_relative_km_h",
}


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert column names to a clean snake_case format (lowercase, underscores)."""
    cleaned = (
        df.columns.str.strip()
        .str.replace(r"[^a-zA-Z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    result = df.copy()
    result.columns = cleaned
    return result


def apply_rename_map(df: pd.DataFrame, rename_map: dict[str, str]) -> pd.DataFrame:
    """Apply a rename map to a dataframe, only renaming columns that exist."""
    existing = {k: v for k, v in rename_map.items() if k in df.columns}
    return df.rename(columns=existing)


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    """Apply safe default cleaning: normalize columns, drop duplicates, strip strings."""
    result = normalize_columns(df)
    result = result.drop_duplicates().reset_index(drop=True)
    for column in result.select_dtypes(include="object").columns:
        result[column] = result[column].astype("string").str.strip()
    return result


def build_clean_dataset(input_path: Path) -> pd.DataFrame:
    """Read a raw CSV file and return a cleaned dataframe (no rename maps applied)."""
    df = pd.read_csv(input_path)
    return basic_clean(df)


def save_processed(df: pd.DataFrame, output_path: Path) -> None:
    """Write the cleaned dataframe to disk, creating the parent folder if needed."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


# ---------------------------------------------------------------------------
# Dataset-specific loaders
# ---------------------------------------------------------------------------


def load_asteroid_close_approaches(raw_dir: Path) -> pd.DataFrame:
    """Load the raw close approaches CSV and apply close-approach rename map.

    Returns a dataframe with fully descriptive column names.
    """
    file_path = Path(raw_dir) / "asteroid_close_approaches_2015_2035.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    df = pd.read_csv(file_path)
    return apply_rename_map(df, CLOSE_RENAME_MAP)


def load_near_earth_asteroids(raw_dir: Path) -> pd.DataFrame:
    """Load the raw NEA catalogue and apply the NEA rename map.

    Uses low_memory=False to handle mixed-type columns.
    Returns a dataframe with fully descriptive column names.
    """
    file_path = Path(raw_dir) / "near_earth_asteroids_2025.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    df = pd.read_csv(file_path, low_memory=False)
    return apply_rename_map(df, NEA_RENAME_MAP)


def extract_all(raw_dir: Path) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load both raw datasets with renames applied.

    Returns:
        (close_approaches_df, near_earth_asteroids_df)
    """
    close = load_asteroid_close_approaches(raw_dir)
    nea = load_near_earth_asteroids(raw_dir)
    return close, nea


# ---------------------------------------------------------------------------
# CLI (single-file mode, for quick one-off cleaning)
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a single-file ETL pass (load → clean → save)."
    )
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


def main() -> None:
    args = parse_args()
    cleaned_df = build_clean_dataset(args.input)
    save_processed(cleaned_df, args.output)
    print(f"Processed dataset saved to: {args.output}")
    print(f"Rows: {len(cleaned_df):,} | Columns: {len(cleaned_df.columns)}")


if __name__ == "__main__":
    main()
