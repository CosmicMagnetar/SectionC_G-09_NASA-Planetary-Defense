# Tableau 4-Dashboard Complete Build Guide

**NST DVA Capstone 2 · Team SectionC_G-09 · NASA Planetary Defense**

---

## Data Sources

| # | File | Rows | Dashboards |
|---|------|------|------------|
| 1 | `nea_catalogue_clean.csv` | ~41,000 | Dashboard 1 & 2 |
| 2 | `close_approaches_clean.csv` | ~95,000 | Dashboard 3 & 4 |

**Setup:** Tableau Public → Connect → Text File → select each CSV. **Do NOT join them.** Two separate data sources.

---

## Extensions to Install (from Dashboard → Extensions → Gallery)

| Extension | Publisher | Purpose | Dashboards |
|-----------|----------|---------|------------|
| **Export All** | Tableau | Users can download filtered data as CSV/Excel | 2 & 4 |
| **Data-Driven Parameters** | Tableau | Dynamic "Top N" slider auto-updates from data | 4 |
| **Filter Bookmarks** | Tableau | Save/reload filter presets (optional) | 1 |

**How to add:** Dashboard tab → Objects panel (left) → drag "Extension" onto canvas → "Extension Gallery" → search name → "Add to Dashboard".

---

## Calculated Fields to Create First

Open each data source and create these before building any sheet.

### In `nea_catalogue_clean` data source:

```
FIELD: [PHA Count]
Formula: IF [Is Potentially Hazardous] = "True" THEN 1 ELSE 0 END
Purpose: Integer flag for summing PHA asteroids in KPIs

FIELD: [Size Proxy]
Formula:
IF [Absolute Magnitude H] <= 18 OR [Diameter Km] >= 1 THEN "Large (≥1 km)"
ELSEIF [Absolute Magnitude H] <= 22 THEN "Medium (140m–1km)"
ELSE "Small (<140m)"
END
Purpose: Three-tier size category for filtering and coloring

FIELD: [Display Size]
Formula: 30 - [Absolute Magnitude H]
Purpose: Inverted magnitude for scatter bubble sizing (lower H = bigger dot)

FIELD: [MOID Bin]
How: Right-click "min_orbit_intersection_dist_au" → Create → Bins → Bin Size: 0.01
Purpose: For MOID histogram x-axis
```

### In `close_approaches_clean` data source:

```
FIELD: [Velocity Bin]
How: Right-click "velocity_km_s" → Create → Bins → Bin Size: 2
Purpose: For velocity histogram x-axis

FIELD: [Time Period]
Formula: IF [Approach Year] >= 2025 THEN "Future" ELSE "Historical" END
Purpose: Split historical vs future approaches

FIELD: [Danger Score]
Formula: (1 / [Distance Lunar Distances]) * [Velocity Km S]
Purpose: Composite risk metric for bubble sizing

FIELD: [Row Index]
Formula: INDEX()
Purpose: Used to limit "Top N" tables
```

---

## Color Palette (Use Consistently Across All 4 Dashboards)

| Element | Hex | Where Used |
|---------|-----|-----------|
| Critical / PHA True / Very Fast | `#D62728` | Red |
| High / Fast | `#FF7F0E` | Orange |
| Moderate | `#FFDD57` | Yellow |
| Low / Slow | `#2CA02C` | Green |
| Accent / Non-PHA | `#00D2FF` | Cyan |
| Baseline / Non-PHA default | `#1F77B4` | Blue |
| Background | `#1E1E2F` | Dark mode |

---

# DASHBOARD 1: Executive Hazard Overview

**Data Source:** `nea_catalogue_clean.csv`
**Goal:** How many NEAs exist? How many are dangerous? What types?

---

## Chart 1.1 — KPI: Total NEAs (Text Tile)

| Setting | Value |
|---------|-------|
| **New Worksheet name** | `KPI - Total NEAs` |
| **Marks Card → Text** | Drag `spk_id` → change aggregation to **Count Distinct** (right-click → Measure → Count Distinct) |
| **Format** | Click the Text mark → Edit → Font: 36pt, Bold, Color: `#00D2FF` |
| **Subtitle** | Below the number, add text "Total NEAs" in 12pt, gray `#A0A0B0` |
| **Tooltip** | Disable (uncheck "Include command buttons") |
| **Rows/Columns** | Leave empty — just the text mark |

---

## Chart 1.2 — KPI: Potentially Hazardous Count

