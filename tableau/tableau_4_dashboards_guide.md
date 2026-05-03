# Tableau 4-Dashboard Complete Build Guide

**NST DVA Capstone 2 · Team SectionC_G-09 · NASA Planetary Defense**

> **Key Rule:** Every dashboard contains charts from BOTH datasets (2 from NEA + 2 from Close Approaches).

---

## Data Sources (Connect Separately — Do NOT Join)

| # | File | Rows | Used In |
|---|------|------|---------|
| 1 | `nea_catalogue_clean.csv` | ~41,000 | All 4 dashboards |
| 2 | `close_approaches_clean.csv` | ~95,000 | All 4 dashboards |

**Setup:** Tableau Public → Connect → Text File → select CSV #1. Then File → New Data Source → Text File → CSV #2.

---

## Extensions to Install

Install from: **Dashboard tab → Objects panel → drag "Extension" → "Extension Gallery" → search → Add**

| Extension | Publisher | Purpose | Used In |
|-----------|----------|---------|---------|
| **Export All** | Tableau | Download filtered data as CSV/Excel | Dashboard 2 & 4 |
| **Data-Driven Parameters** | Tableau | Dynamic "Top N" slider updates from data | Dashboard 4 |
| **Filter Bookmarks** | Tableau | Save/reload filter combos (optional) | Dashboard 1 |

---

## Calculated Fields (Create Before Building Any Sheet)

### In `nea_catalogue_clean`:

```
FIELD: [PHA Count]
Formula: IF [Is Potentially Hazardous] = "True" THEN 1 ELSE 0 END

FIELD: [Size Proxy]
Formula:
IF [Absolute Magnitude H] <= 18 OR [Diameter Km] >= 1 THEN "Large (≥1 km)"
ELSEIF [Absolute Magnitude H] <= 22 THEN "Medium (140m–1km)"
ELSE "Small (<140m)"
END

FIELD: [Display Size]
Formula: 30 - [Absolute Magnitude H]

FIELD: [MOID Bin]
How: Right-click "min_orbit_intersection_dist_au" → Create → Bins → Size: 0.01
```

### In `close_approaches_clean`:

```
FIELD: [Velocity Bin]
How: Right-click "velocity_km_s" → Create → Bins → Size: 2

FIELD: [Time Period]
Formula: IF [Approach Year] >= 2025 THEN "Future" ELSE "Historical" END

FIELD: [Danger Score]
Formula: (1 / [Distance Lunar Distances]) * [Velocity Km S]

FIELD: [Row Index]
Formula: INDEX()
```

---

## Color Palette (Consistent Across All Dashboards)

| Element | Hex |
|---------|-----|
| Critical / PHA / Very Fast | `#D62728` (red) |
| High / Fast | `#FF7F0E` (orange) |
| Moderate | `#FFDD57` (yellow) |
| Low / Slow | `#2CA02C` (green) |
| Accent / Non-PHA | `#00D2FF` (cyan) |
| Default baseline | `#1F77B4` (blue) |

---

# DASHBOARD 1: Executive Overview & Approach Summary

**Goal:** High-level KPIs and counts from both datasets at a glance.

---

## Chart 1.1 — Risk Tier Bar (NEA Dataset)

| Setting | Value |
|---------|-------|
| **Data Source** | `nea_catalogue_clean` |
| **Worksheet Name** | `Risk Tier Breakdown` |
| **Rows** | `risk_tier` |
| **Columns** | `spk_id` → right-click → Measure → **Count Distinct** |
| **Sort** | Right-click `risk_tier` on Rows → Sort → Manual → Critical, High, Moderate, Low |
| **Marks → Color** | Drag `risk_tier` to Color → Edit Colors → Critical=`#D62728`, High=`#FF7F0E`, Moderate=`#FFDD57`, Low=`#2CA02C` |
| **Marks → Label** | Click Label → check "Show mark labels". Also add Quick Table Calc → Percent of Total |
| **Marks → Tooltip** | Edit: `Risk Tier: <risk_tier>` then new line `Count: <CNTD(spk_id)>` then new line `Share: <% of Total CNTD(spk_id)>` |
| **Format** | Right-click chart area → Format → Borders: None. Font: 11pt |

