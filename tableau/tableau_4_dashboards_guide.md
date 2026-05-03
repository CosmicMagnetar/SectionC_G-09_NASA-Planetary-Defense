# Tableau 4-Dashboard Complete Build Guide

**NST DVA Capstone 2 · Team SectionC_G-09 · NASA Planetary Defense**

> Every dashboard has 2 charts from each dataset (2 NEA + 2 Close Approaches = 4 charts per dashboard).

---

## Actual CSV Column Names Reference

### `nea_catalogue_clean.csv` (33 columns):
`spk_id`, `full_name`, `primary_designation`, `name`, `is_potentially_hazardous`, `absolute_magnitude_h`, `diameter_km`, `diameter_m`, `diameter_is_estimated`, `size_category`, `albedo`, `rotation_period_hours`, `class`, `orbital_eccentricity`, `semi_major_axis_au`, `orbital_inclination_deg`, `perihelion_dist_au`, `aphelion_dist_au`, `orbital_period_days`, `orbital_period_years`, `min_orbit_intersection_dist_au`, `min_orbit_intersection_dist_km`, `moid_lunar_distances`, `mean_motion_deg_per_day`, `orbital_condition_code`, `first_obs`, `last_obs`, `data_arc_days`, `data_arc_years`, `is_named`, `observation_span_years`, `risk_tier`, `orbit_class_label`

### `close_approaches_clean.csv` (19 columns):
`designation`, `full_name`, `close_approach_date`, `distance_au`, `distance_km`, `distance_lunar_distances`, `distance_min_au`, `distance_max_au`, `velocity_km_s`, `velocity_relative_km_h`, `velocity_infinity_km_s`, `absolute_magnitude`, `is_future`, `approach_year`, `approach_month`, `approach_month_name`, `approach_day_of_week`, `is_very_close_approach`, `speed_category`

---

## Extensions to Install (Dashboard → Extensions → Gallery)

| Extension | Purpose | Used In |
|-----------|---------|---------|
| **Export All** | Download filtered data as CSV/Excel | Dashboard 2 & 4 |
| **Data-Driven Parameters** | Dynamic "Top N" slider | Dashboard 4 |
| **Filter Bookmarks** | Save filter presets | Dashboard 1 (optional) |

---

## Calculated Fields to Create First

### In `nea_catalogue_clean`:

| Field Name | Formula | Purpose |
|-----------|---------|---------|
| `[PHA Count]` | `IF [is_potentially_hazardous] = "True" THEN 1 ELSE 0 END` | Sum PHAs in KPIs |
| `[Display Size]` | `30 - [absolute_magnitude_h]` | Inverted H for bubble sizing |
| `[MOID Bin]` | Right-click `min_orbit_intersection_dist_au` → Create → Bins → Size: `0.01` | Histogram x-axis |

### In `close_approaches_clean`:

| Field Name | Formula | Purpose |
|-----------|---------|---------|
| `[Velocity Bin]` | Right-click `velocity_km_s` → Create → Bins → Size: `2` | Histogram x-axis |
| `[Danger Score]` | `(1 / [distance_lunar_distances]) * [velocity_km_s]` | Risk bubble sizing |
| `[Row Index]` | `INDEX()` | Top-N table limiting |

---

## Color Palette

| Element | Hex |
|---------|-----|
| Critical / PHA / Very Fast | `#D62728` |
| High / Fast | `#FF7F0E` |
| Moderate | `#FFDD57` |
| Low / Slow | `#2CA02C` |
| Accent / Non-PHA | `#00D2FF` |
| Default | `#1F77B4` |

---

# DASHBOARD 1: Executive Overview & Approach Summary

---

### Chart 1.1 — Risk Tier Bar *(NEA dataset)*