| Setting | Value |
|---------|-------|
| **New Worksheet name** | `KPI - PHA Count` |
| **Marks Card → Text** | Drag calculated field `[PHA Count]` → aggregation **SUM** |
| **Format** | Font: 36pt, Bold, Color: `#D62728` (red) |
| **Subtitle** | "Potentially Hazardous" in 12pt gray |
| **Rows/Columns** | Leave empty |

---

## Chart 1.3 — KPI: Critical Risk Count

| Setting | Value |
|---------|-------|
| **New Worksheet name** | `KPI - Critical Count` |
| **Filter** | Drag `risk_tier` to Filters shelf → select only "Critical" |
| **Marks Card → Text** | Drag `spk_id` → Count Distinct |
| **Format** | Font: 36pt, Bold, Color: `#FF7F0E` (orange) |
| **Subtitle** | "Critical Risk Tier" in 12pt gray |

---

## Chart 1.4 — KPI: Median MOID

| Setting | Value |
|---------|-------|
| **New Worksheet name** | `KPI - Median MOID` |
| **Marks Card → Text** | Drag `min_orbit_intersection_dist_au` → change aggregation to **Median** |
| **Format** | Font: 36pt, Bold, Color: `#00D2FF`. Number format: `0.000` + suffix " AU" |
| **Subtitle** | "Median MOID" in 12pt gray |

---

## Chart 1.5 — Risk Tier Horizontal Bar

| Setting | Value |
|---------|-------|
| **New Worksheet name** | `Risk Tier Breakdown` |
| **Rows shelf** | Drag `risk_tier` |
| **Columns shelf** | Drag `spk_id` → aggregation: Count Distinct (CNTD) |
| **Marks Card → Color** | Drag `risk_tier` → click Color → Edit Colors → assign: Critical=`#D62728`, High=`#FF7F0E`, Moderate=`#FFDD57`, Low=`#2CA02C` |
| **Marks Card → Label** | Click Label → Show mark labels → check "Show" → format shows count value |
| **Sort** | Right-click `risk_tier` on Rows → Sort → Manual → order: Critical, High, Moderate, Low |
| **Tooltip** | Edit: `Risk Tier: <risk_tier> | Count: <CNTD(spk_id)> | % of Total: <% of Total CNTD(spk_id)>` |
| **Format** | Right-click chart → Format → Borders: None. Shading: None (transparent). Font: 11pt |
| **Fit** | Standard fit, bar width auto |

**How to add % of Total to tooltip:** In tooltip editor, click "Insert" → CNTD(spk_id) → then after inserting, right-click the pill that appears → "Quick Table Calculation" → "Percent of Total".

---

## Chart 1.6 — Orbit Class Pie/Donut

| Setting | Value |
|---------|-------|
| **New Worksheet name** | `Orbit Class Distribution` |
| **Mark Type** | Change dropdown from "Automatic" to **Pie** |
| **Marks Card → Angle** | Drag `spk_id` → Count Distinct |
| **Marks Card → Color** | Drag `orbit_class_label` → use auto-assigned palette or custom |
| **Marks Card → Label** | Drag `orbit_class_label` AND `CNTD(spk_id)`. Also add "% of Total" via Quick Table Calc |
| **Marks Card → Detail** | `orbit_class_label` (if not already there) |
| **Tooltip** | `Orbit Class: <orbit_class_label> | Count: <CNTD(spk_id)> | Share: <% of Total>` |
| **Size** | Make pie fill the view |

**Donut effect (optional):** Dual axis approach—add a second Rows axis with a MIN(0), make it a small white filled circle layered on top. Or just keep as a regular pie.

---

## Chart 1.7 — Size Category Treemap

| Setting | Value |
|---------|-------|
| **New Worksheet name** | `Size Category Treemap` |
| **Mark Type** | Change to **Square** (this creates a treemap) |
| **Marks Card → Size** | Drag `spk_id` → Count Distinct |
| **Marks Card → Color** | Drag `size_category` → assign: Large=`#D62728`, Medium=`#FF7F0E`, Small=`#00D2FF` |
| **Marks Card → Label** | Drag `size_category` AND `CNTD(spk_id)` |
| **Marks Card → Detail** | `size_category` |
| **Tooltip** | `Size: <size_category> | Count: <CNTD(spk_id)>` |

---

## Dashboard 1 Assembly

1. **New Dashboard** → Name: "Executive Hazard Overview" → Size: Automatic or 1920×1080
2. Layout (drag sheets from left panel):

