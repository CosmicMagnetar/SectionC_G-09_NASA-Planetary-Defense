# Portfolio Case Study — Harshil
## NASA Planetary Defense: Asteroid Risk & Close Approach Analysis

**NST DVA Capstone 2 · SectionC_G-09**
**Role:** Statistical Analysis Lead · Report Author
**Live Dashboard:** [Tableau Public](https://tableaupublic.com) _(paste URL)_
**Repository:** [GitHub](https://github.com) _(paste URL)_

---

## Problem Statement

Identifying which asteroids are "dangerous" requires more than intuition — it requires statistical validation. This project applied rigorous non-parametric hypothesis testing to confirm that Potentially Hazardous Asteroids (PHAs) differ significantly from non-PHAs on every key orbital and physical metric, and to quantify the strength of correlations between orbital parameters.

---

## My Role

As **Statistical Analysis Lead and Report Author**, I was responsible for:

- Designing and executing all statistical tests in `notebooks/04_statistical_analysis.ipynb`
- Building the orbital parameter correlation matrix (9 × 9)
- Running Mann-Whitney U tests for PHA vs non-PHA comparison on 6 key metrics
- Interpreting results in business/decision language (not just p-values)
- Writing the full `reports/project_report.md` — all 13 sections with real findings
- Authoring the KPI framework section with formula definitions

---

## Statistical Methods Applied

### Mann-Whitney U Test (non-parametric)
Chosen because orbital parameter distributions are highly non-normal (right-skewed, multi-modal). The Mann-Whitney U test compares rank distributions without normality assumption.

**Tested comparisons: PHA vs Non-PHA**

| Metric | PHA Mean | Non-PHA Mean | p-value | Finding |
|---|---|---|---|---|
| `absolute_magnitude_h` | lower | higher | < 0.001 | PHAs are significantly larger |
| `min_orbit_intersection_dist_au` | lower | higher | < 0.001 | PHAs orbit significantly closer to Earth |
| `orbital_eccentricity` | higher | lower | < 0.001 | PHAs have more elliptical orbits |
| `semi_major_axis_au` | lower | higher | < 0.001 | PHAs have smaller orbits |
| `orbital_inclination_deg` | lower | higher | < 0.01 | PHAs are more coplanar with ecliptic |
| `observation_span_years` | higher | lower | < 0.001 | PHAs are better tracked |

All 6 tests significant — confirming PHAs occupy a statistically distinct orbital regime.

### Correlation Matrix

**Key correlations (NEA orbital parameters):**
- `semi_major_axis_au` vs `mean_motion_deg_per_day`: **r = −0.97** ← Kepler's Third Law verified
- `perihelion_dist_au` vs `semi_major_axis_au`: **r = +0.89**
- `orbital_eccentricity` vs `min_orbit_intersection_dist_au`: **r = −0.41** (higher eccentricity → closer Earth approach)
- `orbital_period_years` vs `semi_major_axis_au`: **r = +0.98** ← Kepler's Third Law

### Close Approach Variable Correlations
- Distance metrics (AU, km, lunar) are perfectly correlated (different units, same measurement)
- Velocity metrics (`velocity_km_s`, `velocity_relative_km_h`, `velocity_infinity_km_s`) are highly correlated

---

## KPI Framework Authored

| KPI | Formula | Rationale |
|---|---|---|
| PHA Count | `COUNT WHERE is_potentially_hazardous = True` | Primary safety metric |
| Critical PHA Count | `COUNT WHERE risk_tier = 'Critical'` | Immediate priority flag |
| Median MOID | `MEDIAN(min_orbit_intersection_dist_au)` | Robust central tendency for skewed distribution |
| Median Velocity | `MEDIAN(velocity_km_s)` | Representative approach speed |
| Very Close Approach Rate | `COUNT WHERE distance_lunar_distances < 10` | Operational monitoring threshold |

---

## Report Sections Authored

- Executive Summary
- Sector & Business Context
- Statistical Analysis (Section 8)
- Key Insights (all 10)
- Recommendations (all 4 with impact estimates)
- Limitations & Next Steps
- Contribution Matrix

---

## Skills Demonstrated

`scipy.stats` · `Mann-Whitney U` · `Correlation Analysis` · `Seaborn Heatmaps`
`Statistical Interpretation` · `Business Writing` · `KPI Design` · `Jupyter Notebooks` · `GitHub`

---

## What I Learned

The most important lesson from the statistical analysis: a p-value alone is not an insight. Every test result had to be translated into a decision-relevant statement. "PHAs have statistically significantly lower MOID (p < 0.001)" becomes "MOID alone can pre-screen 94% of the catalogue as low-risk, allowing observation resources to focus on the remaining 6%." That translation — from statistics to decision language — is what separates analysis from analytics.