| Setting | Exact Column / Value |
|---------|---------------------|
| **Rows** | `risk_tier` |
| **Columns** | `spk_id` → right-click → Measure → Count Distinct |
| **Sort** | Right-click `risk_tier` → Sort → Manual → Critical, High, Moderate, Low |
| **Marks → Color** | `risk_tier` → Critical=`#D62728`, High=`#FF7F0E`, Moderate=`#FFDD57`, Low=`#2CA02C` |
| **Marks → Label** | Show mark labels ON. Add Quick Table Calc → Percent of Total |
| **Marks → Tooltip** | `Risk Tier: <risk_tier>` / `Count: <CNTD(spk_id)>` / `Share: <% of Total>` |

---

### Chart 1.2 — Orbit Class Pie *(NEA dataset)*

| Setting | Exact Column / Value |
|---------|---------------------|
| **Mark Type** | Change to **Pie** |
| **Marks → Angle** | `spk_id` → Count Distinct |
| **Marks → Color** | `orbit_class_label` |
| **Marks → Label** | `orbit_class_label` + `CNTD(spk_id)` with Percent of Total |
| **Marks → Tooltip** | `Class: <orbit_class_label>` / `Count: <CNTD(spk_id)>` / `Share: <%>` |

---

### Chart 1.3 — Annual Approach Line *(Close Approaches dataset)*

| Setting | Exact Column / Value |
|---------|---------------------|
| **Columns** | `approach_year` → Discrete (blue pill) |
| **Rows** | `designation` → Count |
| **Mark Type** | Line → right-click → Show Markers |
| **Marks → Color** | Fixed: `#00D2FF` |
| **Marks → Label** | Show mark labels ON |
| **Reference Line** | Analytics → Constant Line on X-axis → Value `2025`, dashed red, label "Present" |
| **Marks → Tooltip** | `Year: <approach_year>` / `Approaches: <CNT(designation)>` |

---

### Chart 1.4 — Speed Category Bar *(Close Approaches dataset)*

| Setting | Exact Column / Value |
|---------|---------------------|
| **Rows** | `speed_category` |
| **Columns** | `designation` → Count |
| **Sort** | Manual: Slow (<5 km/s), Moderate (5–15), Fast (15–30), Very Fast (>30) |
| **Marks → Color** | `speed_category` → Slow=`#2CA02C`, Moderate=`#FFDD57`, Fast=`#FF7F0E`, Very Fast=`#D62728` |
| **Marks → Label** | Show mark labels ON |
| **Marks → Tooltip** | `Speed: <speed_category>` / `Count: <CNT(designation)>` / `Share: <%>` |

### Dashboard 1 Layout
```
┌──────────────────────┬──────────────────────┐
│ Risk Tier Bar (1.1)  │ Orbit Class Pie(1.2) │
│ [NEA]                │ [NEA]                │
├──────────────────────┴──────────────────────┤
│     Annual Approach Line (1.3) [CA]         │
├─────────────────────────────────────────────┤
│     Speed Category Bar (1.4) [CA]           │
└─────────────────────────────────────────────┘
```
**Filters:** `risk_tier` (multi-select), `speed_category` (multi-select)

---

# DASHBOARD 2: Hazard Analysis & Velocity Deep Dive

---

### Chart 2.1 — MOID Histogram *(NEA dataset)*

| Setting | Exact Column / Value |
|---------|---------------------|
| **Columns** | `[MOID Bin]` (binned from `min_orbit_intersection_dist_au`, size 0.01) |
| **Rows** | `spk_id` → Count Distinct |
| **Filter** | `min_orbit_intersection_dist_au` → Range: 0 to 0.5 |
| **Marks → Color** | `is_potentially_hazardous` → True=`#D62728`, False=`#1F77B4` |
| **Reference Line** | Analytics → Constant Line on X-axis → `0.05`, dashed orange, label "PHA Threshold" |
| **Marks → Tooltip** | `MOID: <MOID Bin> AU` / `Count: <CNTD(spk_id)>` / `PHA: <is_potentially_hazardous>` |

---

### Chart 2.2 — Hazard Quadrant Scatter *(NEA dataset)*