---

## Chart 1.2 — Orbit Class Pie (NEA Dataset)

| Setting | Value |
|---------|-------|
| **Data Source** | `nea_catalogue_clean` |
| **Worksheet Name** | `Orbit Class Distribution` |
| **Mark Type** | Change dropdown (top of Marks card) from Automatic to **Pie** |
| **Marks → Angle** | Drag `spk_id` → Count Distinct |
| **Marks → Color** | Drag `orbit_class_label` → auto-palette or custom |
| **Marks → Label** | Drag `orbit_class_label` to Label. Also drag `CNTD(spk_id)` to Label → right-click → Quick Table Calc → Percent of Total |
| **Marks → Tooltip** | `<orbit_class_label>` then new line `Count: <CNTD(spk_id)>` then new line `Share: <% of Total>` |

---

## Chart 1.3 — Annual Approach Count Line (Close Approaches Dataset)

| Setting | Value |
|---------|-------|
| **Data Source** | `close_approaches_clean` |
| **Worksheet Name** | `Annual Timeline` |
| **Columns** | Drag `approach_year` → right-click → **Discrete** (blue pill) |
| **Rows** | Drag `designation` → Count |
| **Mark Type** | Line |
| **Marks → Color** | Fixed single color: `#00D2FF` |
| **Marks → Label** | Check "Show mark labels" (shows count per year) |
| **Marks → Size** | Increase line weight to ~2px |
| **Reference Line** | Analytics pane (left) → drag "Constant Line" to X-axis → Value: `2025` → Style: dashed red → Label: "Present" |
| **Marks → Tooltip** | `Year: <approach_year>` then new line `Close Approaches: <CNT(designation)>` |
| **Add Markers** | Right-click line → Show Markers |

---

## Chart 1.4 — Speed Category Bar (Close Approaches Dataset)

| Setting | Value |
|---------|-------|
| **Data Source** | `close_approaches_clean` |
| **Worksheet Name** | `Speed Category Overview` |
| **Rows** | Drag `speed_category` |
| **Columns** | Drag `designation` → Count |
| **Sort** | Manual: Slow (<5 km/s), Moderate (5–15 km/s), Fast (15–30 km/s), Very Fast (>30 km/s) |
| **Marks → Color** | Drag `speed_category` to Color → Slow=`#2CA02C`, Moderate=`#FFDD57`, Fast=`#FF7F0E`, Very Fast=`#D62728` |
| **Marks → Label** | Show mark labels (count) |
| **Marks → Tooltip** | `Speed: <speed_category>` then new line `Count: <CNT(designation)>` then new line `Share: <% of Total CNT(designation)>` |

---

## Dashboard 1 Layout & Assembly

```
┌───────────────────────┬─────────────────────┐
│  Risk Tier Bar (1.1)  │  Orbit Class Pie    │
│  [NEA data]           │  (1.2) [NEA data]   │
├───────────────────────┴─────────────────────┤
│     Annual Approach Line (1.3) [CA data]    │
├───────────────────────────────────────────────┤
│     Speed Category Bar (1.4) [CA data]      │
└───────────────────────────────────────────────┘
```

**Filters to show:**
- `risk_tier` → Multi-select dropdown (applies to NEA sheets)
- `speed_category` → Multi-select checkboxes (applies to CA sheets)

**Optional Extension:** Add **Filter Bookmarks** at bottom

---

# DASHBOARD 2: Hazard Analysis & Velocity Deep Dive

**Goal:** Physical/orbital properties of dangerous asteroids + velocity patterns of approaches.

---

## Chart 2.1 — MOID Histogram (NEA Dataset)

