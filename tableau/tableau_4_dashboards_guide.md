# Tableau Guide — NASA Planetary Defense (4 Dashboards)

**NST DVA Capstone 2 · Team SectionC_G-09**  
Reference: [nst-capstone-2.netlify.app](https://nst-capstone-2.netlify.app/)

---

## Overview

This guide walks through building **four distinct Tableau dashboards** from the two processed datasets (`nea_catalogue_clean.csv` and `close_approaches_clean.csv`). 

### Recommended Tableau Extensions
To enhance interactivity, download and use the following Tableau Dashboard Extensions (available in the Tableau Extension Gallery):
1. **Data-Driven Parameters**: Dynamically updates parameter lists when underlying data changes.
2. **Export All**: Allows stakeholders to download the filtered underlying data directly from the dashboard to Excel/CSV.
3. **Show Me More**: (Optional) Provides advanced chart types like radial charts or network graphs if you wish to expand beyond standard Tableau visuals.

---

## Step 1 — Connect Data Sources

1. Open **Tableau Desktop / Tableau Public**
2. Connect to **Text File** → `data/processed/nea_catalogue_clean.csv`
3. Add a **New Data Source** → connect to `data/processed/close_approaches_clean.csv`

> ⚠️ Do NOT join the files. Treat them as two separate data sources. Use dashboard-level parameter actions if cross-filtering is necessary.

---

## Dashboard 1: Executive Hazard Overview
**Goal:** Answer "How many asteroids are dangerous?"
**Data Source:** `nea_catalogue_clean`

### Sheets Required
| Sheet Name | Chart Type | Columns/Fields | Configuration |
|---|---|---|---|
| KPI Banner | Text Tiles | `spk_id`, `is_potentially_hazardous` | Count distinct of spk_id. Create calculated field for PHA count. |
| Risk Tier Breakdown | Horizontal Bar | `risk_tier`, `spk_id` | Rows: `risk_tier`. Cols: Count(spk_id). Color by Risk Tier (Traffic light colors). |
| Orbit Class Distribution | Treemap / Pie | `orbit_class_label`, `spk_id` | Size: Count(spk_id). Label: `orbit_class_label` + Percent of Total. |

**Dashboard Assembly:**
- Place KPIs at the top.
- Side-by-side layout for Risk Tiers and Orbit Classes.
- **Filters to Add:** `risk_tier` (Multi-select list), `orbit_class_label` (Dropdown).

---

## Dashboard 2: Orbital Mechanics Deep Dive
**Goal:** Visualise the physics of Potentially Hazardous Asteroids (PHAs).
**Data Source:** `nea_catalogue_clean`

### Sheets Required
| Sheet Name | Chart Type | Columns/Fields | Configuration |
|---|---|---|---|
| MOID Histogram | Binned Bar Chart | `min_orbit_intersection_dist_au`, `is_potentially_hazardous` | Create bins on MOID (size 0.05). Add Reference Line at 0.05 AU (PHA Threshold). Color by PHA flag. |
| Eccentricity vs Distance | Scatter Plot | `semi_major_axis_au`, `orbital_eccentricity` | Cols: SMA. Rows: Eccentricity. Color by PHA flag. Add vertical Reference Line at X=1.0 (Earth's Orbit). |
| Observation Span | Box Plot | `is_potentially_hazardous`, `observation_span_years` | Compare how long PHAs have been tracked vs non-PHAs. |

**Dashboard Assembly:**
- Use the Scatter Plot as the main central view.
- Histogram on the right panel.
- **Extensions:** Add the "Export All" extension so analysts can download the data points of selected clusters.

---

## Dashboard 3: Historical Approach Timeline
**Goal:** Track frequency and velocity of past close approaches.
**Data Source:** `close_approaches_clean`

### Sheets Required
| Sheet Name | Chart Type | Columns/Fields | Configuration |
|---|---|---|---|
| Annual Timeline | Area Chart / Line | `approach_year` (or `close_approach_date`), `spk_id` | Cols: Year(Date). Rows: Count(spk_id). Filter to Years <= 2024. |
| Velocity Distribution | Histogram | `velocity_km_s`, `speed_category` | Create bins on velocity. Color bars by `speed_category`. |
| Monthly Heatmap | Highlight Table | `approach_month_name`, `approach_year` | Rows: Months. Cols: Years. Color: Count. Identifies seasonal observation bias. |

**Dashboard Assembly:**
- Stack the Timeline and Velocity Distribution vertically.
- **Filters to Add:** `speed_category`, `is_very_close_approach`.

---

## Dashboard 4: Future Risk Forecast
**Goal:** Predict and prioritise upcoming close approaches (2025–2035).
**Data Source:** `close_approaches_clean`

### Sheets Required
| Sheet Name | Chart Type | Columns/Fields | Configuration |
|---|---|---|---|
| Future Approaches Map | Scatter Plot | `close_approach_date`, `distance_lunar_distances` | Filter Date >= 2025. Cols: Exact Date. Rows: Distance. Size by `absolute_magnitude`. Invert Y-axis so closer to Earth is higher up. |
| Top 20 Nearest | Text Table | `full_name`, `close_approach_date`, `distance_lunar_distances`, `velocity_km_s` | Filter Date >= Today. Sort Ascending by Distance. Limit to Top 20. |

**Dashboard Assembly:**
- Place the Scatter Plot dominating the left side.
- Place the Text Table on the right for exact readouts.
- **Extensions:** Use "Data-Driven Parameters" if you want to allow users to dynamically change the "Top N" parameter based on the dataset.

---

## Step 2 — Calculated Fields Reference

```text
// 1. Total PHA Count (for KPIs)
IF [is_potentially_hazardous] = TRUE THEN 1 ELSE 0 END

// 2. Is Large Asteroid (proxy)
IF [absolute_magnitude_h] <= 18 OR [diameter_km] >= 1 THEN "Large" ELSE "Small" END

// 3. Very Close Approach Flag
IF [distance_lunar_distances] < 10 THEN TRUE ELSE FALSE END
```

## Step 3 — Publish to Tableau Public
1. Go to **Server → Tableau Public → Save to Tableau Public**.
2. Sign in and publish.
3. Check the "Allow workbook and its data to be downloaded by others" box.
4. Copy the URL and paste it into `tableau/dashboard_links.md`.