| Setting | Exact Column / Value |
|---------|---------------------|
| **Columns** | `min_orbit_intersection_dist_au` (continuous). X-axis fixed range: 0 to 0.3 |
| **Rows** | `absolute_magnitude_h` (continuous). **Reverse Y-axis** (Edit Axis → Reversed) |
| **Mark Type** | Circle |
| **Marks → Color** | `risk_tier` → Critical=`#D62728`, High=`#FF7F0E`, Moderate=`#FFDD57`, Low=`#2CA02C` |
| **Marks → Size** | `[Display Size]` (= 30 - absolute_magnitude_h) |
| **Marks → Detail** | `full_name` |
| **Marks → Tooltip** | `<full_name>` / `MOID: <min_orbit_intersection_dist_au> AU` / `H: <absolute_magnitude_h>` / `Risk: <risk_tier>` |
| **Reference Line 1** | Constant Line X-axis → `0.05`, dashed orange |
| **Reference Line 2** | Constant Line Y-axis → `22`, dashed gray, label "H Threshold" |

---

### Chart 2.3 — Velocity Histogram *(Close Approaches dataset)*

| Setting | Exact Column / Value |
|---------|---------------------|
| **Columns** | `[Velocity Bin]` (binned from `velocity_km_s`, size 2) |
| **Rows** | `designation` → Count |
| **Marks → Color** | `speed_category` → Very Fast=`#D62728`, Fast=`#FF7F0E`, Moderate=`#FFDD57`, Slow=`#2CA02C` |
| **Stacking** | Analysis → Stack Marks → On |
| **Marks → Tooltip** | `Velocity: <Velocity Bin> km/s` / `Category: <speed_category>` / `Count: <CNT(designation)>` |

---

### Chart 2.4 — Distance vs Velocity Scatter *(Close Approaches dataset)*

| Setting | Exact Column / Value |
|---------|---------------------|
| **Columns** | `velocity_km_s` (continuous) |
| **Rows** | `distance_lunar_distances` (continuous). Y-axis → Logarithmic scale |
| **Filter** | `approach_year` → Range: 2015 to 2024 |
| **Mark Type** | Circle |
| **Marks → Color** | `speed_category` → same 4-color map |
| **Marks → Size** | `absolute_magnitude` (adjust size range) |
| **Marks → Detail** | `full_name`, `close_approach_date` |
| **Marks → Tooltip** | `<full_name>` / `Date: <close_approach_date>` / `Distance: <distance_lunar_distances> LD` / `Speed: <velocity_km_s> km/s` |

### Dashboard 2 Layout
```
┌──────────────────────┬──────────────────────┐
│ MOID Histogram (2.1) │ Hazard Quadrant(2.2) │
│ [NEA]                │ [NEA]                │
├──────────────────────┼──────────────────────┤
│ Velocity Hist (2.3)  │ Dist vs Vel (2.4)    │
│ [CA]                 │ [CA]                 │
└──────────────────────┴──────────────────────┘
```
**Filters:** `risk_tier`, `is_potentially_hazardous` (NEA), `speed_category` (CA)
**Extension:** **Export All** at bottom-right

---

# DASHBOARD 3: Observation Quality & Seasonal Patterns

---

### Chart 3.1 — Observation Span Box Plot *(NEA dataset)*

| Setting | Exact Column / Value |
|---------|---------------------|
| **Columns** | `is_potentially_hazardous` (discrete) |
| **Rows** | `observation_span_years` (continuous) |
| **Mark Type** | Circle |
| **Box Plot** | Analytics pane → drag "Box Plot" → drop on Cell |
| **Marks → Color** | `is_potentially_hazardous` → True=`#D62728`, False=`#1F77B4` |
| **Marks → Tooltip** | `PHA: <is_potentially_hazardous>` / `Span: <observation_span_years> years` |

---

### Chart 3.2 — Size Category Treemap *(NEA dataset)*

