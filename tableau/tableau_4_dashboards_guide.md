# Tableau 4-Dashboard Build Guide — NASA Planetary Defense

**NST DVA Capstone 2 · Team SectionC_G-09**

---

## Data Sources (DO NOT JOIN)

| # | File | Rows | Used In |
|---|------|------|---------|
| 1 | `data/processed/nea_catalogue_clean.csv` | ~41,000 | Dashboard 1 & 2 |
| 2 | `data/processed/close_approaches_clean.csv` | ~95,000 | Dashboard 3 & 4 |

**Connection:** Tableau Desktop/Public → Connect → Text File → select each CSV separately. Keep as **two independent data sources**.

---

## Extensions / Addons to Install

Install these from **Dashboard → Extensions → Extension Gallery** (inside Tableau):

| Extension | Publisher | Why You Need It | Used In |
|-----------|-----------|----------------|---------|
| **Export All** | Tableau | Lets users download filtered data as CSV/Excel directly from the dashboard. Required for analyst workflows. | Dashboard 2 & 4 |
| **Data-Driven Parameters** | Tableau | Auto-updates parameter dropdown lists when the data changes (e.g., dynamic "Top N" slider). | Dashboard 4 |
| **Filter Bookmarks** | Tableau (optional) | Lets users save and reload filter presets. Nice-to-have for complex multi-filter dashboards. | Dashboard 1 (optional) |

> **How to add:** Open your dashboard tab → drag "Extension" object from the left panel → click "Extension Gallery" → search by name → click "Add".

---

## Calculated Fields (Create Before Building Sheets)

Create these in Tableau before building any sheets:

```
// CF-1: PHA Flag (Integer for KPI sums)
// Data Source: nea_catalogue_clean
IF [Is Potentially Hazardous] = "True" THEN 1 ELSE 0 END
→ Name: [PHA Count]

// CF-2: Size Proxy Category
// Data Source: nea_catalogue_clean
IF [Absolute Magnitude H] <= 18 OR [Diameter Km] >= 1 THEN "Large (≥1 km)"
ELSEIF [Absolute Magnitude H] <= 22 THEN "Medium (140m–1km)"
ELSE "Small (<140m)" END
→ Name: [Size Proxy]

// CF-3: MOID Bin (for histogram)
// Data Source: nea_catalogue_clean
// Use Tableau built-in: Right-click min_orbit_intersection_dist_au → Create → Bins → Size: 0.01

// CF-4: Velocity Bin (for histogram)
// Data Source: close_approaches_clean
// Right-click velocity_km_s → Create → Bins → Size: 2

// CF-5: Is Future Approach
// Data Source: close_approaches_clean
IF [Approach Year] >= 2025 THEN "Future" ELSE "Historical" END
→ Name: [Time Period]

// CF-6: Danger Score (for bubble sizing)
// Data Source: close_approaches_clean
(1 / [Distance Lunar Distances]) * [Velocity Km S]
→ Name: [Danger Score]
```

---

## DASHBOARD 1: Executive Hazard Overview

**Goal:** Answer "How many NEAs exist, how many are dangerous, and what types are they?"
**Data Source:** `nea_catalogue_clean.csv`

### Sheet 1.1 — KPI Banner (4 Text Tiles)

| KPI | Column(s) | Aggregation | Format |
|-----|-----------|-------------|--------|
| Total NEAs | `spk_id` | CNTD (Count Distinct) | `#,##0` |
| Potentially Hazardous | `[PHA Count]` (CF-1) | SUM | `#,##0` |
| Critical Risk | `risk_tier` | COUNTD where risk_tier = "Critical" | `#,##0` |
| Median MOID | `min_orbit_intersection_dist_au` | MEDIAN | `0.000 AU` |

**How to build each tile:**
1. New Worksheet → drag the measure to Text on Marks card
2. Format → Font size 36pt, bold, color `#00D2FF`
3. Add a subtitle label below (Font 12pt, gray)
4. Duplicate for each KPI

### Sheet 1.2 — Risk Tier Horizontal Bar Chart

