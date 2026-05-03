# Tableau 4-Dashboard Complete Build Guide

**NST DVA Capstone 2 · Team SectionC_G-09 · NASA Planetary Defense**

> **Structure:** Each dashboard = 4 KPI text tiles (2 from each dataset) + 2 or 4 visual charts (from both datasets).

---

## CSV Column Names

### `nea_catalogue_clean.csv` (33 columns):
`spk_id`, `full_name`, `primary_designation`, `name`, `is_potentially_hazardous`, `absolute_magnitude_h`, `diameter_km`, `diameter_m`, `diameter_is_estimated`, `size_category`, `albedo`, `rotation_period_hours`, `class`, `orbital_eccentricity`, `semi_major_axis_au`, `orbital_inclination_deg`, `perihelion_dist_au`, `aphelion_dist_au`, `orbital_period_days`, `orbital_period_years`, `min_orbit_intersection_dist_au`, `min_orbit_intersection_dist_km`, `moid_lunar_distances`, `mean_motion_deg_per_day`, `orbital_condition_code`, `first_obs`, `last_obs`, `data_arc_days`, `data_arc_years`, `is_named`, `observation_span_years`, `risk_tier`, `orbit_class_label`

### `close_approaches_clean.csv` (19 columns):
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

## Colors (All Dashboards)

| Element | Hex |
|---------|-----|
| Critical / PHA / Very Fast | `#D62728` |
| High / Fast | `#FF7F0E` |
| Moderate | `#FFDD57` |
| Low / Slow | `#2CA02C` |
| Accent | `#00D2FF` |
| Default | `#1F77B4` |

---

# DASHBOARD 1: Executive Overview

## KPI Tiles (4 text tiles across the top)

### KPI 1.A — Total NEAs *(NEA dataset)*
| Setting | Value |
|---------|-------|
| **Marks → Text** | `spk_id` → Count Distinct |
| **Font** | 36pt, bold, `#00D2FF` |
| **Subtitle** | "Total NEAs Tracked" (12pt gray) |

### KPI 1.B — Potentially Hazardous *(NEA dataset)*
| Setting | Value |
|---------|-------|
| **Marks → Text** | `[PHA Count]` → SUM |
| **Font** | 36pt, bold, `#D62728` |
| **Subtitle** | "Potentially Hazardous" |

### KPI 1.C — Total Close Approaches *(CA dataset)*
| Setting | Value |
|---------|-------|
| **Marks → Text** | `designation` → Count |
| **Font** | 36pt, bold, `#00D2FF` |
| **Subtitle** | "Total Close Approaches" |

### KPI 1.D — Very Close Approaches *(CA dataset)*
| Setting | Value |
|---------|-------|
| **Marks → Text** | `designation` → Count, **filtered** to `is_very_close_approach` = True |
| **Font** | 36pt, bold, `#D62728` |
| **Subtitle** | "Very Close (<10 LD)" |

---

## Charts (4 visual charts)

### Chart 1.1 — Risk Tier Bar *(NEA dataset)*
| Setting | Column / Value |
|---------|---------------|
| **Rows** | `risk_tier` |
| **Columns** | `spk_id` → Count Distinct |
| **Sort** | Manual: Critical, High, Moderate, Low |
| **Marks → Color** | `risk_tier` → Critical=`#D62728`, High=`#FF7F0E`, Moderate=`#FFDD57`, Low=`#2CA02C` |
| **Marks → Label** | Show mark labels + Percent of Total (Quick Table Calc) |
| **Marks → Tooltip** | `Risk: <risk_tier>` / `Count: <CNTD(spk_id)>` / `Share: <%>` |

### Chart 1.2 — Orbit Class Pie *(NEA dataset)*
| Setting | Column / Value |
|---------|---------------|
| **Mark Type** | Pie |
| **Marks → Angle** | `spk_id` → Count Distinct |
| **Marks → Color** | `orbit_class_label` |
| **Marks → Label** | `orbit_class_label` + `CNTD(spk_id)` + Percent of Total |
| **Marks → Tooltip** | `Class: <orbit_class_label>` / `Count: <CNTD(spk_id)>` / `Share: <%>` |

