# Tableau 4-Dashboard Complete Build Guide

**NST DVA Capstone 2 · Team SectionC_G-09 · NASA Planetary Defense**

> **Structure:** 2 dashboards from NEA data only, 2 dashboards from Close Approaches data only. Each dashboard = 4 KPI tiles + 4 visual charts. No datasets are combined.

---

## CSV Column Names

### `nea_catalogue_clean.csv` (33 columns) → Dashboard 1 & 2:
`spk_id`, `full_name`, `primary_designation`, `name`, `is_potentially_hazardous`, `absolute_magnitude_h`, `diameter_km`, `diameter_m`, `diameter_is_estimated`, `size_category`, `albedo`, `rotation_period_hours`, `class`, `orbital_eccentricity`, `semi_major_axis_au`, `orbital_inclination_deg`, `perihelion_dist_au`, `aphelion_dist_au`, `orbital_period_days`, `orbital_period_years`, `min_orbit_intersection_dist_au`, `min_orbit_intersection_dist_km`, `moid_lunar_distances`, `mean_motion_deg_per_day`, `orbital_condition_code`, `first_obs`, `last_obs`, `data_arc_days`, `data_arc_years`, `is_named`, `observation_span_years`, `risk_tier`, `orbit_class_label`

### `close_approaches_clean.csv` (19 columns) → Dashboard 3 & 4:
`designation`, `full_name`, `close_approach_date`, `distance_au`, `distance_km`, `distance_lunar_distances`, `distance_min_au`, `distance_max_au`, `velocity_km_s`, `velocity_relative_km_h`, `velocity_infinity_km_s`, `absolute_magnitude`, `is_future`, `approach_year`, `approach_month`, `approach_month_name`, `approach_day_of_week`, `is_very_close_approach`, `speed_category`

---

## Extensions (Dashboard → Extensions → Gallery)

| Extension | Purpose | Used In |
|-----------|---------|---------|
| **Export All** | Download filtered data as CSV | Dashboard 2 & 4 |
| **Data-Driven Parameters** | Dynamic Top N slider | Dashboard 4 |

---

## Calculated Fields

### In `nea_catalogue_clean`:

| Name | Formula |
|------|---------|
| `[PHA Count]` | `IF [is_potentially_hazardous] = "True" THEN 1 ELSE 0 END` |
| `[Display Size]` | `30 - [absolute_magnitude_h]` |
| `[MOID Bin]` | Right-click `min_orbit_intersection_dist_au` → Create → Bins → Size: `0.01` |

### In `close_approaches_clean`:

| Name | Formula |
|------|---------|
| `[Velocity Bin]` | Right-click `velocity_km_s` → Create → Bins → Size: `2` |
| `[Danger Score]` | `(1 / [distance_lunar_distances]) * [velocity_km_s]` |

---

## Colors

| Element | Hex |
|---------|-----|
| Critical / PHA / Very Fast | `#D62728` |
| High / Fast | `#FF7F0E` |
| Moderate | `#FFDD57` |
| Low / Slow | `#2CA02C` |
| Accent | `#00D2FF` |
| Default | `#1F77B4` |

---

# DASHBOARD 1: NEA Executive Hazard Overview

**Data Source:** `nea_catalogue_clean.csv` only

---

## KPI Tiles

### KPI 1.A — Total NEAs
| Setting | Value |
|---------|-------|
| **Marks → Text** | `spk_id` → Count Distinct |
| **Font** | 36pt, bold, `#00D2FF` |
| **Subtitle** | "Total NEAs Tracked" |

### KPI 1.B — Potentially Hazardous
| Setting | Value |
|---------|-------|
| **Marks → Text** | `[PHA Count]` → SUM |
| **Font** | 36pt, bold, `#D62728` |
| **Subtitle** | "Potentially Hazardous" |

### KPI 1.C — Critical Risk
| Setting | Value |
|---------|-------|
| **Filter** | `risk_tier` = "Critical" |
| **Marks → Text** | `spk_id` → Count Distinct |
| **Font** | 36pt, bold, `#FF7F0E` |
| **Subtitle** | "Critical Risk Tier" |

### KPI 1.D — Median MOID
| Setting | Value |
|---------|-------|
| **Marks → Text** | `min_orbit_intersection_dist_au` → Median. Format: `0.000` + " AU" |
| **Font** | 36pt, bold, `#00D2FF` |
| **Subtitle** | "Median MOID" |

---

## Charts

