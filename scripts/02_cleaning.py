"""Dataset-specific cleaning for asteroid close approaches and NEA catalogue.

Produces two analysis-ready CSVs:
  1. nea_catalogue_clean.csv          — Full NEA catalogue (renamed + derived)
  2. close_approaches_clean.csv       — All close approaches (renamed + derived)
"""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd

import importlib

# Handle both module and direct execution
try:
    # If run as module (python -m scripts.02_cleaning)
    extraction = importlib.import_module(".01_extraction", package="scripts")
except ImportError:
    # If run directly
    extraction = importlib.import_module("01_extraction")

basic_clean = extraction.basic_clean
apply_rename_map = extraction.apply_rename_map
NEA_RENAME_MAP = extraction.NEA_RENAME_MAP
CLOSE_RENAME_MAP = extraction.CLOSE_RENAME_MAP


# ---------------------------------------------------------------------------
# Close Approaches cleaning
# ---------------------------------------------------------------------------


def clean_close_approaches(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich the close approaches dataset.

    Transformations applied (in order):
    1. Normalize column names and drop duplicates (via basic_clean)
    2. Apply CLOSE_RENAME_MAP for descriptive column names
    3. Parse close_approach_date to datetime
    4. Impute velocity_infinity_km_s nulls with velocity_km_s
    5. Impute absolute_magnitude nulls with column median
    6. Derive: approach_year, approach_month, approach_day_of_week
    7. Derive: is_close_approach (distance_lunar_distances < 10)
    8. Derive: hazard_speed_category (binned velocity)
    9. Sort chronologically
    """
    result = basic_clean(df)
    # Apply rename map (handles any cols not yet renamed during load)
    result = apply_rename_map(result, CLOSE_RENAME_MAP)

    # --- Date parsing ---
    result["close_approach_date"] = pd.to_datetime(
        result["close_approach_date"], errors="coerce"
    )

    # --- Null imputation ---
    if "velocity_infinity_km_s" in result.columns and "velocity_km_s" in result.columns:
        result["velocity_infinity_km_s"] = result["velocity_infinity_km_s"].fillna(
            result["velocity_km_s"]
        )
    if "absolute_magnitude" in result.columns:
        result["absolute_magnitude"] = result["absolute_magnitude"].fillna(
            result["absolute_magnitude"].median()
        )

    # --- Derived temporal columns ---
    result["approach_year"] = result["close_approach_date"].dt.year
    result["approach_month"] = result["close_approach_date"].dt.month
    result["approach_month_name"] = result["close_approach_date"].dt.strftime("%B")
    result["approach_day_of_week"] = result["close_approach_date"].dt.day_name()

    # --- Derived risk columns ---
    if "distance_lunar_distances" in result.columns:
        result["is_very_close_approach"] = result["distance_lunar_distances"] < 10

    if "velocity_km_s" in result.columns:
        result["speed_category"] = pd.cut(
            result["velocity_km_s"],
            bins=[0, 5, 15, 30, float("inf")],
            labels=["Slow (<5 km/s)", "Moderate (5–15 km/s)",
                    "Fast (15–30 km/s)", "Very Fast (>30 km/s)"],
            right=False,
        ).astype("string")

    result = result.sort_values("close_approach_date").reset_index(drop=True)
    return result


# ---------------------------------------------------------------------------
# NEA Catalogue cleaning
# ---------------------------------------------------------------------------


def clean_near_earth_asteroids(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich the near-earth asteroids catalogue.

    Transformations applied (in order):
    1. Normalize column names and drop duplicates (via basic_clean)
    2. Apply NEA_RENAME_MAP for fully descriptive column names
    3. Parse first_obs and last_obs to datetime
    4. Drop rows missing min_orbit_intersection_dist_au (critical hazard field)
    5. Derive: is_named (True if name is not null)
    6. Derive: observation_span_years
    7. Derive: estimated_diameter_km (midpoint if range not given)
    8. Derive: risk_tier (PHAs classified by MOID and size)
    9. Derive: orbit_type_label (human-readable class expansion)
    """
    result = basic_clean(df)
    # Apply rename map (handles any cols not yet renamed during load)
    result = apply_rename_map(result, NEA_RENAME_MAP)

    # --- Date parsing ---
    result["first_obs"] = pd.to_datetime(result["first_obs"], errors="coerce")
    result["last_obs"] = pd.to_datetime(result["last_obs"], errors="coerce")

    # --- Drop rows missing critical MOID field ---
    result = result.dropna(subset=["min_orbit_intersection_dist_au"]).reset_index(
        drop=True
    )

    # --- Derived columns ---
    result["is_named"] = result["name"].notna()

    result["observation_span_years"] = (
        result["last_obs"] - result["first_obs"]
    ).dt.days / 365.25

    # Hazard risk tier: PHAs with small MOID get highest tier
    if "is_potentially_hazardous" in result.columns and \
       "min_orbit_intersection_dist_au" in result.columns:
        def _risk_tier(row) -> str:
            pha = row.get("is_potentially_hazardous", False)
            moid = row.get("min_orbit_intersection_dist_au", 1.0)
            if pha is True or pha == "True":
                if moid < 0.01:
                    return "Critical"
                elif moid < 0.05:
                    return "High"
                else:
                    return "Moderate"
            else:
                return "Low"
        result["risk_tier"] = result.apply(_risk_tier, axis=1).astype("string")

    # Orbit class human-readable expansion
    orbit_class_labels = {
        "AMO": "Amor (Earth-approaching, outside orbit)",
        "APO": "Apollo (Earth-crossing, semi-major >1 AU)",
        "ATE": "Aten (Earth-crossing, semi-major <1 AU)",
        "IEO": "Interior Earth Object (inside Earth's orbit)",
        "MCA": "Mars-Crossing Asteroid",
        "IMB": "Inner Main Belt",
        "MBA": "Main Belt Asteroid",
        "OMB": "Outer Main Belt",
        "TJN": "Jupiter Trojan",
        "CEN": "Centaur",
        "TNO": "Trans-Neptunian Object",
    }
    if "class" in result.columns:
        result["orbit_class_label"] = (
            result["class"].map(orbit_class_labels).fillna(result["class"])
        ).astype("string")

    return result


# ---------------------------------------------------------------------------
# Orchestrators
# ---------------------------------------------------------------------------


def clean_all(
    close_raw: pd.DataFrame, nea_raw: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Clean both datasets independently. Returns (close_clean, nea_clean)."""
    close_clean = clean_close_approaches(close_raw)
    nea_clean = clean_near_earth_asteroids(nea_raw)
    return close_clean, nea_clean


def save_cleaned_datasets(
    close_clean: pd.DataFrame,
    nea_clean: pd.DataFrame,
    output_dir: Path,
) -> dict[str, str]:
    """Save all two analysis-ready datasets to CSV.

    Outputs:
        nea_catalogue_clean.csv
        close_approaches_clean.csv

    Returns:
        dict mapping dataset name → file path (as strings)
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "nea_catalogue": output_dir / "nea_catalogue_clean.csv",
        "close_approaches": output_dir / "close_approaches_clean.csv",
    }

    # Save two datasets
    nea_clean.to_csv(paths["nea_catalogue"], index=False)
    close_clean.to_csv(paths["close_approaches"], index=False)

    print(f"  ✓ NEA Catalogue       → {paths['nea_catalogue'].name}"
          f"  ({len(nea_clean):,} rows, {len(nea_clean.columns)} cols)")
    print(f"  ✓ Close Approaches    → {paths['close_approaches'].name}"
          f"  ({len(close_clean):,} rows, {len(close_clean.columns)} cols)")

    return {k: str(v) for k, v in paths.items()}