### Chart 1.3 — Annual Approach Line *(CA dataset)*
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `approach_year` (discrete) |
| **Rows** | `designation` → Count |
| **Mark Type** | Line + Show Markers |
| **Marks → Color** | Fixed `#00D2FF` |
| **Marks → Label** | Show mark labels |
| **Reference Line** | Constant X = `2025`, dashed red, label "Present" |
| **Marks → Tooltip** | `Year: <approach_year>` / `Approaches: <CNT(designation)>` |

### Chart 1.4 — Speed Category Bar *(CA dataset)*
| Setting | Column / Value |
|---------|---------------|
| **Rows** | `speed_category` |
| **Columns** | `designation` → Count |
| **Sort** | Manual: Slow, Moderate, Fast, Very Fast |
| **Marks → Color** | `speed_category` → Slow=`#2CA02C`, Moderate=`#FFDD57`, Fast=`#FF7F0E`, Very Fast=`#D62728` |
| **Marks → Label** | Show mark labels |
| **Marks → Tooltip** | `Speed: <speed_category>` / `Count: <CNT(designation)>` |

### Layout
```
┌────────┬────────┬────────┬────────┐
│ KPI 1A │ KPI 1B │ KPI 1C │ KPI 1D │  ← 4 KPI tiles, ~80px height
├────────┴────────┼────────┴────────┤
│ Risk Tier Bar   │ Orbit Class Pie │  ← NEA row
│ (1.1) [NEA]     │ (1.2) [NEA]     │
├─────────────────┼─────────────────┤
│ Annual Line     │ Speed Cat Bar   │  ← CA row
│ (1.3) [CA]      │ (1.4) [CA]      │
└─────────────────┴─────────────────┘
```
**Filters:** `risk_tier` (multi-select), `speed_category` (multi-select)

---

# DASHBOARD 2: Hazard Analysis & Velocity Deep Dive

## KPI Tiles (4 text tiles)

### KPI 2.A — Critical Risk Count *(NEA dataset)*
| Setting | Value |
|---------|-------|
| **Filter** | `risk_tier` = "Critical" only |
| **Marks → Text** | `spk_id` → Count Distinct |
| **Font** | 36pt, bold, `#D62728` |
| **Subtitle** | "Critical Risk Asteroids" |

### KPI 2.B — Median MOID *(NEA dataset)*
| Setting | Value |
|---------|-------|
| **Marks → Text** | `min_orbit_intersection_dist_au` → Median. Format: `0.000` + " AU" |
| **Font** | 36pt, bold, `#FF7F0E` |
| **Subtitle** | "Median MOID" |

### KPI 2.C — Average Velocity *(CA dataset)*
| Setting | Value |
|---------|-------|
| **Marks → Text** | `velocity_km_s` → Average. Format: `0.0` + " km/s" |
| **Font** | 36pt, bold, `#00D2FF` |
| **Subtitle** | "Avg Approach Velocity" |

### KPI 2.D — Max Velocity *(CA dataset)*
| Setting | Value |
|---------|-------|
| **Marks → Text** | `velocity_km_s` → Maximum. Format: `0.0` + " km/s" |
| **Font** | 36pt, bold, `#D62728` |
| **Subtitle** | "Fastest Approach" |

---

## Charts (4 visual charts)

### Chart 2.1 — MOID Histogram *(NEA dataset)*
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `[MOID Bin]` (binned from `min_orbit_intersection_dist_au`, size 0.01) |
| **Rows** | `spk_id` → Count Distinct |
| **Filter** | `min_orbit_intersection_dist_au` range: 0 to 0.5 |
| **Marks → Color** | `is_potentially_hazardous` → True=`#D62728`, False=`#1F77B4` |
| **Reference Line** | Constant X = `0.05`, dashed orange, label "PHA Threshold" |
| **Marks → Tooltip** | `MOID: <MOID Bin> AU` / `Count: <CNTD(spk_id)>` / `PHA: <is_potentially_hazardous>` |