```
┌──────────┬──────────┬──────────┬──────────┐
│ KPI 1.1  │ KPI 1.2  │ KPI 1.3  │ KPI 1.4  │  ← Horizontal container, height ~100px
├──────────┴──────────┼──────────┴──────────┤
│ Risk Tier Bar (1.5) │ Orbit Class Pie(1.6)│  ← 50/50 split
├─────────────────────┴─────────────────────┤
│        Size Category Treemap (1.7)        │  ← Full width bottom
└───────────────────────────────────────────┘
```

3. **Add Filters** (from any sheet, right-click → Show Filter):
   - `risk_tier` → show as Multi-select dropdown → Apply to: All Using This Data Source
   - `orbit_class_label` → show as Dropdown → Apply to: All Using This Data Source
   - `is_potentially_hazardous` → show as Single Value (toggle)

4. **Optional Extension:** Drag "Extension" object → add **Filter Bookmarks** from gallery

---

# DASHBOARD 2: Orbital Mechanics Deep Dive

**Data Source:** `nea_catalogue_clean.csv`
**Goal:** Visualize the physics of PHAs — orbit shapes, distances, magnitudes.

---

## Chart 2.1 — MOID Histogram

| Setting | Value |
|---------|-------|
| **New Worksheet name** | `MOID Distribution` |
| **Columns shelf** | Drag the `[MOID Bin]` you created (binned `min_orbit_intersection_dist_au`, size 0.01) |
| **Rows shelf** | Drag `spk_id` → Count Distinct |
| **Filter** | Drag `min_orbit_intersection_dist_au` to Filters → Range → 0 to 0.5 (cuts off long tail) |
| **Marks Card → Color** | Drag `is_potentially_hazardous` → True=`#D62728`, False=`#1F77B4` |
| **Reference Line** | Go to Analytics pane (left panel) → drag "Constant Line" onto the x-axis → Value: `0.05` → Line: dashed, orange. Label: "PHA Threshold (0.05 AU)" |
| **Tooltip** | `MOID Range: <MOID Bin> | Count: <CNTD(spk_id)> | PHA: <is_potentially_hazardous>` |
| **X-axis title** | "MOID (AU)" |
| **Y-axis title** | "Number of Asteroids" |

---

## Chart 2.2 — Eccentricity vs Semi-Major Axis Scatter

| Setting | Value |
|---------|-------|
| **New Worksheet name** | `Orbital Scatter` |
| **Columns shelf** | Drag `semi_major_axis_au` (keep as continuous/green) |
| **Rows shelf** | Drag `orbital_eccentricity` (keep as continuous/green) |
| **Marks Card → Mark Type** | Circle |
| **Marks Card → Color** | Drag `is_potentially_hazardous` → True=`#D62728`, False=`#00D2FF`. Set opacity to 50% |
| **Marks Card → Size** | Drag `[Display Size]` calculated field (= 30 - H). Adjust slider to small-medium range |
| **Marks Card → Detail** | Drag `full_name`, `risk_tier`, `min_orbit_intersection_dist_au` |
| **Marks Card → Tooltip** | Edit: `<full_name> | SMA: <semi_major_axis_au> AU | Ecc: <orbital_eccentricity> | MOID: <min_orbit_intersection_dist_au> AU | Risk: <risk_tier>` |
| **X-axis** | Right-click → Edit Axis → Range: Fixed, 0 to 4. Title: "Semi-Major Axis (AU)" |
| **Y-axis** | Range: 0 to 1. Title: "Orbital Eccentricity" |
| **Reference Line** | Analytics → Constant Line on X-axis → Value: `1.0` → green dashed → Label: "Earth Orbit" |
| **Performance** | If >40K marks is slow: add `spk_id` to filter → Sample → check "Sample data" |

---

## Chart 2.3 — Observation Span Box Plot

| Setting | Value |
|---------|-------|
| **New Worksheet name** | `Observation Span Comparison` |
| **Columns shelf** | Drag `is_potentially_hazardous` (discrete/blue) |
| **Rows shelf** | Drag `observation_span_years` (continuous/green) |
| **Mark Type** | Circle |
| **Add Box Plot** | Analytics pane → drag "Box Plot" onto the view → drop on "Cell" |
| **Marks Card → Color** | Drag `is_potentially_hazardous` → True=`#D62728`, False=`#1F77B4` |
| **Tooltip** | `PHA: <is_potentially_hazardous> | Observation Span: <observation_span_years> years` |
| **Y-axis title** | "Observation Span (Years)" |
| **X-axis title** | "Is Potentially Hazardous" |
| **Insight** | PHAs have longer observation arcs — they are tracked more carefully |