### Chart 1.1 — Risk Tier Horizontal Bar
| Setting | Column / Value |
|---------|---------------|
| **Rows** | `risk_tier` |
| **Columns** | `spk_id` → Count Distinct |
| **Sort** | Manual: Critical, High, Moderate, Low |
| **Marks → Color** | `risk_tier` → Critical=`#D62728`, High=`#FF7F0E`, Moderate=`#FFDD57`, Low=`#2CA02C` |
| **Marks → Label** | Show mark labels + Quick Table Calc → Percent of Total |
| **Marks → Tooltip** | `Risk: <risk_tier>` / `Count: <CNTD(spk_id)>` / `Share: <%>` |

### Chart 1.2 — Orbit Class Pie
| Setting | Column / Value |
|---------|---------------|
| **Mark Type** | Pie |
| **Marks → Angle** | `spk_id` → Count Distinct |
| **Marks → Color** | `orbit_class_label` |
| **Marks → Label** | `orbit_class_label` + `CNTD(spk_id)` + Percent of Total |
| **Marks → Tooltip** | `Class: <orbit_class_label>` / `Count: <CNTD(spk_id)>` / `Share: <%>` |

### Chart 1.3 — Size Category Treemap
| Setting | Column / Value |
|---------|---------------|
| **Mark Type** | Square (treemap) |
| **Marks → Size** | `spk_id` → Count Distinct |
| **Marks → Color** | `size_category` → Large=`#D62728`, Medium=`#FF7F0E`, Small=`#00D2FF` |
| **Marks → Label** | `size_category` + `CNTD(spk_id)` |
| **Marks → Tooltip** | `Size: <size_category>` / `Count: <CNTD(spk_id)>` |

### Chart 1.4 — PHA vs Non-PHA by Orbit Class (Stacked Bar)
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `orbit_class_label` (discrete) |
| **Rows** | `spk_id` → Count Distinct |
| **Marks → Color** | `is_potentially_hazardous` → True=`#D62728`, False=`#1F77B4` |
| **Stacking** | Analysis → Stack Marks → On |
| **Sort** | Sort `orbit_class_label` by descending count |
| **Marks → Tooltip** | `Class: <orbit_class_label>` / `PHA: <is_potentially_hazardous>` / `Count: <CNTD(spk_id)>` |

### Layout
```
┌────────┬────────┬────────┬────────┐
│ KPI 1A │ KPI 1B │ KPI 1C │ KPI 1D │
├────────┴────────┼────────┴────────┤
│ Risk Tier Bar   │ Orbit Pie       │
│ (1.1)           │ (1.2)           │
├─────────────────┼─────────────────┤
│ Size Treemap    │ PHA by Class    │
│ (1.3)           │ (1.4)           │
└─────────────────┴─────────────────┘
```
**Filters:** `risk_tier` (multi-select), `orbit_class_label` (dropdown), `is_potentially_hazardous` (toggle)

---

# DASHBOARD 2: NEA Orbital Mechanics Deep Dive

**Data Source:** `nea_catalogue_clean.csv` only

---

## KPI Tiles

### KPI 2.A — Named Asteroids
| Setting | Value |
|---------|-------|
| **Filter** | `is_named` = True |
| **Marks → Text** | `spk_id` → Count Distinct |
| **Font** | 36pt, bold, `#2CA02C` |
| **Subtitle** | "Named Asteroids" |

### KPI 2.B — Avg Observation Span
| Setting | Value |
|---------|-------|
| **Marks → Text** | `observation_span_years` → Average. Format: `0.0` + " yrs" |
| **Font** | 36pt, bold, `#00D2FF` |
| **Subtitle** | "Avg Observation Span" |

### KPI 2.C — Large Asteroids (>1 km)
| Setting | Value |
|---------|-------|
| **Filter** | `size_category` contains "Large" |
| **Marks → Text** | `spk_id` → Count Distinct |
| **Font** | 36pt, bold, `#FF7F0E` |
| **Subtitle** | "Large Asteroids (>1 km)" |

### KPI 2.D — High + Critical Risk
| Setting | Value |
|---------|-------|
| **Filter** | `risk_tier` IN ("Critical", "High") |
| **Marks → Text** | `spk_id` → Count Distinct |
| **Font** | 36pt, bold, `#D62728` |
| **Subtitle** | "High + Critical Risk" |

---

## Charts