| Setting | Value |
|---------|-------|
| **Data Source** | `nea_catalogue_clean` |
| **Worksheet Name** | `MOID Distribution` |
| **Columns** | Drag `[MOID Bin]` (the bin you created, size 0.01) |
| **Rows** | Drag `spk_id` → Count Distinct |
| **Filter** | Drag `min_orbit_intersection_dist_au` to Filters → Range of values → 0 to 0.5 |
| **Marks → Color** | Drag `is_potentially_hazardous` to Color → True=`#D62728`, False=`#1F77B4` |
| **Reference Line** | Analytics → drag "Constant Line" to X-axis → Value: `0.05` → dashed orange → Label: "PHA Threshold (0.05 AU)" |
| **Marks → Tooltip** | `MOID Range: <MOID Bin> AU` then new line `Count: <CNTD(spk_id)>` then new line `PHA: <is_potentially_hazardous>` |
| **X-axis title** | "Minimum Orbit Intersection Distance (AU)" |
| **Y-axis title** | "Number of Asteroids" |

---

## Chart 2.2 — Hazard Quadrant Scatter (NEA Dataset)

| Setting | Value |
|---------|-------|
| **Data Source** | `nea_catalogue_clean` |
| **Worksheet Name** | `Hazard Quadrant` |
| **Columns** | Drag `min_orbit_intersection_dist_au` (continuous green pill) |
| **Rows** | Drag `absolute_magnitude_h` (continuous green pill) |
| **Y-axis** | Right-click Y-axis → Edit Axis → check **Reversed** (low H = big asteroid = top) |
| **X-axis range** | Right-click → Edit Axis → Fixed: 0 to 0.3 |
| **Mark Type** | Circle |
| **Marks → Color** | Drag `risk_tier` → Critical=`#D62728`, High=`#FF7F0E`, Moderate=`#FFDD57`, Low=`#2CA02C` |
| **Marks → Size** | Drag `[Display Size]` (calc field = 30 - H). Adjust slider |
| **Marks → Detail** | Drag `full_name` |
| **Marks → Tooltip** | `<full_name>` then new line `MOID: <min_orbit_intersection_dist_au> AU` then new line `H Magnitude: <absolute_magnitude_h>` then new line `Risk: <risk_tier>` |
| **Reference Line 1** | Analytics → Constant Line on X-axis → `0.05` → dashed orange → "MOID Threshold" |
| **Reference Line 2** | Analytics → Constant Line on Y-axis → `22` → dashed gray → "H Magnitude Threshold" |
| **Insight** | Top-left quadrant = biggest + closest = most dangerous |

---

## Chart 2.3 — Velocity Distribution Histogram (Close Approaches Dataset)

| Setting | Value |
|---------|-------|
| **Data Source** | `close_approaches_clean` |
| **Worksheet Name** | `Velocity Distribution` |
| **Columns** | Drag `[Velocity Bin]` (bin size 2 km/s) |
| **Rows** | Drag `designation` → Count |
| **Marks → Color** | Drag `speed_category` → Very Fast=`#D62728`, Fast=`#FF7F0E`, Moderate=`#FFDD57`, Slow=`#2CA02C` |
| **Stacking** | Menu → Analysis → Stack Marks → On |
| **Marks → Tooltip** | `Velocity: <Velocity Bin> km/s` then new line `Category: <speed_category>` then new line `Count: <CNT(designation)>` |
| **X-axis title** | "Approach Velocity (km/s)" |
| **Y-axis title** | "Number of Approaches" |

---

## Chart 2.4 — Distance vs Velocity Scatter (Close Approaches Dataset)

| Setting | Value |
|---------|-------|
| **Data Source** | `close_approaches_clean` |
| **Worksheet Name** | `Distance vs Velocity` |
| **Columns** | Drag `velocity_km_s` (continuous) |
| **Rows** | Drag `distance_lunar_distances` (continuous) |
| **Y-axis** | Right-click → Edit Axis → check **Logarithmic** (spread out clusters) |
| **Mark Type** | Circle |
| **Marks → Color** | Drag `speed_category` → same 4-color map |
| **Marks → Size** | Fixed small size OR drag `absolute_magnitude` (inverted) |
| **Marks → Detail** | Drag `full_name`, `close_approach_date` |
| **Marks → Tooltip** | `<full_name>` then new line `Date: <close_approach_date>` then new line `Distance: <distance_lunar_distances> LD` then new line `Speed: <velocity_km_s> km/s` |
| **Filter** | Drag `approach_year` → Range: 2015–2024 (historical only) |
| **Performance tip** | If slow: filter to `is_very_close_approach = True` |