### Chart 2.2 — Hazard Quadrant Scatter *(NEA dataset)*
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `min_orbit_intersection_dist_au` (continuous). X range: 0 to 0.3 |
| **Rows** | `absolute_magnitude_h` (continuous). **Reverse Y-axis** |
| **Marks → Color** | `risk_tier` → Critical=`#D62728`, High=`#FF7F0E`, Moderate=`#FFDD57`, Low=`#2CA02C` |
| **Marks → Size** | `[Display Size]` (= 30 - absolute_magnitude_h) |
| **Marks → Detail** | `full_name` |
| **Marks → Tooltip** | `<full_name>` / `MOID: <min_orbit_intersection_dist_au> AU` / `H: <absolute_magnitude_h>` / `Risk: <risk_tier>` |
| **Ref Line 1** | Constant X = `0.05`, orange dashed |
| **Ref Line 2** | Constant Y = `22`, gray dashed, label "H Threshold" |

### Chart 2.3 — Velocity Histogram *(CA dataset)*
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `[Velocity Bin]` (binned from `velocity_km_s`, size 2) |
| **Rows** | `designation` → Count |
| **Marks → Color** | `speed_category` → Very Fast=`#D62728`, Fast=`#FF7F0E`, Moderate=`#FFDD57`, Slow=`#2CA02C` |
| **Stacking** | Analysis → Stack Marks → On |
| **Marks → Tooltip** | `Velocity: <Velocity Bin> km/s` / `Category: <speed_category>` / `Count: <CNT(designation)>` |

### Chart 2.4 — Distance vs Velocity Scatter *(CA dataset)*
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `velocity_km_s` (continuous) |
| **Rows** | `distance_lunar_distances` (continuous, logarithmic scale) |
| **Filter** | `approach_year` range: 2015 to 2024 |
| **Marks → Color** | `speed_category` → same 4-color map |
| **Marks → Detail** | `full_name`, `close_approach_date` |
| **Marks → Tooltip** | `<full_name>` / `Date: <close_approach_date>` / `Dist: <distance_lunar_distances> LD` / `Speed: <velocity_km_s> km/s` |

### Layout
```
┌────────┬────────┬────────┬────────┐
│ KPI 2A │ KPI 2B │ KPI 2C │ KPI 2D │
├────────┴────────┼────────┴────────┤
│ MOID Hist (2.1) │ Hazard Quad(2.2)│
│ [NEA]            │ [NEA]           │
├─────────────────┼─────────────────┤
│ Vel Hist (2.3)  │ Dist vs Vel(2.4)│
│ [CA]             │ [CA]            │
└─────────────────┴─────────────────┘
```
**Filters:** `risk_tier`, `is_potentially_hazardous` (NEA), `speed_category` (CA)
**Extension:** **Export All** at bottom-right

---

# DASHBOARD 3: Observation Quality & Seasonal Patterns

## KPI Tiles (4 text tiles)

### KPI 3.A — Named Asteroids *(NEA dataset)*
| Setting | Value |
|---------|-------|
| **Filter** | `is_named` = True |
| **Marks → Text** | `spk_id` → Count Distinct |
| **Font** | 36pt, bold, `#2CA02C` |
| **Subtitle** | "Named Asteroids" |

### KPI 3.B — Avg Observation Span *(NEA dataset)*
| Setting | Value |
|---------|-------|
| **Marks → Text** | `observation_span_years` → Average. Format: `0.0` + " yrs" |
| **Font** | 36pt, bold, `#00D2FF` |
| **Subtitle** | "Avg Observation Span" |

### KPI 3.C — Peak Month *(CA dataset)*
| Setting | Value |
|---------|-------|
| **How** | Sort `approach_month_name` by CNT(designation) descending → show first value as text |
| **Font** | 36pt, bold, `#FF7F0E` |
| **Subtitle** | "Busiest Month" |

### KPI 3.D — Total Years Covered *(CA dataset)*
| Setting | Value |
|---------|-------|
| **Marks → Text** | `approach_year` → Count Distinct |
| **Font** | 36pt, bold, `#00D2FF` |
| **Subtitle** | "Years of Data" |

---

## Charts (4 visual charts)

### Chart 3.1 — Observation Span Box Plot *(NEA dataset)*
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `is_potentially_hazardous` (discrete) |
| **Rows** | `observation_span_years` (continuous) |
| **Mark Type** | Circle |
| **Box Plot** | Analytics pane → drag "Box Plot" → drop on Cell |
| **Marks → Color** | `is_potentially_hazardous` → True=`#D62728`, False=`#1F77B4` |
| **Marks → Tooltip** | `PHA: <is_potentially_hazardous>` / `Span: <observation_span_years> years` |