### Chart 2.1 — MOID Histogram
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `[MOID Bin]` (binned from `min_orbit_intersection_dist_au`, size 0.01) |
| **Rows** | `spk_id` → Count Distinct |
| **Filter** | `min_orbit_intersection_dist_au` range: 0 to 0.5 |
| **Marks → Color** | `is_potentially_hazardous` → True=`#D62728`, False=`#1F77B4` |
| **Reference Line** | Constant X = `0.05`, dashed orange, label "PHA Threshold" |
| **Marks → Tooltip** | `MOID: <MOID Bin> AU` / `Count: <CNTD(spk_id)>` / `PHA: <is_potentially_hazardous>` |

### Chart 2.2 — Hazard Quadrant Scatter (Magnitude vs MOID)
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `min_orbit_intersection_dist_au` (continuous, range 0–0.3) |
| **Rows** | `absolute_magnitude_h` (continuous, **Reverse Y-axis**) |
| **Mark Type** | Circle |
| **Marks → Color** | `risk_tier` → Critical=`#D62728`, High=`#FF7F0E`, Moderate=`#FFDD57`, Low=`#2CA02C` |
| **Marks → Size** | `[Display Size]` (= 30 - absolute_magnitude_h) |
| **Marks → Detail** | `full_name` |
| **Marks → Tooltip** | `<full_name>` / `MOID: <min_orbit_intersection_dist_au> AU` / `H: <absolute_magnitude_h>` / `Risk: <risk_tier>` |
| **Ref Line 1** | Constant X = `0.05`, orange dashed |
| **Ref Line 2** | Constant Y = `22`, gray dashed, label "H Threshold" |

### Chart 2.3 — Eccentricity vs Semi-Major Axis Scatter
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `semi_major_axis_au` (continuous, range 0–4) |
| **Rows** | `orbital_eccentricity` (continuous, range 0–1) |
| **Mark Type** | Circle |
| **Marks → Color** | `is_potentially_hazardous` → True=`#D62728`, False=`#00D2FF`, opacity 50% |
| **Marks → Size** | `[Display Size]` |
| **Marks → Detail** | `full_name`, `risk_tier` |
| **Marks → Tooltip** | `<full_name>` / `SMA: <semi_major_axis_au> AU` / `Ecc: <orbital_eccentricity>` / `Risk: <risk_tier>` |
| **Reference Line** | Constant X = `1.0`, green dashed, label "Earth Orbit" |

### Chart 2.4 — Observation Span Box Plot
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `is_potentially_hazardous` (discrete) |
| **Rows** | `observation_span_years` (continuous) |
| **Mark Type** | Circle → Analytics → drag "Box Plot" → drop on Cell |
| **Marks → Color** | `is_potentially_hazardous` → True=`#D62728`, False=`#1F77B4` |
| **Marks → Tooltip** | `PHA: <is_potentially_hazardous>` / `Span: <observation_span_years> years` |

### Layout
```
┌────────┬────────┬────────┬────────┐
│ KPI 2A │ KPI 2B │ KPI 2C │ KPI 2D │
├────────┴────────┼────────┴────────┤
│ MOID Hist (2.1) │ Hazard Quad(2.2)│
├─────────────────┼─────────────────┤
│ Orbital Scatter │ Obs Span Box    │
│ (2.3)           │ (2.4)           │
└─────────────────┴─────────────────┘
```
**Filters:** `risk_tier`, `orbit_class_label`, `size_category`
**Extension:** **Export All** at bottom-right

---

# DASHBOARD 3: Close Approaches Historical Timeline

**Data Source:** `close_approaches_clean.csv` only

---

## KPI Tiles

### KPI 3.A — Total Close Approaches
| Setting | Value |
|---------|-------|
| **Marks → Text** | `designation` → Count |
| **Font** | 36pt, bold, `#00D2FF` |
| **Subtitle** | "Total Close Approaches" |

### KPI 3.B — Very Close (<10 LD)
| Setting | Value |
|---------|-------|
| **Filter** | `is_very_close_approach` = True |
| **Marks → Text** | `designation` → Count |
| **Font** | 36pt, bold, `#D62728` |
| **Subtitle** | "Very Close (<10 LD)" |

### KPI 3.C — Average Velocity
| Setting | Value |
|---------|-------|
| **Marks → Text** | `velocity_km_s` → Average. Format: `0.0` + " km/s" |
| **Font** | 36pt, bold, `#FF7F0E` |
| **Subtitle** | "Avg Approach Velocity" |