---

## Chart 2.4 — Hazard Quadrant (Magnitude vs MOID)

| Setting | Value |
|---------|-------|
| **New Worksheet name** | `Hazard Quadrant` |
| **Columns shelf** | Drag `min_orbit_intersection_dist_au` (continuous) |
| **Rows shelf** | Drag `absolute_magnitude_h` (continuous) |
| **Rows axis** | Right-click → Edit Axis → check **"Reversed"** (so low H / big asteroids are at TOP) |
| **X-axis range** | Fixed: 0 to 0.3 |
| **Marks Card → Mark Type** | Circle |
| **Marks Card → Color** | Drag `risk_tier` → Critical=`#D62728`, High=`#FF7F0E`, Moderate=`#FFDD57`, Low=`#2CA02C` |
| **Marks Card → Size** | Small fixed size or use `[Display Size]` |
| **Marks Card → Detail** | `full_name` |
| **Marks Card → Tooltip** | `<full_name> | MOID: <min_orbit_intersection_dist_au> AU | H: <absolute_magnitude_h> | Risk: <risk_tier>` |
| **Reference Line 1** | Analytics → Constant Line on X-axis → Value: `0.05` → dashed orange → "MOID Threshold" |
| **Reference Line 2** | Analytics → Constant Line on Y-axis → Value: `22` → dashed gray → "H Magnitude Threshold" |
| **Insight** | Top-left quadrant = most dangerous (large asteroid + close to Earth) |

---

## Dashboard 2 Assembly

```
┌───────────────────────┬─────────────────────┐
│ MOID Histogram (2.1)  │ Obs Span Box (2.3)  │
├───────────────────────┼─────────────────────┤
│ Orbital Scatter (2.2) │ Hazard Quadrant(2.4)│
└───────────────────────┴─────────────────────┘
```

**Filters:** `risk_tier` (multi-select), `orbit_class_label` (dropdown), `size_category` (multi-select). Apply to all sheets.

**Extension:** Drag Extension object → add **Export All** → place in bottom-right corner. Users select points on scatter → click Export All → download CSV.

---

# DASHBOARD 3: Historical Close Approach Timeline

**Data Source:** `close_approaches_clean.csv`
**Goal:** Frequency, velocity, and seasonal patterns of past approaches.

---

## Chart 3.1 — Annual Approach Count (Line)

| Setting | Value |
|---------|-------|
| **New Worksheet name** | `Annual Timeline` |
| **Columns shelf** | Drag `approach_year` → right-click → change to **Discrete** (blue pill) |
| **Rows shelf** | Drag `designation` → aggregation: Count (CNT) |
| **Mark Type** | Line |
| **Marks Card → Color** | Single fixed color: `#00D2FF` |
| **Marks Card → Label** | Check "Show mark labels" → shows count per year |
| **Marks Card → Size** | Increase line thickness to ~2px |
| **Reference Line** | Analytics → Constant Line on X-axis → Value: `2025` → red dashed → Label: "Present (2025)" |
| **Tooltip** | `Year: <approach_year> | Approaches: <CNT(designation)>` |
| **X-axis title** | "Year" |
| **Y-axis title** | "Number of Close Approaches" |
| **Marks** | Right-click line → "Show Markers" to add dots on each year |

---

## Chart 3.2 — Velocity Distribution Histogram

| Setting | Value |
|---------|-------|
| **New Worksheet name** | `Velocity Distribution` |
| **Columns shelf** | Drag `[Velocity Bin]` (the bin you created, size 2 km/s) |
| **Rows shelf** | Drag `designation` → Count |
| **Marks Card → Color** | Drag `speed_category` → assign: Very Fast=`#D62728`, Fast=`#FF7F0E`, Moderate=`#FFDD57`, Slow=`#00D2FF` |
| **Color legend sort** | Right-click legend → "Edit Alias" if needed. Manual sort: Slow, Moderate, Fast, Very Fast |
| **Stacking** | Marks Card → Analysis menu → ensure "Stack Marks" → On |
| **Tooltip** | `Velocity Range: <Velocity Bin> km/s | Category: <speed_category> | Count: <CNT(designation)>` |
| **X-axis title** | "Approach Velocity (km/s)" |
| **Y-axis title** | "Count" |