### Chart 3.2 — Size Category Treemap *(NEA dataset)*
| Setting | Column / Value |
|---------|---------------|
| **Mark Type** | Square (treemap) |
| **Marks → Size** | `spk_id` → Count Distinct |
| **Marks → Color** | `size_category` → Large=`#D62728`, Medium=`#FF7F0E`, Small=`#00D2FF` |
| **Marks → Label** | `size_category` + `CNTD(spk_id)` |
| **Marks → Tooltip** | `Size: <size_category>` / `Count: <CNTD(spk_id)>` |

### Chart 3.3 — Monthly Heatmap *(CA dataset)*
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `approach_year` (discrete) |
| **Rows** | `approach_month_name` (discrete, manual sort Jan–Dec) |
| **Mark Type** | Square |
| **Marks → Color** | `designation` → Count → sequential Blue-Teal gradient |
| **Marks → Label** | `designation` → Count (number in each cell) |
| **Marks → Size** | Max slider |
| **Marks → Tooltip** | `<approach_month_name> <approach_year>` / `Approaches: <CNT(designation)>` |

### Chart 3.4 — Very Close vs Normal Stacked Bar *(CA dataset)*
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `approach_year` (discrete) |
| **Rows** | `designation` → Count |
| **Marks → Color** | `is_very_close_approach` → True=`#D62728`, False=`#1F77B4` |
| **Stacking** | Analysis → Stack Marks → On |
| **Marks → Tooltip** | `Year: <approach_year>` / `Very Close: <is_very_close_approach>` / `Count: <CNT(designation)>` |

### Layout
```
┌────────┬────────┬────────┬────────┐
│ KPI 3A │ KPI 3B │ KPI 3C │ KPI 3D │
├────────┴────────┼────────┴────────┤
│ Obs Span Box    │ Size Treemap    │
│ (3.1) [NEA]     │ (3.2) [NEA]     │
├─────────────────┼─────────────────┤
│ Monthly Heatmap │ Close vs Normal │
│ (3.3) [CA]      │ (3.4) [CA]      │
└─────────────────┴─────────────────┘
```
**Filters:** `is_potentially_hazardous` (NEA), `orbit_class_label` (NEA), `approach_year` slider (CA)

---

# DASHBOARD 4: Future Risk Forecast

## KPI Tiles (4 text tiles)

### KPI 4.A — Future Approaches *(CA dataset)*
| Setting | Value |
|---------|-------|
| **Filter** | `approach_year` >= 2025 |
| **Marks → Text** | `designation` → Count |
| **Font** | 36pt, bold, `#00D2FF` |
| **Subtitle** | "Future Approaches (2025–2035)" |

### KPI 4.B — Future Very Close *(CA dataset)*
| Setting | Value |
|---------|-------|
| **Filter** | `approach_year` >= 2025 AND `is_very_close_approach` = True |
| **Marks → Text** | `designation` → Count |
| **Font** | 36pt, bold, `#D62728` |
| **Subtitle** | "Future Very Close (<10 LD)" |

### KPI 4.C — Large Asteroids *(NEA dataset)*
| Setting | Value |
|---------|-------|
| **Filter** | `size_category` contains "Large" |
| **Marks → Text** | `spk_id` → Count Distinct |
| **Font** | 36pt, bold, `#FF7F0E` |
| **Subtitle** | "Large Asteroids (>1 km)" |

### KPI 4.D — High+Critical Risk *(NEA dataset)*
| Setting | Value |
|---------|-------|
| **Filter** | `risk_tier` IN ("Critical", "High") |
| **Marks → Text** | `spk_id` → Count Distinct |
| **Font** | 36pt, bold, `#D62728` |
| **Subtitle** | "High + Critical Risk" |

---

## Charts (4 visual charts)

### Chart 4.1 — Orbital Scatter *(NEA dataset)*
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `semi_major_axis_au` (continuous, range 0–4) |
| **Rows** | `orbital_eccentricity` (continuous, range 0–1) |
| **Marks → Color** | `is_potentially_hazardous` → True=`#D62728`, False=`#00D2FF`, opacity 50% |
| **Marks → Size** | `[Display Size]` calc field |
| **Marks → Detail** | `full_name`, `risk_tier`, `min_orbit_intersection_dist_au` |
| **Marks → Tooltip** | `<full_name>` / `SMA: <semi_major_axis_au> AU` / `Ecc: <orbital_eccentricity>` / `MOID: <min_orbit_intersection_dist_au> AU` / `Risk: <risk_tier>` |
| **Reference Line** | Constant X = `1.0`, green dashed, label "Earth Orbit" |