| Setting | Exact Column / Value |
|---------|---------------------|
| **Mark Type** | **Square** (creates treemap) |
| **Marks → Size** | `spk_id` → Count Distinct |
| **Marks → Color** | `size_category` → Large=`#D62728`, Medium=`#FF7F0E`, Small=`#00D2FF` |
| **Marks → Label** | `size_category` + `CNTD(spk_id)` |
| **Marks → Tooltip** | `Size: <size_category>` / `Count: <CNTD(spk_id)>` |

---

### Chart 3.3 — Monthly Heatmap *(Close Approaches dataset)*

| Setting | Exact Column / Value |
|---------|---------------------|
| **Columns** | `approach_year` (discrete) |
| **Rows** | `approach_month_name` (discrete). Sort → Manual → January to December |
| **Mark Type** | Square |
| **Marks → Color** | `designation` → Count → gradient. Edit Colors → Sequential Blue-Teal |
| **Marks → Label** | `designation` → Count (number in each cell) |
| **Marks → Size** | Max slider so squares fill cells |
| **Marks → Tooltip** | `<approach_month_name> <approach_year>` / `Approaches: <CNT(designation)>` |

---

### Chart 3.4 — Very Close vs Normal Stacked Bar *(Close Approaches dataset)*

| Setting | Exact Column / Value |
|---------|---------------------|
| **Columns** | `approach_year` (discrete) |
| **Rows** | `designation` → Count |
| **Marks → Color** | `is_very_close_approach` → True=`#D62728`, False=`#1F77B4` |
| **Stacking** | Analysis → Stack Marks → On |
| **Marks → Label** | Analysis → Totals → Show Column Grand Totals |
| **Marks → Tooltip** | `Year: <approach_year>` / `Very Close: <is_very_close_approach>` / `Count: <CNT(designation)>` |

### Dashboard 3 Layout
```
┌──────────────────────┬──────────────────────┐
│ Obs Span Box (3.1)   │ Size Treemap (3.2)   │
│ [NEA]                │ [NEA]                │
├──────────────────────┴──────────────────────┤
│     Monthly Heatmap (3.3) [CA]              │
├─────────────────────────────────────────────┤
│  Very Close vs Normal Bar (3.4) [CA]        │
└─────────────────────────────────────────────┘
```
**Filters:** `is_potentially_hazardous` (NEA), `orbit_class_label` (NEA), `approach_year` slider (CA), `is_very_close_approach` toggle (CA)

---

# DASHBOARD 4: Future Risk Forecast & Asteroid Profiling

---

### Chart 4.1 — Orbital Scatter *(NEA dataset)*

| Setting | Exact Column / Value |
|---------|---------------------|
| **Columns** | `semi_major_axis_au` (continuous). X-axis fixed: 0 to 4 |
| **Rows** | `orbital_eccentricity` (continuous). Y-axis fixed: 0 to 1 |
| **Mark Type** | Circle |
| **Marks → Color** | `is_potentially_hazardous` → True=`#D62728`, False=`#00D2FF`. Opacity: 50% |
| **Marks → Size** | `[Display Size]` calc field |
| **Marks → Detail** | `full_name`, `risk_tier`, `min_orbit_intersection_dist_au` |
| **Marks → Tooltip** | `<full_name>` / `SMA: <semi_major_axis_au> AU` / `Ecc: <orbital_eccentricity>` / `MOID: <min_orbit_intersection_dist_au> AU` / `Risk: <risk_tier>` |
| **Reference Line** | Constant Line X-axis → `1.0`, green dashed, label "Earth Orbit" |

---

### Chart 4.2 — KPI Tiles *(NEA dataset)* — 3 mini worksheets