---

## Chart 3.3 — Monthly Heatmap (Highlight Table)

| Setting | Value |
|---------|-------|
| **New Worksheet name** | `Monthly Heatmap` |
| **Columns shelf** | Drag `approach_year` (discrete) |
| **Rows shelf** | Drag `approach_month_name` (discrete) |
| **Rows sort** | Right-click `approach_month_name` → Sort → Manual → order: January through December |
| **Mark Type** | Square |
| **Marks Card → Color** | Drag `designation` → Count → Color becomes a gradient. Click Color → Edit → Sequential palette: Blue-Teal or Orange-Red |
| **Marks Card → Label** | Drag `designation` → Count → shows number in each cell |
| **Marks Card → Size** | Max out the slider so squares fill cells |
| **Tooltip** | `<approach_month_name> <approach_year> | Approaches: <CNT(designation)>` |
| **Insight** | Reveals observation bias and seasonal patterns |

---

## Chart 3.4 — Distance vs Velocity Scatter

| Setting | Value |
|---------|-------|
| **New Worksheet name** | `Distance vs Velocity` |
| **Columns shelf** | Drag `velocity_km_s` (continuous) |
| **Rows shelf** | Drag `distance_lunar_distances` (continuous) |
| **Filter** | Drag `approach_year` to Filters → Range: 2015 to 2024 (historical only) |
| **Marks Card → Mark Type** | Circle |
| **Marks Card → Color** | Drag `speed_category` → same 4-color map |
| **Marks Card → Size** | Drag `absolute_magnitude` → reverse meaning: adjust size range so small H = large dot |
| **Marks Card → Detail** | `full_name`, `close_approach_date` |
| **Marks Card → Tooltip** | `<full_name> | Date: <close_approach_date> | Distance: <distance_lunar_distances> LD | Speed: <velocity_km_s> km/s` |
| **Y-axis** | Consider log scale: right-click → Edit Axis → check "Logarithmic" |
| **Performance** | Use sampling or filter to `is_very_close_approach = True` for a focused view |

---

## Dashboard 3 Assembly

```
┌─────────────────────────────────────────────┐
│        Annual Approach Line (3.1)           │  ← Full width, height ~250px
├───────────────────────┬─────────────────────┤
│ Velocity Histogram    │ Monthly Heatmap     │
│ (3.2)                 │ (3.3)               │
├───────────────────────┴─────────────────────┤
│     Distance vs Velocity Scatter (3.4)      │  ← Full width bottom
└─────────────────────────────────────────────┘
```

**Filters (show as interactive):**
- `speed_category` → Multi-select checkboxes → Apply to all sheets
- `is_very_close_approach` → Single value toggle (True/False)
- `approach_year` → Range slider (2015–2035)

---

# DASHBOARD 4: Future Risk Forecast (2025–2035)

**Data Source:** `close_approaches_clean.csv`
**Goal:** Prioritize upcoming dangerous close approaches.

---

## Chart 4.1 — Future Danger Map (Scatter)

| Setting | Value |
|---------|-------|
| **New Worksheet name** | `Future Danger Map` |
| **Columns shelf** | Drag `close_approach_date` → right-click → change to **Exact Date** (continuous green) |
| **Rows shelf** | Drag `distance_lunar_distances` (continuous) |
| **Rows axis** | Right-click → Edit Axis → check **"Reversed"** (closer to Earth = HIGHER on chart) |
| **Filter** | Drag `approach_year` to Filters → Range: 2025 to 2035 |
| **Marks Card → Mark Type** | Circle |
| **Marks Card → Color** | Drag `speed_category` → Very Fast=`#D62728`, Fast=`#FF7F0E`, Moderate=`#FFDD57`, Slow=`#00D2FF` |
| **Marks Card → Size** | Drag `[Danger Score]` or `absolute_magnitude` (inverted) |
| **Marks Card → Detail** | `full_name`, `velocity_km_s` |
| **Marks Card → Tooltip** | `<full_name> | Date: <close_approach_date> | Distance: <distance_lunar_distances> LD | Speed: <velocity_km_s> km/s | Category: <speed_category>` |
| **Reference Line** | Analytics → Constant Line on Y-axis → Value: `10` → red dashed → Label: "Very Close (<10 LD)" |
| **X-axis title** | "Close Approach Date" |
| **Y-axis title** | "Distance from Earth (Lunar Distances) — Reversed" |