### KPI 3.D — Max Velocity
| Setting | Value |
|---------|-------|
| **Marks → Text** | `velocity_km_s` → Maximum. Format: `0.0` + " km/s" |
| **Font** | 36pt, bold, `#D62728` |
| **Subtitle** | "Fastest Approach" |

---

## Charts

### Chart 3.1 — Annual Approach Count Line
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `approach_year` (discrete) |
| **Rows** | `designation` → Count |
| **Mark Type** | Line + Show Markers |
| **Marks → Color** | Fixed `#00D2FF` |
| **Marks → Label** | Show mark labels |
| **Reference Line** | Constant X = `2025`, dashed red, label "Present" |
| **Marks → Tooltip** | `Year: <approach_year>` / `Approaches: <CNT(designation)>` |

### Chart 3.2 — Velocity Distribution Histogram
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `[Velocity Bin]` (binned from `velocity_km_s`, size 2) |
| **Rows** | `designation` → Count |
| **Marks → Color** | `speed_category` → Very Fast=`#D62728`, Fast=`#FF7F0E`, Moderate=`#FFDD57`, Slow=`#2CA02C` |
| **Stacking** | Analysis → Stack Marks → On |
| **Marks → Tooltip** | `Velocity: <Velocity Bin> km/s` / `Category: <speed_category>` / `Count: <CNT(designation)>` |

### Chart 3.3 — Monthly Heatmap (Highlight Table)
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `approach_year` (discrete) |
| **Rows** | `approach_month_name` (discrete, manual sort Jan–Dec) |
| **Mark Type** | Square |
| **Marks → Color** | `designation` → Count → sequential Blue-Teal gradient |
| **Marks → Label** | `designation` → Count (number inside each cell) |
| **Marks → Size** | Max slider |
| **Marks → Tooltip** | `<approach_month_name> <approach_year>` / `Approaches: <CNT(designation)>` |

### Chart 3.4 — Speed Category Bar
| Setting | Column / Value |
|---------|---------------|
| **Rows** | `speed_category` |
| **Columns** | `designation` → Count |
| **Sort** | Manual: Slow, Moderate, Fast, Very Fast |
| **Marks → Color** | `speed_category` → Slow=`#2CA02C`, Moderate=`#FFDD57`, Fast=`#FF7F0E`, Very Fast=`#D62728` |
| **Marks → Label** | Show mark labels + Percent of Total |
| **Marks → Tooltip** | `Speed: <speed_category>` / `Count: <CNT(designation)>` / `Share: <%>` |

### Layout
```
┌────────┬────────┬────────┬────────┐
│ KPI 3A │ KPI 3B │ KPI 3C │ KPI 3D │
├────────┴────────┴────────┴────────┤
│   Annual Approach Line (3.1)      │
├─────────────────┬─────────────────┤
│ Vel Hist (3.2)  │ Speed Bar (3.4) │
├─────────────────┴─────────────────┤
│     Monthly Heatmap (3.3)         │
└───────────────────────────────────┘
```
**Filters:** `speed_category` (multi-select), `is_very_close_approach` (toggle), `approach_year` (range slider)

---

# DASHBOARD 4: Close Approaches Future Risk Forecast

**Data Source:** `close_approaches_clean.csv` only

---

## KPI Tiles

### KPI 4.A — Future Approaches
| Setting | Value |
|---------|-------|
| **Filter** | `approach_year` >= 2025 |
| **Marks → Text** | `designation` → Count |
| **Font** | 36pt, bold, `#00D2FF` |
| **Subtitle** | "Future Approaches (2025–2035)" |

### KPI 4.B — Future Very Close
| Setting | Value |
|---------|-------|
| **Filter** | `approach_year` >= 2025 AND `is_very_close_approach` = True |
| **Marks → Text** | `designation` → Count |
| **Font** | 36pt, bold, `#D62728` |
| **Subtitle** | "Future Very Close (<10 LD)" |

### KPI 4.C — Min Future Distance
| Setting | Value |
|---------|-------|
| **Filter** | `approach_year` >= 2025 |
| **Marks → Text** | `distance_lunar_distances` → Minimum. Format: `0.00` + " LD" |
| **Font** | 36pt, bold, `#FF7F0E` |
| **Subtitle** | "Closest Future Approach" |

### KPI 4.D — Avg Future Velocity
| Setting | Value |
|---------|-------|
| **Filter** | `approach_year` >= 2025 |
| **Marks → Text** | `velocity_km_s` → Average. Format: `0.0` + " km/s" |
| **Font** | 36pt, bold, `#00D2FF` |
| **Subtitle** | "Avg Future Velocity" |