| Tile | Column Used | Aggregation | Font | Subtitle |
|------|-------------|-------------|------|----------|
| Total NEAs | `spk_id` | Count Distinct | 36pt bold `#00D2FF` | "Total NEAs" |
| PHAs | `[PHA Count]` calc field | SUM | 36pt bold `#D62728` | "Potentially Hazardous" |
| Median MOID | `min_orbit_intersection_dist_au` | Median, format `0.000 AU` | 36pt bold `#FF7F0E` | "Median MOID" |

**How:** New sheet → drag column to Text mark → change aggregation → Format font. Place 3 tiles in horizontal container.

---

### Chart 4.3 — Future Danger Map Scatter *(Close Approaches dataset)*

| Setting | Exact Column / Value |
|---------|---------------------|
| **Columns** | `close_approach_date` → right-click → Exact Date (continuous green) |
| **Rows** | `distance_lunar_distances` (continuous). **Reverse Y-axis** (Edit Axis → Reversed) |
| **Filter** | `approach_year` → Range: 2025 to 2035 |
| **Mark Type** | Circle |
| **Marks → Color** | `speed_category` → Very Fast=`#D62728`, Fast=`#FF7F0E`, Moderate=`#FFDD57`, Slow=`#2CA02C` |
| **Marks → Size** | `[Danger Score]` calc field |
| **Marks → Detail** | `full_name`, `velocity_km_s` |
| **Marks → Tooltip** | `<full_name>` / `Date: <close_approach_date>` / `Distance: <distance_lunar_distances> LD` / `Speed: <velocity_km_s> km/s` / `Category: <speed_category>` |
| **Reference Line** | Constant Line Y-axis → `10`, red dashed, label "Very Close Threshold" |

---

### Chart 4.4 — Top 20 Closest Future Table *(Close Approaches dataset)*

| Setting | Exact Column / Value |
|---------|---------------------|
| **Rows** | Drag in order: `full_name`, `close_approach_date`, `distance_lunar_distances`, `velocity_km_s`, `speed_category` |
| **Filter 1** | `approach_year` → Range: 2025 to 2035 |
| **Sort** | Right-click `distance_lunar_distances` → Sort → Ascending |
| **Filter 2** | `full_name` → Top tab → By field → Top `20` by `distance_lunar_distances` Minimum |
| **Conditional Color** | Right-click `distance_lunar_distances` column → Format → if <1 red bg, <5 orange bg, <10 yellow bg |
| **Extension** | **Data-Driven Parameters** → create Parameter "Top N" (integer, default 20, range 5–100), replace 20 with parameter |

### Dashboard 4 Layout
```
┌──────────┬──────────┬──────────┐
│ KPI Tile │ KPI Tile │ KPI Tile │  ← NEA KPIs (4.2)
├──────────┴──────────┴──────────┤
│   Orbital Scatter (4.1) [NEA]  │
├──────────────────┬─────────────┤
│ Future Danger Map│ Top 20 Table│
│ (4.3) [CA]       │ (4.4) [CA]  │
└──────────────────┴─────────────┘
```
**Filters:** `approach_year` slider (CA), `speed_category` (CA), `risk_tier` (NEA)
**Extensions:** **Export All** + **Data-Driven Parameters**

---

## Summary Table

| Dashboard | NEA Chart 1 | NEA Chart 2 | CA Chart 1 | CA Chart 2 |
|-----------|------------|------------|-----------|-----------|
| 1 | Risk Tier Bar | Orbit Class Pie | Annual Line | Speed Category Bar |
| 2 | MOID Histogram | Hazard Quadrant | Velocity Histogram | Dist vs Vel Scatter |
| 3 | Obs Span Box | Size Treemap | Monthly Heatmap | Close vs Normal Bar |
| 4 | Orbital Scatter + KPIs | (KPIs) | Future Danger Map | Top 20 Table |

---

## Publishing

1. File → Save to Tableau Public
2. Hide raw worksheet tabs (right-click → Hide)
3. Test all filters in incognito browser
4. Export screenshots (1920×1080) to `tableau/screenshots/`
5. Paste URL into `tableau/dashboard_links.md`