---

## Dashboard 2 Layout & Assembly

```
┌───────────────────────┬─────────────────────┐
│ MOID Histogram (2.1)  │ Hazard Quadrant     │
│ [NEA data]            │ (2.2) [NEA data]    │
├───────────────────────┼─────────────────────┤
│ Velocity Histogram    │ Dist vs Vel Scatter  │
│ (2.3) [CA data]       │ (2.4) [CA data]     │
└───────────────────────┴─────────────────────┘
```

**Filters:**
- `risk_tier` → Multi-select (NEA sheets)
- `speed_category` → Multi-select (CA sheets)
- `is_potentially_hazardous` → Toggle (NEA sheets)

**Extension:** Add **Export All** at bottom-right → users can select scatter points → export data

---

# DASHBOARD 3: Observation Quality & Seasonal Patterns

**Goal:** Data quality of asteroid tracking + seasonal trends in close approaches.

---

## Chart 3.1 — Observation Span Box Plot (NEA Dataset)

| Setting | Value |
|---------|-------|
| **Data Source** | `nea_catalogue_clean` |
| **Worksheet Name** | `Observation Span Comparison` |
| **Columns** | Drag `is_potentially_hazardous` (discrete blue pill) |
| **Rows** | Drag `observation_span_years` (continuous green pill) |
| **Mark Type** | Circle |
| **Box Plot** | Analytics pane → drag "Box Plot" → drop on "Cell" |
| **Marks → Color** | Drag `is_potentially_hazardous` → True=`#D62728`, False=`#1F77B4` |
| **Marks → Tooltip** | `PHA: <is_potentially_hazardous>` then new line `Obs Span: <observation_span_years> years` |
| **Y-axis title** | "Observation Span (Years)" |
| **Insight** | PHAs are tracked longer — more observation data = higher confidence |

---

## Chart 3.2 — Size Category Treemap (NEA Dataset)

| Setting | Value |
|---------|-------|
| **Data Source** | `nea_catalogue_clean` |
| **Worksheet Name** | `Size Category Treemap` |
| **Mark Type** | Change to **Square** (creates treemap) |
| **Marks → Size** | Drag `spk_id` → Count Distinct |
| **Marks → Color** | Drag `size_category` → Large=`#D62728`, Medium=`#FF7F0E`, Small=`#00D2FF` |
| **Marks → Label** | Drag `size_category` AND `CNTD(spk_id)` to Label |
| **Marks → Tooltip** | `Size: <size_category>` then new line `Count: <CNTD(spk_id)>` |

---

## Chart 3.3 — Monthly Heatmap (Close Approaches Dataset)

| Setting | Value |
|---------|-------|
| **Data Source** | `close_approaches_clean` |
| **Worksheet Name** | `Monthly Heatmap` |
| **Columns** | Drag `approach_year` (discrete) |
| **Rows** | Drag `approach_month_name` (discrete) |
| **Rows sort** | Right-click `approach_month_name` → Sort → Manual → January, February, ... December |
| **Mark Type** | Square |
| **Marks → Color** | Drag `designation` → Count → Color becomes gradient → click Color → Edit Colors → Sequential: Blue-Teal |
| **Marks → Label** | Drag `designation` → Count → number shows inside each cell |
| **Marks → Size** | Maximize slider so squares fill cells |
| **Marks → Tooltip** | `<approach_month_name> <approach_year>` then new line `Approaches: <CNT(designation)>` |
| **Insight** | Reveals seasonal observation patterns and peak months |

---

## Chart 3.4 — Very Close Approach Yearly Stacked Bar (Close Approaches Dataset)

| Setting | Value |
|---------|-------|
| **Data Source** | `close_approaches_clean` |
| **Worksheet Name** | `Close vs Normal by Year` |
| **Columns** | Drag `approach_year` (discrete) |
| **Rows** | Drag `designation` → Count |
| **Marks → Color** | Drag `is_very_close_approach` → True=`#D62728`, False=`#1F77B4` |
| **Stacking** | Analysis → Stack Marks → On |
| **Marks → Label** | Show mark labels for totals: Analysis → Totals → Show Column Grand Totals |
| **Marks → Tooltip** | `Year: <approach_year>` then new line `Very Close (<10 LD): <is_very_close_approach>` then new line `Count: <CNT(designation)>` |
| **X-axis title** | "Year" |
| **Y-axis title** | "Number of Approaches" |