---

## Chart 4.2 — Top 20 Closest Future Approaches (Table)

| Setting | Value |
|---------|-------|
| **New Worksheet name** | `Top 20 Nearest` |
| **Mark Type** | Text (automatic for tables) |
| **Rows shelf** | Drag: `full_name`, `close_approach_date`, `distance_lunar_distances`, `velocity_km_s`, `speed_category` |
| **Filter 1** | `approach_year` → Range: 2025 to 2035 |
| **Sort** | Right-click `distance_lunar_distances` on Rows → Sort → Ascending |
| **Filter 2 (Top N)** | Drag `[Row Index]` to Filters → add as table calc → range 1 to 20. OR: drag `full_name` to Filters → Top tab → By field → Top 20 by `distance_lunar_distances` Minimum |
| **Conditional Format** | Right-click `distance_lunar_distances` column → Format → Conditional: <1 = red bg, <5 = orange bg, <10 = yellow bg |
| **Column widths** | Adjust to fit: Name ~200px, Date ~120px, Distance ~80px, Velocity ~80px, Category ~120px |
| **Tooltip** | Default is fine for tables |

**For dynamic Top N:** Create a Parameter: Name="Top N", Type=Integer, Current=20, Range 5–100. Then use `[Row Index]` <= [Top N] as a filter. This is where the **Data-Driven Parameters** extension helps.

---

## Chart 4.3 — Future Yearly Forecast (Stacked Bar)

| Setting | Value |
|---------|-------|
| **New Worksheet name** | `Future Yearly Forecast` |
| **Columns shelf** | Drag `approach_year` (discrete) |
| **Rows shelf** | Drag `designation` → Count |
| **Filter** | `approach_year` → Range: 2025 to 2035 |
| **Marks Card → Color** | Drag `is_very_close_approach` → True=`#D62728` (red), False=`#1F77B4` (blue) |
| **Stacking** | Analysis → Stack Marks → On (stacked bars) |
| **Marks Card → Label** | Show mark labels with totals: Analysis → Totals → Show Column Grand Totals |
| **Tooltip** | `Year: <approach_year> | Very Close: <is_very_close_approach> | Count: <CNT(designation)>` |
| **X-axis title** | "Year" |
| **Y-axis title** | "Number of Approaches" |

---

## Chart 4.4 — Speed Category Breakdown by Year

| Setting | Value |
|---------|-------|
| **New Worksheet name** | `Speed Breakdown by Year` |
| **Columns shelf** | Drag `approach_year` (discrete, filtered 2025–2035) |
| **Rows shelf** | Drag `designation` → Count |
| **Mark Type** | Bar |
| **Marks Card → Color** | Drag `speed_category` → same 4-color scheme |
| **Stacking** | Stacked (default for bar with color dimension) |
| **Marks Card → Label** | Optional: show count per segment |
| **Tooltip** | `Year: <approach_year> | Speed: <speed_category> | Count: <CNT(designation)>` |
| **Insight** | Shows if future approaches are trending faster or slower |

---

## Dashboard 4 Assembly

```
┌─────────────────────────────────────────────┐
│     Future Yearly Forecast Bar (4.3)        │  ← Compact, height ~180px
├───────────────────────┬─────────────────────┤
│                       │                     │
│  Future Danger Map    │  Top 20 Closest     │
│  Scatter (4.1)        │  Table (4.2)        │
│                       │                     │
├───────────────────────┴─────────────────────┤
│    Speed Category Breakdown (4.4)           │  ← Bottom bar, height ~200px
└─────────────────────────────────────────────┘
```

**Filters (show as interactive):**
- `approach_year` → Range slider (2025–2035)
- `speed_category` → Multi-select checkboxes
- `distance_lunar_distances` → Range slider

**Extensions:**
1. Drag "Extension" → add **Data-Driven Parameters** → wire to "Top N" parameter for the table
2. Drag "Extension" → add **Export All** → place in bottom-right → analysts can export the Top 20 table data

---

## Publishing Checklist

1. File → Save to Tableau Public (free account at public.tableau.com)
2. Ensure all 4 dashboards are separate tabs in the workbook
3. Right-click sheet tabs → "Hide" all raw worksheets (only show dashboard tabs)
4. Verify filters work in published version (incognito browser test)
5. Export screenshots (1920×1080) to `tableau/screenshots/`
6. Paste public URL into `tableau/dashboard_links.md` and `README.md`
