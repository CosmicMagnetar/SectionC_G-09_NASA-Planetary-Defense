# Project Report — NASA Planetary Defense
## Asteroid Risk & Close Approach Analysis

**Newton School of Technology | DVA Capstone 2**
**Team:** SectionC_G-09 | **Section:** C
**Members:** Aditya Rana · Aanya Mehrotra · Pihu Jaitly · Harshil
**Faculty Mentor:** _[Faculty Mentor Name]_
**Submission Date:** _[Submission Date]_

---

## 1. Executive Summary

This project applies data analytics to NASA/JPL's asteroid catalogue and close approach datasets to build a planetary defense intelligence dashboard. Using Python-based ETL, statistical analysis, and Tableau visualisation, the team processed 41,150 Near-Earth Asteroid (NEA) records and 27,430 close approach events spanning 2015–2035.

**Key findings:**
- 2,539 asteroids (6.2%) are classified as Potentially Hazardous (PHAs)
- Minimum Orbit Intersection Distance (MOID) is the statistically strongest predictor of hazard classification (Mann-Whitney U p < 0.001)
- Apollo-class asteroids dominate the PHA pool
- 3,888 close approaches are forecast between 2025 and 2035
- Diameter and physical data are missing for 80%+ of small NEAs, making H magnitude the only reliable size proxy

**Key recommendations:**
1. Prioritise radar observation for Critical-tier PHAs (MOID < 0.01 AU)
2. Fund space-based infrared surveys to characterise small NEA sizes
3. Implement automated 10 Lunar Distance alert triggers
4. Focus deflection planning on the Apollo-class PHA population

---

## 2. Sector & Business Context

**Sector:** Space & Planetary Science / Public Safety

Planetary defense is the applied science of detecting, tracking, and if necessary deflecting near-Earth objects (NEOs) that could collide with Earth. It is a genuine public-safety discipline supported by NASA, ESA, and international observatories. The 2021 DART mission — which successfully deflected asteroid Dimorphos — demonstrated that data-driven planetary defense is no longer theoretical.

**Decision-maker:** NASA's Planetary Defense Coordination Office (PDCO), observatory directors allocating telescope time, and science policy bodies funding NEO survey missions.

**Why this matters:** A 140-metre asteroid impact would devastate an area the size of a major city. A 1-km impactor would trigger a global climate catastrophe. Real-time analytical dashboards allow limited observation resources to be allocated toward the highest-risk objects, and communicate risk to legislators and the public in a clear, data-backed format.

---

## 3. Problem Statement & Objectives

**Formal problem:** The raw NASA/JPL asteroid datasets contain cryptic abbreviated column names, no pre-computed risk tiers, and require significant transformation before they are usable by a non-specialist analyst or Tableau dashboard.

**Scope:** The project covers:
- Full ETL of two raw NASA/JPL CSV datasets
- Column renaming and descriptive naming for all 29+ orbital/physical fields
- Derivation of risk tier, speed category, orbit class label, and observation span
- Production of 2 analysis-ready datasets
- Interactive Streamlit application
- 4 separate Tableau dashboards covering analytical views

**Success criteria:**
- All abbreviated column names replaced with fully descriptive names
- 2 separate processed datasets produced and validated
- 4 Tableau dashboards published with at least 3 interactive filters
- 10 data-backed insights delivered in decision language
- 4 actionable recommendations with impact estimates

---

## 4. Data Description

### Dataset 1: NEA Catalogue (`near_earth_asteroids_2025.csv`)

- **Source:** NASA JPL Small Body Database — https://ssd.jpl.nasa.gov/tools/sbdb_query.html
- **Raw shape:** 41,281 rows × 29 columns
- **Cleaned shape:** 41,150 rows × 33 columns
- **Granularity:** One row per unique asteroid
- **Coverage:** All known Near-Earth Asteroids as of the 2025 snapshot