---

## Dashboard 3 Layout & Assembly

```
┌───────────────────────┬─────────────────────┐
│ Obs Span Box Plot     │ Size Treemap        │
│ (3.1) [NEA data]      │ (3.2) [NEA data]    │
├───────────────────────┴─────────────────────┤
│       Monthly Heatmap (3.3) [CA data]       │
├─────────────────────────────────────────────┤
│  Close vs Normal Stacked Bar (3.4) [CA data]│
└─────────────────────────────────────────────┘
```

**Filters:**
- `is_potentially_hazardous` → Toggle (NEA sheets)
- `orbit_class_label` → Dropdown (NEA sheets)
- `approach_year` → Range slider (CA sheets)
- `is_very_close_approach` → Toggle (CA sheets)

---

# DASHBOARD 4: Future Risk Forecast & Asteroid Profiling

**Goal:** Upcoming dangerous approaches + physical profile of the asteroid catalogue.

---

## Chart 4.1 — Eccentricity vs Semi-Major Axis Scatter (NEA Dataset)

| Setting | Value |
|---------|-------|
| **Data Source** | `nea_catalogue_clean` |
| **Worksheet Name** | `Orbital Scatter` |
| **Columns** | Drag `semi_major_axis_au` (continuous green pill) |
| **Rows** | Drag `orbital_eccentricity` (continuous green pill) |
| **X-axis** | Right-click → Edit Axis → Fixed Range: 0 to 4. Title: "Semi-Major Axis (AU)" |
| **Y-axis** | Fixed Range: 0 to 1. Title: "Orbital Eccentricity" |
| **Mark Type** | Circle |
| **Marks → Color** | Drag `is_potentially_hazardous` → True=`#D62728`, False=`#00D2FF` → set opacity to 50% (click Color → slider) |
| **Marks → Size** | Drag `[Display Size]` calc field. Adjust slider to small-medium |
| **Marks → Detail** | Drag `full_name`, `risk_tier`, `min_orbit_intersection_dist_au` |
| **Marks → Tooltip** | `<full_name>` then new line `SMA: <semi_major_axis_au> AU` then new line `Eccentricity: <orbital_eccentricity>` then new line `MOID: <min_orbit_intersection_dist_au> AU` then new line `Risk: <risk_tier>` |
| **Reference Line** | Analytics → Constant Line on X-axis → `1.0` → green dashed → Label: "Earth Orbit" |

---

## Chart 4.2 — KPI Tiles (NEA Dataset)

Build 3 separate mini worksheets, each showing one number:

| KPI Tile | Column | Aggregation | Font Color | Subtitle |
|----------|--------|-------------|------------|----------|
| **Total NEAs** | `spk_id` | Count Distinct | `#00D2FF` | "Total NEAs Tracked" |
| **PHAs** | `[PHA Count]` | SUM | `#D62728` | "Potentially Hazardous" |
| **Median MOID** | `min_orbit_intersection_dist_au` | MEDIAN → format `0.000 AU` | `#FF7F0E` | "Median MOID" |

**How:** New sheet → drag measure to Text on Marks card → change aggregation → Format font 36pt bold. Place all 3 in a horizontal container on the dashboard.

---

## Chart 4.3 — Future Danger Map Scatter (Close Approaches Dataset)

