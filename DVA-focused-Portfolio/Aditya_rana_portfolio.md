# Portfolio Case Study — Aditya Rana
## NASA Planetary Defense: Asteroid Risk & Close Approach Analysis

**NST DVA Capstone 2 · SectionC_G-09**
**Role:** Project Lead · ETL Pipeline Architect
**Live Dashboard:** [Tableau Public](https://tableaupublic.com) _(paste URL)_
**Repository:** [GitHub](https://github.com) _(paste URL)_
**Portfolio:** [https://dva-portfolio-inky-beta.vercel.app/](https://dva-portfolio-inky-beta.vercel.app/)

---

## Problem Statement

NASA's planetary defense mission relies on continuous monitoring of 41,000+ Near-Earth Asteroids. Raw data from JPL's SBDB uses opaque orbital mechanics notation — abbreviations like `H`, `e`, `a`, `q`, `ad`, `per`, `n` — that cannot be used directly in analysis pipelines or stakeholder dashboards. This project built a production-ready ETL system to transform, rename, and enrich both NASA/JPL asteroid datasets into two distinct analysis-ready outputs.

**Business Question:** Which asteroids present the highest near-term risk to Earth, and how do velocity, MOID, and orbital characteristics predict hazard severity?

---

## My Role

As **Project Lead and ETL Pipeline Architect**, I was responsible for:

- Designing the full 3-module Python ETL architecture (`01_extraction.py`, `02_cleaning.py`, `05_final_load_prep.py`)
- Authoring the complete column rename maps for 17 abbreviated JPL fields across both datasets
- Implementing `apply_rename_map()`, `normalize_columns()`, and all dataset loaders
- Defining the 2-dataset output structure and the `risk_tier` derivation logic
- Coordinating notebook standards and team deliverables

---

## Dataset & Scale

| Dataset | Raw Shape | Cleaned Shape |
|---|---|---|
| NEA Catalogue | 41,281 × 29 | 41,150 × 33 |
| Close Approaches | 27,430 × 13 | 27,430 × 19 |

---

## Key Technical Contributions

### Column Rename Map (17 JPL fields → descriptive names)
```python
NEA_RENAME_MAP = {
    'H': 'absolute_magnitude_h',
    'e': 'orbital_eccentricity',
    'a': 'semi_major_axis_au',
    'i': 'orbital_inclination_deg',
    'q': 'perihelion_dist_au',
    'ad': 'aphelion_dist_au',
    'per': 'orbital_period_days',
    'n': 'mean_motion_deg_per_day',
    'pha': 'is_potentially_hazardous',
    # ... 8 more
}
```

### Risk Tier Derivation
```python
def _risk_tier(row) -> str:
    if is_pha and moid < 0.01: return 'Critical'
    if is_pha and moid < 0.05: return 'High'
    if is_pha:                  return 'Moderate'
    return 'Low'
```

### 2-Dataset Pipeline Output
Running `python scripts/05_final_load_prep.py` produces both analysis-ready CSVs in under 30 seconds from raw inputs.

---

## Key Findings from My Analysis

- 2,539 PHAs identified (6.2% of catalogue) — verified by pipeline
- All 17 abbreviated column names successfully renamed across both datasets
- Pipeline runtime: < 30 seconds for 68,000+ total records
- Zero abbreviated column names remain in any processed output (validated in notebook 05)

---

## Skills Demonstrated

`Python` · `pandas` · `ETL Architecture` · `Data Cleaning` · `Column Standardisation`
`Jupyter Notebooks` · `GitHub` · `CLI Scripting` · `Data Dictionary Authoring`

---

## What I Learned

Designing a rename-map-first ETL architecture taught me that column naming is not cosmetic — it directly determines the usability of downstream analysis and dashboard tools. JPL's abbreviated notation is precise for astronomers, but completely opaque for data analytics work. The rename-first approach prevented ambiguity across all 5 notebooks and the Tableau build.
