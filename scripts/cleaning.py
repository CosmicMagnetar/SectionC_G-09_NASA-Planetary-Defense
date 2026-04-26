"""Dataset-specific cleaning for asteroid close approaches and NEA catalogue."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd

# Handle both module and direct execution
try:
    from .etl_pipeline import basic_clean
except ImportError:
    from etl_pipeline import basic_clean


def clean_close_approaches(df: pd.DataFrame) -> pd.DataFrame:
    """Clean asteroid close approaches dataset.

    Transformations:
    - Normalize column names and remove duplicates (via basic_clean)
    - Parse close_approach_date to datetime
    - Impute velocity_infinity_km_s nulls with velocity_km_s
    - Impute absolute_magnitude nulls with column median
    - Add approach_year and approach_month columns
    - Sort chronologically
    """
    result = basic_clean(df)

    result["close_approach_date"] = pd.to_datetime(result["close_approach_date"], errors="coerce")

    result["velocity_infinity_km_s"] = result["velocity_infinity_km_s"].fillna(result["velocity_km_s"])
    result["absolute_magnitude"] = result["absolute_magnitude"].fillna(result["absolute_magnitude"].median())

    result["approach_year"] = result["close_approach_date"].dt.year
    result["approach_month"] = result["close_approach_date"].dt.month

    result = result.sort_values("close_approach_date").reset_index(drop=True)

    return result


def clean_near_earth_asteroids(df: pd.DataFrame) -> pd.DataFrame:
    """Clean near-earth asteroids dataset.

    Transformations:
    - Normalize column names and remove duplicates (via basic_clean)
    - Parse first_obs and last_obs to datetime
    - Drop rows with missing moid_au (critical hazard field)
    - Add is_named column (True if name is not null)
    - Add observation_span_years column (calculated from date range)
    """
    result = basic_clean(df)

    result["first_obs"] = pd.to_datetime(result["first_obs"], errors="coerce")
    result["last_obs"] = pd.to_datetime(result["last_obs"], errors="coerce")

    # Drop rows missing critical MOID field
    before = len(result)
    result = result.dropna(subset=["moid_au"]).reset_index(drop=True)

    # Derived columns useful downstream
    result["is_named"] = result["name"].notna()
    result["observation_span_years"] = (result["last_obs"] - result["first_obs"]).dt.days / 365.25

    return result


def clean_all(close_raw: pd.DataFrame, nea_raw: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Clean both datasets independently. Returns (close_clean, nea_clean)."""
    close_clean = clean_close_approaches(close_raw)
    nea_clean = clean_near_earth_asteroids(nea_raw)
    return close_clean, nea_clean


def save_cleaned_datasets(
    close_clean: pd.DataFrame, nea_clean: pd.DataFrame, output_dir: Path
) -> None:
    """Save both cleaned datasets to CSV files."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    close_path = output_dir / "close_approaches_clean.csv"
    nea_path = output_dir / "near_earth_asteroids_clean.csv"

    close_clean.to_csv(close_path, index=False)
    nea_clean.to_csv(nea_path, index=False)

    print(f"Saved {len(close_clean):,} close approaches -> {close_path}")
    print(f"Saved {len(nea_clean):,} NEA objects -> {nea_path}")