| Setting | Value |
|---------|-------|
| **Data Source** | `close_approaches_clean` |
| **Worksheet Name** | `Future Danger Map` |
| **Columns** | Drag `close_approach_date` → right-click → **Exact Date** (continuous green pill) |
| **Rows** | Drag `distance_lunar_distances` (continuous) |
| **Y-axis** | Right-click → Edit Axis → check **Reversed** (closer to Earth = higher up) |
| **Filter** | Drag `approach_year` to Filters → Range: 2025 to 2035 |
| **Mark Type** | Circle |
| **Marks → Color** | Drag `speed_category` → Very Fast=`#D62728`, Fast=`#FF7F0E`, Moderate=`#FFDD57`, Slow=`#2CA02C` |
| **Marks → Size** | Drag `[Danger Score]` calc field. Adjust slider |
| **Marks → Detail** | Drag `full_name`, `velocity_km_s` |
| **Marks → Tooltip** | `<full_name>` then new line `Date: <close_approach_date>` then new line `Distance: <distance_lunar_distances> LD` then new line `Speed: <velocity_km_s> km/s` then new line `Category: <speed_category>` |
| **Reference Line** | Analytics → Constant Line on Y-axis → `10` → red dashed → Label: "Very Close Threshold (10 LD)" |
| **X-axis title** | "Close Approach Date" |
| **Y-axis title** | "Distance (Lunar Distances) — Inverted" |

---

## Chart 4.4 — Top 20 Closest Future Approaches Table (Close Approaches Dataset)

| Setting | Value |
|---------|-------|
| **Data Source** | `close_approaches_clean` |
| **Worksheet Name** | `Top 20 Nearest Future` |
| **Rows** | Drag these in order: `full_name`, `close_approach_date`, `distance_lunar_distances`, `velocity_km_s`, `speed_category` |
| **Filter 1** | Drag `approach_year` → Range: 2025 to 2035 |
| **Sort** | Right-click `distance_lunar_distances` header → Sort → Ascending |
| **Filter 2 (Top 20)** | Drag `full_name` to Filters → Top tab → "By field" → Top `20` by `distance_lunar_distances` **Minimum** |
| **Conditional Color** | Right-click `distance_lunar_distances` column → Format → Color → if <1 = red bg, <5 = orange bg, <10 = yellow bg |
| **Marks → Tooltip** | Default table tooltip is fine |
| **Dynamic Top N (optional)** | Create Parameter "Top N" (integer, default 20, range 5–100). Replace hard-coded 20 with `[Top N]` parameter. This is where **Data-Driven Parameters** extension helps |

---

## Dashboard 4 Layout & Assembly

```
┌──────────┬──────────┬──────────┐
│ KPI Tile │ KPI Tile │ KPI Tile │  ← NEA KPIs (4.2), height ~80px
├──────────┴──────────┴──────────┤
│ Orbital Scatter (4.1) [NEA]    │  ← ~300px height
├───────────────────────┬────────┤
│ Future Danger Map     │ Top 20 │
│ Scatter (4.3) [CA]    │ Table  │
│                       │ (4.4)  │
│                       │ [CA]   │
└───────────────────────┴────────┘
```

**Filters:**
- `approach_year` → Range slider 2025–2035 (CA sheets)
- `speed_category` → Multi-select (CA sheets)
- `risk_tier` → Multi-select (NEA sheets)

**Extensions:**
1. **Data-Driven Parameters** → wired to "Top N" parameter for table (4.4)
2. **Export All** → bottom-right corner → export scatter/table data

---

## Summary: What Each Dashboard Contains

| Dashboard | NEA Chart 1 | NEA Chart 2 | CA Chart 1 | CA Chart 2 |
|-----------|------------|------------|-----------|-----------|
| **1: Executive Overview** | Risk Tier Bar | Orbit Class Pie | Annual Timeline Line | Speed Category Bar |
| **2: Hazard & Velocity** | MOID Histogram | Hazard Quadrant Scatter | Velocity Histogram | Dist vs Vel Scatter |
| **3: Quality & Seasonal** | Obs Span Box Plot | Size Treemap | Monthly Heatmap | Close vs Normal Bar |
| **4: Future Forecast** | Orbital Scatter + KPIs | (KPIs count as 2nd) | Future Danger Map | Top 20 Table |

---

## Publishing Checklist

1. **File → Save to Tableau Public** (free account at public.tableau.com)
2. All 4 dashboards visible as tabs. Hide raw worksheet tabs (right-click → Hide)
3. Verify all filters work in published URL (test in incognito browser)
4. Export screenshots (1920×1080) → save to `tableau/screenshots/`
5. Paste public URL into `tableau/dashboard_links.md` and `README.md`