---

## Charts

### Chart 4.1 — Future Danger Map Scatter
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `close_approach_date` → Exact Date (continuous) |
| **Rows** | `distance_lunar_distances` (continuous, **Reverse Y-axis**) |
| **Filter** | `approach_year` range: 2025–2035 |
| **Mark Type** | Circle |
| **Marks → Color** | `speed_category` → Very Fast=`#D62728`, Fast=`#FF7F0E`, Moderate=`#FFDD57`, Slow=`#2CA02C` |
| **Marks → Size** | `[Danger Score]` calc field |
| **Marks → Detail** | `full_name`, `velocity_km_s` |
| **Marks → Tooltip** | `<full_name>` / `Date: <close_approach_date>` / `Dist: <distance_lunar_distances> LD` / `Speed: <velocity_km_s> km/s` |
| **Reference Line** | Constant Y = `10`, red dashed, label "Very Close Threshold" |

### Chart 4.2 — Top 20 Closest Future Table
| Setting | Column / Value |
|---------|---------------|
| **Rows** | `full_name`, `close_approach_date`, `distance_lunar_distances`, `velocity_km_s`, `speed_category` |
| **Filter 1** | `approach_year` range: 2025–2035 |
| **Sort** | `distance_lunar_distances` → Ascending |
| **Filter 2** | `full_name` → Top tab → By field → Top 20 by `distance_lunar_distances` Minimum |
| **Conditional Color** | Format `distance_lunar_distances`: <1=red bg, <5=orange bg, <10=yellow bg |

### Chart 4.3 — Future Yearly Stacked Bar
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `approach_year` (discrete, filtered 2025–2035) |
| **Rows** | `designation` → Count |
| **Marks → Color** | `is_very_close_approach` → True=`#D62728`, False=`#1F77B4` |
| **Stacking** | Analysis → Stack Marks → On |
| **Marks → Tooltip** | `Year: <approach_year>` / `Very Close: <is_very_close_approach>` / `Count: <CNT(designation)>` |

### Chart 4.4 — Distance vs Velocity Scatter (Future)
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `velocity_km_s` (continuous) |
| **Rows** | `distance_lunar_distances` (continuous, logarithmic scale) |
| **Filter** | `approach_year` range: 2025–2035 |
| **Mark Type** | Circle |
| **Marks → Color** | `speed_category` → same 4-color map |
| **Marks → Detail** | `full_name`, `close_approach_date` |
| **Marks → Tooltip** | `<full_name>` / `Date: <close_approach_date>` / `Dist: <distance_lunar_distances> LD` / `Speed: <velocity_km_s> km/s` |

### Layout
```
┌────────┬────────┬────────┬────────┐
│ KPI 4A │ KPI 4B │ KPI 4C │ KPI 4D │
├────────┴────────┴────────┴────────┤
│   Future Danger Map Scatter (4.1) │
├───────────────────┬───────────────┤
│ Top 20 Table(4.2) │ Dist vs Vel   │
│                   │ Scatter (4.4) │
├───────────────────┼───────────────┤
│ Yearly Stacked Bar (4.3)         │
└───────────────────────────────────┘
```
**Filters:** `approach_year` (range slider), `speed_category` (multi-select)
**Extensions:** **Export All** + **Data-Driven Parameters** (for Top N)

---

## Summary

| Dashboard | Dataset | 4 KPIs | 4 Charts |
|-----------|---------|--------|----------|
| **1** | NEA only | Total, PHAs, Critical, Median MOID | Risk Bar, Orbit Pie, Size Treemap, PHA by Class |
| **2** | NEA only | Named, Avg Obs Span, Large, High+Critical | MOID Hist, Hazard Quad, Orbital Scatter, Obs Box |
| **3** | CA only | Total CAs, Very Close, Avg Vel, Max Vel | Annual Line, Vel Hist, Monthly Heat, Speed Bar |
| **4** | CA only | Future CAs, Future Close, Min Dist, Avg Vel | Danger Map, Top 20, Yearly Bar, Dist vs Vel |

---

## Publishing

1. File → Save to Tableau Public
2. Hide raw worksheet tabs
3. Test filters in incognito
4. Screenshots (1920×1080) → `tableau/screenshots/`
5. Paste URL → `tableau/dashboard_links.md` + `README.md`
