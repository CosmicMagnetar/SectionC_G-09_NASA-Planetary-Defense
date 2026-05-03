# NASA Planetary Defense — Asteroid Risk & Close Approach Analysis

> **Newton School of Technology | DVA Capstone 2**
> Python + GitHub + Tableau · Team SectionC_G-09

---

## Project Overview

| Field | Details |
|---|---|
| **Project Title** | NASA Planetary Defense — Asteroid Risk & Close Approach Analysis |
| **Sector** | Space & Planetary Science / Public Safety |
| **Team ID** | SectionC_G-09 |
| **Section** | Section C |
| **Faculty Mentor** | _[Faculty Mentor Name]_ |
| **Institute** | Newton School of Technology |
| **Submission Date** | _[Submission Date]_ |

### Team Members

| Role | Name | GitHub Username |
|---|---|---|
| Project Lead / ETL Lead | Aditya Rana | `@[github-handle]` |
| Data Lead / EDA | Aanya Mehrotra | `@[github-handle]` |
| Visualization Lead | Pihu Jaitly | `@[github-handle]` |
| Statistical Analysis / Report | Harshil | `@[github-handle]` |

---

## Business Problem

NASA's planetary defense mission requires continuous monitoring of Near-Earth Asteroids (NEAs) to identify objects that pose a credible impact risk. With over 41,000 known NEAs and thousands of recorded close approach events, analysts need a data-driven system to prioritize monitoring and communicate risk to stakeholders.

**Core Business Question**
> Which asteroids present the highest near-term risk, and how do velocity, MOID, and orbital characteristics predict hazard severity?

**Decision Supported**
> Enables planetary defense teams to prioritize observation toward Critical/High-tier PHAs, forecast future close approaches, and communicate risk tiers through an interactive dashboard.

---

## Dataset

| Attribute | Details |
|---|---|
| **Source** | NASA/JPL SBDB + CNEOS Close Approach Data |
| **Links** | https://ssd.jpl.nasa.gov/tools/sbdb_query.html · https://cneos.jpl.nasa.gov/ca/ |
| **NEA Catalogue** | 41,281 rows × 29 cols (raw) → 41,150 × 33 cols (cleaned) |
| **Close Approaches** | 27,430 rows × 13 cols (raw) → 27,430 × 19 cols (cleaned) |
| **Time Period** | Observations 1893–2025 (NEA); Approaches 2015–2035 |
| **Format** | CSV |

**Key Columns**

| Column | Description | Role |
|---|---|---|
| `is_potentially_hazardous` | PHA classification (MOID ≤ 0.05 AU & H ≤ 22) | Primary hazard filter |
| `min_orbit_intersection_dist_au` | Minimum orbital distance to Earth's orbit | Key hazard KPI |
| `absolute_magnitude_h` | Size proxy — lower = larger | Segmentation |
| `risk_tier` | Derived: Critical / High / Moderate / Low | Dashboard traffic light |
| `close_approach_date` | Date/time of close approach | Timeline axis |
| `velocity_km_s` | Approach speed in km/s | Speed KPI |
| `distance_lunar_distances` | Approach distance in lunar distances | Distance KPI |
| `orbit_class_label` | Human-readable orbit class name | Filter |

Full definitions → [`docs/data_dictionary.md`](docs/data_dictionary.md)

---

## KPI Framework

| KPI | Formula |
|---|---|
| Total NEA Count | `COUNT(spk_id)` in nea_catalogue_clean |
| PHA Count | `COUNT WHERE is_potentially_hazardous = True` |
| Critical PHA Count | `COUNT WHERE risk_tier = 'Critical'` |
| Median MOID (All) | `MEDIAN(min_orbit_intersection_dist_au)` |
| Future Close Approaches | `COUNT` in close_approaches_future_clean |
| Very Close Approaches (<10 LD) | `COUNT WHERE is_very_close_approach = True` |
| Median Approach Velocity | `MEDIAN(velocity_km_s)` |

---

## Key Insights

1. **2,539 of 41,150 NEAs (6.2%) are Potentially Hazardous** — a small but critical subset.
2. **Apollo-class asteroids dominate the PHA pool** — most common hazardous orbit class.
3. **MOID is the strongest predictor of hazard** — Mann-Whitney U confirms p < 0.001 separation between PHAs and non-PHAs.
4. **PHAs are systematically larger** — significantly lower H magnitude than general NEA population (p < 0.001).
5. **Median close approach velocity ≈ 12–14 km/s** — catastrophic for objects > 140m diameter.
6. **3,888 close approaches predicted 2025–2035** — consistent historical tracking rate.
7. **Very close approaches (< 10 LD) warrant dedicated radar** — disproportionate risk fraction.
8. **Diameter data missing for 80%+ of small NEAs** — H magnitude is the only size proxy available.
9. **Orbit solutions are well-constrained for large/named objects** — condition code 0 dominates.
10. **Long observation arcs (50+ years) improve impact probability estimates** for known large NEAs.