| Property | Setting |
|----------|---------|
| **Rows** | `risk_tier` |
| **Columns** | `CNT(spk_id)` or `CNTD(spk_id)` |
| **Color** | Drag `risk_tier` to Color → assign: Critical=`#D62728`, High=`#FF7F0E`, Moderate=`#FFDD57`, Low=`#2CA02C` |
| **Sort** | Manual order: Critical → High → Moderate → Low |
| **Label** | Show mark labels (count + percentage of total) |
| **Tooltip** | `Risk Tier: <risk_tier>  |  Count: <CNT(spk_id)>  |  % of Total: <% of Total CNT(spk_id)>` |

### Sheet 1.3 — Orbit Class Donut Chart (Pie with hole)

| Property | Setting |
|----------|---------|
| **Angle** | `CNT(spk_id)` |
| **Color** | `orbit_class_label` (auto-palette or custom) |
| **Label** | `orbit_class_label` + `% of Total` |
| **Detail** | `orbit_class_label` |

**Donut trick:** Create a dual-axis pie. Second axis = a small white circle centered on top to create the hole effect. Or use a simple Pie chart (Tableau's built-in).

### Sheet 1.4 — Size Category Treemap

| Property | Setting |
|----------|---------|
| **Mark Type** | Square (Treemap) |
| **Size** | `CNT(spk_id)` |
| **Color** | `size_category` → assign warm tones for large, cool for small |
| **Label** | `size_category` + count |
| **Detail** | `size_category` |

### Dashboard 1 Assembly

```
┌─────────────────────────────────────────────┐
│  KPI 1  │  KPI 2  │  KPI 3  │  KPI 4       │  ← Top banner row
├───────────────────────┬─────────────────────┤
│                       │                     │
│  Risk Tier Bar Chart  │  Orbit Class Donut  │  ← Main row (50/50)
│                       │                     │
├───────────────────────┴─────────────────────┤
│          Size Category Treemap              │  ← Bottom row
└─────────────────────────────────────────────┘
```

**Filters (show as interactive controls):**
- `risk_tier` → Multi-select dropdown
- `orbit_class_label` → Multi-select dropdown
- `is_potentially_hazardous` → Single-value toggle

**Extension:** Optionally add **Filter Bookmarks** so users can save preset filter combos.

---

## DASHBOARD 2: Orbital Mechanics Deep Dive

**Goal:** Visualize the physics — MOID distribution, orbital shapes, and observation quality of PHAs vs non-PHAs.
**Data Source:** `nea_catalogue_clean.csv`

### Sheet 2.1 — MOID Histogram

| Property | Setting |
|----------|---------|
| **Columns** | `min_orbit_intersection_dist_au (bin)` — bin size `0.01`, filter range `0 to 0.5` |
| **Rows** | `CNT(spk_id)` |
| **Color** | `is_potentially_hazardous` → True=`#D62728`, False=`#1F77B4` |
| **Reference Line** | Constant line at X = `0.05` AU, dashed orange, label "PHA Threshold" |
| **Analytics** | Drag "Constant Line" from Analytics pane → set value 0.05 |

### Sheet 2.2 — Eccentricity vs Semi-Major Axis Scatter

| Property | Setting |
|----------|---------|
| **Columns** | `semi_major_axis_au` (continuous, range 0–4) |
| **Rows** | `orbital_eccentricity` (continuous, range 0–1) |
| **Color** | `is_potentially_hazardous` → True=`#D62728`, False=`#00D2FF` |
| **Size** | `absolute_magnitude_h` — reversed (lower H = bigger dot) or use `[Size Proxy]` |
| **Detail** | `full_name`, `risk_tier`, `min_orbit_intersection_dist_au` |
| **Tooltip** | Name, SMA, Eccentricity, MOID, Risk Tier, H magnitude |
| **Reference Line** | Vertical constant at X = `1.0` AU (Earth's orbit), green dashed |
| **Sampling** | If slow, use Tableau's built-in data sampling (Performance → reduce marks) |

### Sheet 2.3 — Observation Span Box Plot

| Property | Setting |
|----------|---------|
| **Columns** | `is_potentially_hazardous` |
| **Rows** | `observation_span_years` |
| **Mark Type** | Change to Circle, then use Analytics → Box Plot |
| **Color** | `is_potentially_hazardous` |
| **Purpose** | Shows PHAs tend to have longer observation arcs (tracked more carefully) |

### Sheet 2.4 — Magnitude vs MOID Scatter (Hazard Quadrant)

| Property | Setting |
|----------|---------|
| **Columns** | `min_orbit_intersection_dist_au` (0–0.3 range) |
| **Rows** | `absolute_magnitude_h` (invert axis — low H at top = bigger) |
| **Color** | `risk_tier` → Critical=red, High=orange, Moderate=yellow, Low=green |
| **Reference Lines** | Vertical at 0.05 (MOID threshold), Horizontal at 22 (H threshold) |
| **Purpose** | Creates 4 quadrants: top-left = most dangerous (large + close) |

### Dashboard 2 Assembly

```
┌───────────────────────┬─────────────────────┐
│                       │                     │
│  MOID Histogram       │  Observation Span   │
│  (Sheet 2.1)          │  Box Plot (2.3)     │
├───────────────────────┼─────────────────────┤
│                       │                     │
│  Eccentricity vs SMA  │  Magnitude vs MOID  │
│  Scatter (2.2)        │  Quadrant (2.4)     │
└───────────────────────┴─────────────────────┘
```

**Filters:** `risk_tier`, `orbit_class_label`, `size_category`

**Extension:** Add **Export All** to bottom-right corner → lets analysts download the scatter plot data points they've selected (brush-select → export).

---

## DASHBOARD 3: Historical Close Approach Timeline

**Goal:** Track frequency, velocity, and seasonal patterns of past close approaches (2015–2024).
**Data Source:** `close_approaches_clean.csv`

### Sheet 3.1 — Annual Approach Count (Line Chart)

| Property | Setting |
|----------|---------|
| **Columns** | `approach_year` (discrete) |
| **Rows** | `CNT(designation)` |
| **Mark Type** | Line with markers |
| **Color** | Single color `#00D2FF` |
| **Label** | Show mark labels (count per year) |
| **Reference Line** | Vertical constant at 2025, red dashed, label "Present" |
| **Filter** | Include all years (2015–2035) to show full timeline |

### Sheet 3.2 — Velocity Distribution Histogram

| Property | Setting |
|----------|---------|
| **Columns** | `velocity_km_s (bin)` — bin size `2` |
| **Rows** | `CNT(designation)` |
| **Color** | `speed_category` → Very Fast=`#D62728`, Fast=`#FF7F0E`, Moderate=`#FFDD57`, Slow=`#00D2FF` |
| **Sort Legend** | Manual: Slow → Moderate → Fast → Very Fast |
| **Stack** | Stacked bars |

### Sheet 3.3 — Monthly Heatmap (Highlight Table)

| Property | Setting |
|----------|---------|
| **Columns** | `approach_year` (discrete) |
| **Rows** | `approach_month_name` (discrete, sorted Jan–Dec) |
| **Color** | `CNT(designation)` — sequential blue/red gradient |
| **Mark Type** | Square |
| **Label** | Count value inside each cell |
| **Purpose** | Reveals seasonal observation patterns and peak months |

### Sheet 3.4 — Distance vs Velocity Scatter (Historical)

| Property | Setting |
|----------|---------|
| **Columns** | `velocity_km_s` |
| **Rows** | `distance_lunar_distances` (log scale recommended) |
| **Color** | `speed_category` |
| **Size** | `absolute_magnitude` (inverted — brighter = larger dot) |
| **Filter** | `approach_year` <= 2024 |
| **Detail** | `full_name`, `close_approach_date` |

### Dashboard 3 Assembly

```
┌─────────────────────────────────────────────┐
│     Annual Approach Count Line (3.1)        │  ← Full width top
├───────────────────────┬─────────────────────┤
│                       │                     │
│  Velocity Histogram   │  Monthly Heatmap    │
│  (3.2)                │  (3.3)              │
├───────────────────────┴─────────────────────┤
│   Distance vs Velocity Scatter (3.4)        │  ← Full width bottom
└─────────────────────────────────────────────┘
```

**Filters (show as interactive):**
- `speed_category` → Multi-select checkboxes
- `is_very_close_approach` → Boolean toggle (True = only <10 LD)
- `approach_year` → Range slider (2015–2035)

---

## DASHBOARD 4: Future Risk Forecast (2025–2035)

**Goal:** Identify and prioritize upcoming dangerous close approaches.
**Data Source:** `close_approaches_clean.csv`

### Sheet 4.1 — Future Approach Scatter (Danger Map)

| Property | Setting |
|----------|---------|
| **Columns** | `close_approach_date` (continuous, exact date) |
| **Rows** | `distance_lunar_distances` — **INVERT axis** (right-click → Edit Axis → Reversed) so closer = higher |
| **Color** | `speed_category` → same color map as Dashboard 3 |
| **Size** | `[Danger Score]` (CF-6) or `absolute_magnitude` (inverted) |
| **Detail** | `full_name`, `velocity_km_s` |
| **Filter** | `approach_year` >= 2025 |
| **Reference Line** | Horizontal at Y=10 LD (dashed red) = "Very Close" threshold |
| **Tooltip** | `Name: <full_name> | Date: <close_approach_date> | Distance: <distance_lunar_distances> LD | Speed: <velocity_km_s> km/s` |

### Sheet 4.2 — Top 20 Closest Future Approaches (Table)

| Property | Setting |
|----------|---------|
| **Rows** | `full_name`, `close_approach_date`, `distance_lunar_distances`, `velocity_km_s`, `speed_category` |
| **Filter** | `approach_year` >= 2025 |
| **Sort** | Ascending by `distance_lunar_distances` |
| **Limit** | Index ≤ 20 (create calculated field: `INDEX()`, add to filter, keep 1–20) |
| **Format** | Conditional coloring on distance: <1 LD = red background, <5 LD = orange, <10 LD = yellow |

### Sheet 4.3 — Future Yearly Forecast Bar

| Property | Setting |
|----------|---------|
| **Columns** | `approach_year` (discrete, filtered 2025–2035) |
| **Rows** | `CNT(designation)` |
| **Color** | `is_very_close_approach` → True=`#D62728`, False=`#1F77B4` |
| **Stack** | Stacked to show dangerous vs. normal |
| **Label** | Show totals |

### Sheet 4.4 — Speed Category Breakdown (Stacked Bar per Year)

| Property | Setting |
|----------|---------|
| **Columns** | `approach_year` (2025–2035) |
| **Rows** | `CNT(designation)` |
| **Color** | `speed_category` (stacked) |
| **Mark Type** | Bar (stacked) |
| **Purpose** | Shows if future approaches are getting faster |

### Dashboard 4 Assembly

```
┌─────────────────────────────────────────────┐
│   Future Yearly Forecast Bar (4.3)          │  ← Compact top bar
├───────────────────────┬─────────────────────┤
│                       │                     │
│  Future Approach      │  Top 20 Closest     │
│  Scatter / Danger Map │  Table (4.2)        │
│  (4.1)                │                     │
├───────────────────────┴─────────────────────┤
│  Speed Category Breakdown (4.4)             │  ← Bottom
└─────────────────────────────────────────────┘
```

**Filters:**
- `approach_year` → Range slider (2025–2035)
- `speed_category` → Multi-select
- `distance_lunar_distances` → Range slider

**Extensions:**
- **Data-Driven Parameters** → Add a "Top N" parameter (default 20). Wire it to Sheet 4.2's INDEX filter. Users can change to Top 10, Top 50, etc.
- **Export All** → Place in bottom-right. Analysts can export the Top N table or scatter data.

---

## Color Palette Reference

| Element | Hex Code | Usage |
|---------|----------|-------|
| Critical risk / PHA True / Very Fast | `#D62728` | Red — danger |
| High risk / Fast | `#FF7F0E` | Orange — warning |
| Moderate risk / Moderate speed | `#FFDD57` | Yellow — caution |
| Low risk / Slow | `#2CA02C` | Green — safe |
| Accent / non-PHA | `#00D2FF` | Cyan — neutral highlight |
| Non-PHA default | `#1F77B4` | Blue — baseline |

---

## Publishing Checklist

1. **File → Save to Tableau Public** (requires free account at public.tableau.com)
2. Ensure all 4 dashboards are in the workbook as separate Dashboard tabs
3. Check "Show Sheets as Tabs" is **OFF** (only dashboards visible)
4. Verify all filters are interactive and visible
5. Test on Tableau Public URL in an incognito browser
6. Paste the URL into `tableau/dashboard_links.md`
7. Export screenshots to `tableau/screenshots/` (1920×1080)