**Key quality issues in raw data:**
- Abbreviated column names (`H`, `e`, `a`, `i`, `q`, `ad`, `per`, `n`) are standard orbital mechanics notation but opaque for general analysis
- `diameter_km` and `albedo` null for ~80% of small objects
- `rot_per` (rotation period) null for most objects
- `moid_au` null for a small fraction — these rows dropped (131 records)

### Dataset 2: Close Approaches (`asteroid_close_approaches_2015_2035.csv`)

- **Source:** NASA CNEOS — https://cneos.jpl.nasa.gov/ca/
- **Raw shape:** 27,430 rows × 13 columns
- **Cleaned shape:** 27,430 rows × 19 columns
- **Granularity:** One row per close approach event
- **Coverage:** All Earth close approaches from 2015 to 2035

**Key quality issues:**
- `dist_km`, `dist_lunar`, `v_rel_kmh` are abbreviated — renamed to descriptive names
- `velocity_infinity_km_s` has nulls — imputed from `velocity_km_s`
- `absolute_magnitude` has minor nulls — imputed with column median

---

## 5. Cleaning & Transformation

### ETL Architecture

The pipeline is implemented across three Python modules:
- `scripts/01_extraction.py` — loaders, rename maps, normalization
- `scripts/02_cleaning.py` — dataset-specific cleaning, derived columns, output
- `scripts/05_final_load_prep.py` — CLI orchestrator

Run the full pipeline:
```bash
python scripts/05_final_load_prep.py
```

### Column Rename Map (NEA Dataset)

| Original | Renamed To |
|---|---|
| `H` | `absolute_magnitude_h` |
| `e` | `orbital_eccentricity` |
| `a` | `semi_major_axis_au` |
| `i` | `orbital_inclination_deg` |
| `q` | `perihelion_dist_au` |
| `ad` | `aphelion_dist_au` |
| `per` | `orbital_period_days` |
| `per_y` | `orbital_period_years` |
| `n` | `mean_motion_deg_per_day` |
| `rot_per` | `rotation_period_hours` |
| `pha` | `is_potentially_hazardous` |
| `spkid` | `spk_id` |
| `pdes` | `primary_designation` |
| `moid_au` | `min_orbit_intersection_dist_au` |
| `moid_km` | `min_orbit_intersection_dist_km` |
| `condition_code` | `orbital_condition_code` |
| `data_arc` | `data_arc_days` |

### Derived Columns

| Column | Logic | Purpose |
|---|---|---|
| `risk_tier` | PHA + MOID thresholds → Critical/High/Moderate/Low | Dashboard traffic light |
| `orbit_class_label` | Mapped from JPL class codes | Human-readable filter |
| `is_named` | `name` is not null | Named vs unnamed filter |
| `observation_span_years` | `(last_obs - first_obs).days / 365.25` | Data quality KPI |
| `speed_category` | Binned on `velocity_km_s` | Dashboard colour coding |
| `is_very_close_approach` | `distance_lunar_distances < 10` | High-risk event flag |
| `approach_year/month/day_of_week` | From `close_approach_date` | Temporal grouping |

### Two Output Datasets

| File | Rows | Cols | Purpose |
|---|---|---|---|
| `nea_catalogue_clean.csv` | 41,150 | 33 | Full orbital analysis & Hazard tracking |
| `close_approaches_clean.csv` | 27,430 | 19 | Timeline & velocity analysis |

---

## 6. KPI Framework

| KPI | Definition | Value (from pipeline) |
|---|---|---|
| Total NEAs | All known NEAs in 2025 snapshot | 41,150 |
| PHA Count | is_potentially_hazardous = True | 2,539 |
| PHA Rate | PHAs as % of all NEAs | 6.17% |
| Critical PHAs | risk_tier = 'Critical' (MOID < 0.01 AU) | computed in Tableau |
| Future Close Approaches | approach_year ≥ 2025 | 3,888 |
| Very Close Approaches | distance_lunar_distances < 10 | computed in Tableau |
| Median Approach Velocity | MEDIAN(velocity_km_s) | ~12–14 km/s |
| Median MOID (all) | MEDIAN(min_orbit_intersection_dist_au) | computed in Tableau |
| Median MOID (PHAs) | MEDIAN on PHA subset | computed in Tableau |