### Chart 4.2 — NEA Discovery Timeline *(NEA dataset)*
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `first_obs` → YEAR (discrete) |
| **Rows** | `spk_id` → Count Distinct |
| **Mark Type** | Bar |
| **Marks → Color** | `is_potentially_hazardous` → True=`#D62728`, False=`#1F77B4` |
| **Stacking** | Analysis → Stack Marks → On |
| **Marks → Tooltip** | `Year: <YEAR(first_obs)>` / `Discovered: <CNTD(spk_id)>` / `PHA: <is_potentially_hazardous>` |

### Chart 4.3 — Future Danger Map Scatter *(CA dataset)*
| Setting | Column / Value |
|---------|---------------|
| **Columns** | `close_approach_date` → Exact Date (continuous) |
| **Rows** | `distance_lunar_distances` (continuous). **Reverse Y-axis** |
| **Filter** | `approach_year` range: 2025 to 2035 |
| **Marks → Color** | `speed_category` → Very Fast=`#D62728`, Fast=`#FF7F0E`, Moderate=`#FFDD57`, Slow=`#2CA02C` |
| **Marks → Size** | `[Danger Score]` calc field |
| **Marks → Detail** | `full_name`, `velocity_km_s` |
| **Marks → Tooltip** | `<full_name>` / `Date: <close_approach_date>` / `Dist: <distance_lunar_distances> LD` / `Speed: <velocity_km_s> km/s` |
| **Reference Line** | Constant Y = `10`, red dashed, label "Very Close Threshold" |

### Chart 4.4 — Top 20 Closest Future Table *(CA dataset)*
| Setting | Column / Value |
|---------|---------------|
| **Rows** | `full_name`, `close_approach_date`, `distance_lunar_distances`, `velocity_km_s`, `speed_category` |
| **Filter 1** | `approach_year` range: 2025 to 2035 |
| **Sort** | `distance_lunar_distances` → Ascending |
| **Filter 2 (Top N)** | `full_name` → Top tab → By field → Top 20 by `distance_lunar_distances` Minimum |
| **Conditional Color** | Format `distance_lunar_distances`: <1=red bg, <5=orange bg, <10=yellow bg |

### Layout
```
┌────────┬────────┬────────┬────────┐
│ KPI 4A │ KPI 4B │ KPI 4C │ KPI 4D │
├────────┴────────┴────────┴────────┤
│ Orbital Scatter (4.1) [NEA]       │
├───────────────────┬───────────────┤
│ Discovery Timeline│Future Danger  │
│ (4.2) [NEA]       │Map (4.3) [CA] │
├───────────────────┴───────────────┤
│   Top 20 Closest Table (4.4) [CA]│
└───────────────────────────────────┘
```
**Filters:** `approach_year` slider (CA), `speed_category` (CA), `risk_tier` (NEA)
**Extensions:** **Export All** + **Data-Driven Parameters** (for Top N)

---

## Summary

| Dashboard | 4 KPIs | NEA Charts | CA Charts |
|-----------|--------|-----------|-----------|
| **1: Executive** | Total NEAs, PHAs, Total CAs, Very Close CAs | Risk Tier Bar, Orbit Pie | Annual Line, Speed Bar |
| **2: Hazard & Velocity** | Critical Count, Median MOID, Avg Vel, Max Vel | MOID Hist, Hazard Quad | Vel Hist, Dist vs Vel |
| **3: Quality & Seasonal** | Named Count, Avg Obs Span, Peak Month, Years | Obs Box Plot, Size Treemap | Monthly Heat, Close Bar |
| **4: Future Forecast** | Future CAs, Future Very Close, Large NEAs, High Risk | Orbital Scatter, Discovery Timeline | Danger Map, Top 20 |

---

## Publishing

1. File → Save to Tableau Public
2. Hide raw worksheet tabs
3. Test filters in incognito browser
4. Screenshots (1920×1080) → `tableau/screenshots/`
5. Paste URL → `tableau/dashboard_links.md` + `README.md`