---

## Recommendations

| # | Recommendation | Expected Impact |
|---|---|---|
| 1 | Prioritize radar time for all Critical-tier PHAs (MOID < 0.01 AU) | Reduces impact uncertainty windows |
| 2 | Fund space-based IR surveys (NEO Surveyor) for small-NEA physical characterisation | Enables accurate threat assessment for 80% uncatalogued objects |
| 3 | Implement automated 10 LD alert triggers in tracking systems | Faster response for emergency observation campaigns |
| 4 | Focus deflection planning on Apollo-class PHA population | Maximises kinetic impactor mission ROI |

---

## Tableau Dashboard

| Item | Details |
|---|---|
| **Dashboard URL** | `[PASTE TABLEAU PUBLIC URL HERE]` |
| **Executive View** | KPI banner · Risk Tier bars · Orbit Class treemap |
| **Operational View** | MOID histogram · Eccentricity scatter · Annual timeline · Future approach scatter |
| **Filters** | Risk Tier · Orbit Class · Size Category · Approach Year · Speed Category |

Screenshots → [`tableau/screenshots/`](tableau/screenshots/)
Build guide → [`tableau/tableau_4_dashboards_guide.md`](tableau/tableau_4_dashboards_guide.md)

---

## Repository Structure

```text
SectionC_G-09_NASA-Planetary-Defense/
├── README.md
├── data/
│   ├── raw/                              # Original datasets (never edited)
│   └── processed/                        # 2 cleaned pipeline outputs
│       ├── nea_catalogue_clean.csv       (41,150 rows · 33 cols)
│       └── close_approaches_clean.csv    (27,430 rows · 19 cols)
├── notebooks/
│   ├── 01_extraction.ipynb              ← Raw audit, rename preview
│   ├── 02_cleaning.ipynb               ← ETL, 4-dataset export
│   ├── 03_eda.ipynb                    ← 8 visual sections
│   ├── 04_statistical_analysis.ipynb   ← Correlations, Mann-Whitney
│   └── 05_final_load_prep.ipynb        ← Tableau validation
├── scripts/
│   ├── 01_extraction.py        ← Rename maps + loaders
│   ├── 02_cleaning.py          ← Dataset cleaning logic
│   └── 05_final_load_prep.py   ← CLI orchestrator (pipeline runner)
├── tableau/
│   ├── screenshots/
│   ├── dashboard_links.md
│   └── tableau_4_dashboards_guide.md
├── streamlit/
│   └── app.py                          ← Interactive dashboard code
├── reports/
│   ├── project_report.md
│   └── presentation_outline.md
├── docs/
│   └── data_dictionary.md
├── DVA-oriented-Resume/
└── DVA-focused-Portfolio/
```

**Run the pipeline:**
```bash
python scripts/05_final_load_prep.py
# Outputs 2 CSVs to data/processed/
```

**Run the Streamlit Dashboard:**
```bash
pip install streamlit plotly
streamlit run streamlit/app.py
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 + Jupyter | ETL, EDA, statistical analysis |
| pandas · numpy · matplotlib · seaborn · scipy | Core libraries |
| Streamlit · Plotly | Interactive web application |
| Tableau Public | 4 Interactive dashboards |
| GitHub | Version control + contribution audit |

---

## Contribution Matrix

| Team Member | Data & ETL | EDA | Stats | Tableau | Report | PPT |
|---|---|---|---|---|---|---|
| Aditya Rana | Owner | Support | Support | Support | Support | Support |
| Aanya Mehrotra | Support | Owner | Support | Support | Support | Support |
| Pihu Jaitly | Support | Support | Support | Owner | Support | Owner |
| Harshil | Support | Support | Owner | Support | Owner | Support |

---

## Submission Checklist

- [x] Notebooks `01–05` committed
- [x] `data/raw/` — original datasets
- [x] `data/processed/` — 2 cleaned CSVs
- [x] `docs/data_dictionary.md` — complete
- [x] `scripts/01_extraction.py` — rename maps + loaders
- [ ] `tableau/screenshots/` — add after publishing
- [ ] `tableau/dashboard_links.md` — add Tableau Public URL
- [ ] All members: visible commits and PRs
- [ ] `reports/project_report.pdf` — export from `project_report.md`
- [ ] `reports/presentation.pdf` — export from `.pptx`

---

*Newton School of Technology · DVA Capstone 2 · SectionC_G-09*