---

## 7. Exploratory Analysis

### Physical Properties
- Absolute magnitude H is right-skewed: most NEAs cluster at H = 20–26 (small objects)
- Diameter data available for only ~20% of the catalogue — for the rest, H is the size proxy
- Size category "Small (<140m)" dominates; "Large (>1km) — City killer+" objects are rare but well-tracked

### Orbit Classes
- **Apollo** class (Earth-crossing, semi-major axis > 1 AU) is the largest group (~60% of NEAs)
- **Amor** class (Earth-approaching, outside orbit) is second largest
- **Aten** class (Earth-crossing, semi-major axis < 1 AU) has the highest PHA density

### Orbital Parameter Patterns
- Strong negative correlation between `semi_major_axis_au` and `mean_motion_deg_per_day` (Kepler's Third Law)
- Strong positive correlation between `perihelion_dist_au` and `semi_major_axis_au`
- `orbital_eccentricity` clusters between 0.1–0.6 for most NEAs

### Close Approach Patterns
- Annual approach count is consistent across 2015–2035, confirming prediction completeness
- Velocity distribution peaks at 10–20 km/s; tail extends to 40+ km/s for high-eccentricity objects
- Approximately 65% of approaches fall in the "Moderate (5–15 km/s)" speed category

---

## 8. Statistical Analysis

### Methodology
Mann-Whitney U tests (non-parametric, appropriate for non-normal distributions) were used to compare PHA vs non-PHA populations on key metrics.

### Results

| Metric | PHA Mean | Non-PHA Mean | p-value | Significant? |
|---|---|---|---|---|
| Absolute Magnitude H | lower | higher | < 0.001 | ✓ Yes — PHAs are larger |
| MOID (AU) | lower | higher | < 0.001 | ✓ Yes — PHAs orbit closer |
| Orbital Eccentricity | higher | lower | < 0.001 | ✓ Yes — PHAs have more elliptical orbits |
| Semi-Major Axis (AU) | lower | higher | < 0.001 | ✓ Yes — PHAs orbit closer to Sun |
| Orbital Inclination | lower | higher | < 0.01 | ✓ Yes — PHAs more coplanar with ecliptic |
| Observation Span (years) | higher | lower | < 0.001 | ✓ Yes — PHAs are better observed |

**Correlation findings:**
- `semi_major_axis_au` vs `mean_motion_deg_per_day`: r = −0.97 (Kepler's Third Law verified)
- `perihelion_dist_au` vs `semi_major_axis_au`: r = +0.89
- `orbital_eccentricity` vs `min_orbit_intersection_dist_au`: r = −0.41 (higher eccentricity → lower MOID)

---

## 9. Dashboard Walkthrough

The 4 Tableau dashboards are published at: `[PASTE TABLEAU PUBLIC URLS HERE]`
A Streamlit dashboard is also provided via `streamlit/app.py`.

**Executive View (Dashboard 1):**
- KPI banner: Total NEAs · PHA Count · Critical PHAs · Median MOID
- Risk Tier horizontal bar chart (colour-coded Critical/High/Moderate/Low)
- Orbit Class treemap

**Operational Views (Dashboards 2-4):**
- MOID distribution histogram with 0.05 AU PHA threshold reference line
- Orbital Eccentricity vs Semi-Major Axis scatter (PHAs in red)
- Annual Close Approach timeline (2015–2035) with 2025 reference
- Future Approaches scatter: Date vs Distance, coloured by speed category

**Interactive Filters:**
- Risk Tier (multi-select)
- Orbit Class (multi-select)
- Size Category (multi-select)
- Approach Year (range slider)
- Speed Category (multi-select)
- Very Close Approach only (toggle)

---

## 10. Key Insights

1. **2,539 PHAs identified (6.2% of catalogue)** — a manageable but critical subset for targeted monitoring.
2. **MOID is the strongest hazard predictor** — statistically separates PHAs from non-PHAs (p < 0.001). MOID alone can pre-screen 94% of the catalogue as low-risk.
3. **PHAs are systematically larger** — significantly lower H magnitude confirms they are more detectable by size, yet still include objects too small to physically characterise.
4. **Apollo-class objects dominate the PHA pool** — this is the highest-priority orbit class for deflection planning.
5. **Median approach velocity ≈ 12–14 km/s** — at this speed, a 140m object would release energy equivalent to hundreds of nuclear warheads.
6. **3,888 future close approaches predicted (2025–2035)** — data completeness is consistent; no alarming spike in predicted events.
7. **Very close approaches (< 10 Lunar Distances) occur regularly** — these require dedicated radar observation campaigns.
8. **80%+ of NEAs have no physical size data** — the catalogue's completeness for threat assessment is significantly limited for small objects.
9. **Orbit condition codes are predominantly 0** — well-established objects have high orbital certainty; newly discovered objects carry significant uncertainty.
10. **Long-arc observations (50+ years) exist for major NEAs** — demonstrating the value of sustained, multi-decade tracking programs.

---

## 11. Recommendations

| # | Recommendation | Expected Impact |
|---|---|---|
| 1 | Prioritise Goldstone/Arecibo-class radar time for all Critical-tier PHAs (MOID < 0.01 AU) | Reduces orbital uncertainty, improving impact probability estimates from ±years to ±days |
| 2 | Fund NEO Surveyor (space-based IR mission) to characterise physical properties of uncatalogued small NEAs | Unlocks threat assessment for the 80% of objects with no diameter or albedo data |
| 3 | Implement automated 10 Lunar Distance alert triggers in CNEOS tracking systems | Reduces response time for emergency observation campaigns from weeks to hours |
| 4 | Focus kinetic impactor and deflection planning on Apollo-class PHA population | Apollo-class objects are both the most numerous PHAs and the most accessible for spacecraft rendezvous |

---

## 12. Limitations & Next Steps

**Data limitations:**
- Physical data (diameter, albedo, rotation period) missing for ~80% of small NEAs
- Close approach data limited to 2035 — longer-horizon predictions have higher orbital uncertainty
- MOID is a static orbital metric; actual impact probability requires full Monte Carlo propagation (not done here)

**Method limitations:**
- Mann-Whitney tests assess statistical significance but not effect size — Cohen's d analysis would add depth
- Risk tier thresholds (MOID < 0.01 = Critical) are team-defined, not official NASA classifications
- No time-series forecasting model built for approach frequency trends

**Next steps:**
- Integrate JPL Sentry impact probability data for individual objects
- Build a machine learning classifier (Random Forest) on PHA vs non-PHA features
- Add spectral type data to distinguish rocky from metallic objects
- Extend close approach timeline to 2050 using orbital propagation

---

## 13. Contribution Matrix

| Team Member | Data & ETL | EDA | Stats | Tableau | Report | PPT |
|---|---|---|---|---|---|---|
| Aditya Rana | Owner | Support | Support | Support | Support | Support |
| Aanya Mehrotra | Support | Owner | Support | Support | Support | Support |
| Pihu Jaitly | Support | Support | Support | Owner | Support | Owner |
| Harshil | Support | Support | Owner | Support | Owner | Support |

_We confirm that the above contribution details are accurate and verifiable through GitHub Insights, PR history, and submitted artifacts._

**Team Lead:** Aditya Rana
**Date:** _[Submission Date]_

---

> **Export instructions:** Print this file to PDF using browser (File → Print → Save as PDF) or run:
> ```bash
> pandoc reports/project_report.md -o reports/project_report.pdf
> ```

*Newton School of Technology · DVA Capstone 2 · SectionC_G-09*
