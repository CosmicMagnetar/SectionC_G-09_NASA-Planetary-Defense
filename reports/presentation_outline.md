# Presentation Outline — NASA Planetary Defense
## Asteroid Risk & Close Approach Analysis
**DVA Capstone 2 · SectionC_G-09 · Newton School of Technology**

---

> This file contains the full slide-by-slide content for the presentation deck.
> The `.pptx` file is at `reports/Asteroid Insights & Risk Analysis - DVA Capstone 2 (1).pptx`
> Export to PDF → save as `reports/presentation.pdf`

---

## Slide 1 — Title Slide

**Title:** NASA Planetary Defense
**Subtitle:** Asteroid Risk & Close Approach Analysis
**Team:** SectionC_G-09 — Aditya Rana · Aanya Mehrotra · Pihu Jaitly · Harshil
**Institute:** Newton School of Technology | DVA Capstone 2
**Date:** _[Submission Date]_

*Suggested visual: dark starfield background, asteroid silhouette, NASA logo*

---

## Slide 2 — The Problem

**Headline:** 41,000+ Known Asteroids. Which ones matter?

- NASA tracks over 41,000 Near-Earth Asteroids (NEAs)
- A 140m impactor → energy of hundreds of nuclear warheads
- A 1km impactor → global climate catastrophe
- Limited telescope time must be allocated to highest-risk objects

**Visual:** Timeline of major asteroid discoveries 1980–2025

**Key question:**
> _Which asteroids present the highest near-term risk, and how do velocity, distance, and orbital characteristics predict hazard severity?_

---

## Slide 3 — Our Data

**Headline:** Two NASA/JPL Datasets · 68,000+ Records

| Dataset | Source | Rows | Key Fields |
|---|---|---|---|
| NEA Catalogue | JPL SBDB | 41,281 | Orbital elements, size, MOID, PHA flag |
| Close Approaches | CNEOS | 27,430 | Date, distance, velocity, asteroid ID |

- **Time period:** Observations 1893–2025 (NEA); Approaches 2015–2035
- **Challenge:** Raw data uses abbreviated JPL notation (H, e, a, i, q, ad, per, n...)
- **Solution:** Full rename map applied; 29 fields renamed to descriptive names

---

## Slide 4 — Our Pipeline

**Headline:** Extract · Rename · Clean · Derive · Deliver

```
Raw CSVs → 01_extraction.py (rename maps) → 02_cleaning.py (clean + derive)
→ 2 processed CSVs → 05_final_load_prep.py → Notebooks / Streamlit / Tableau
```

**Key transformations:**
- `H` → `absolute_magnitude_h`
- `e` → `orbital_eccentricity`
- `pha` → `is_potentially_hazardous`
- **NEW:** `risk_tier` (Critical/High/Moderate/Low)
- **NEW:** `speed_category` (Slow/Moderate/Fast/Very Fast)
- **NEW:** `orbit_class_label` (full English class names)

**Output:** 2 analysis-ready datasets totalling 33 cols (NEA) and 19 cols (Close Approaches)

---

## Slide 5 — KPI Summary

**Headline:** The Numbers That Matter

| KPI | Value |
|---|---|
| Total NEAs in catalogue | **41,150** |
| Potentially Hazardous Asteroids | **2,539 (6.2%)** |
| Future close approaches (2025–2035) | **3,888** |
| Median approach velocity | **~12–14 km/s** |
| NEAs with NO physical size data | **~80%** |

**Visual:** 4 KPI tiles in Tableau traffic-light colour scheme

---

## Slide 6 — Who Are the PHAs?

**Headline:** 2,539 Asteroids on the Watchlist

- **Definition:** MOID ≤ 0.05 AU AND Absolute Magnitude H ≤ 22
- **Dominant class:** Apollo (Earth-crossing, semi-major axis > 1 AU)
- **Key metric:** MOID — Minimum Orbit Intersection Distance

**Visual:** Risk Tier bar chart (Critical/High/Moderate/Low)

**Statistical finding:**
- Mann-Whitney U test confirms PHAs have **significantly lower MOID** than non-PHAs (p < 0.001)
- PHAs are **systematically larger** — lower H magnitude (p < 0.001)

---

## Slide 7 — Orbital Analysis

**Headline:** PHAs Live in a Distinct Orbital Zone

**Visual:** Eccentricity vs Semi-Major Axis scatter (PHAs = red, non-PHAs = blue)

- PHAs cluster at semi-major axis 0.8–1.4 AU with high eccentricity
- This orbital zone maximises Earth-crossing opportunity
- Strong negative correlation: eccentricity ↑ → MOID ↓ (r = −0.41)
- Apollo class has highest PHA density of all orbit types

---

## Slide 8 — Close Approach Timeline

**Headline:** 3,888 Approaches Predicted 2025–2035

**Visual:** Annual close approach count line chart (2015–2035) with 2025 reference line

- Tracking rate is consistent — no alarming future spike
- Speed distribution peaks 10–20 km/s
- ~65% of approaches classified "Moderate (5–15 km/s)"
- Very close approaches (< 10 Lunar Distances) occur regularly → require dedicated radar

**Visual:** Velocity histogram with speed category colour bands

---

## Slide 9 — Dashboard Walkthrough

**Headline:** Decision-Ready Intelligence at a Glance

**Screenshot:** 4 Tableau Dashboards & Streamlit Web App

**Executive Dashboard:**
- KPI banner → Risk Tier bars → Orbit Class treemap

**Operational Dashboards:**
- MOID histogram → Eccentricity scatter → Approach timeline → Future approach scatter

**Interactive Filters:** Risk Tier · Orbit Class · Size Category · Year Range · Speed Category

**Dashboard URL:** `[PASTE TABLEAU PUBLIC URL]`

---

## Slide 10 — Key Insights

**Headline:** 10 Findings in Decision Language

1. 6.2% of NEAs are Potentially Hazardous — small but critical
2. MOID is the single best predictor of hazard classification
3. PHAs are systematically larger than non-PHAs
4. Apollo-class objects dominate the PHA pool
5. Median approach velocity ≈ 12–14 km/s — catastrophic at 140m+
6. 3,888 future approaches tracked — completeness confirmed
7. Very close approaches (< 10 LD) occur regularly
8. 80% of small NEAs have no physical size data
9. Orbital solutions are high-quality for known large NEAs
10. Long-arc observations improve impact probability estimates

---

## Slide 11 — Recommendations

**Headline:** 4 Actions for Planetary Defense Teams

| # | Action | Why |
|---|---|---|
| 1 | Prioritise radar for Critical-tier PHAs (MOID < 0.01 AU) | Reduces orbital uncertainty from years to days |
| 2 | Fund NEO Surveyor IR mission for small-NEA characterisation | 80% of objects lack physical data |
| 3 | Automate 10 Lunar Distance alert triggers | Faster emergency observation response |
| 4 | Focus deflection planning on Apollo-class PHAs | Most numerous + most spacecraft-accessible |

---

## Slide 12 — Limitations & Next Steps

**Limitations:**
- Physical data missing for ~80% of small NEAs
- MOID is static — actual impact probability needs Monte Carlo propagation
- Risk tiers are team-defined, not official NASA classifications
- No ML model built (out of scope for this capstone)

**Next Steps:**
- Integrate JPL Sentry impact probability data
- Train Random Forest classifier on PHA vs non-PHA features
- Add spectral type for metallic vs rocky discrimination
- Extend close approach forecast to 2050

---

## Slide 13 — Team & Contributions

**Headline:** Built by SectionC_G-09

| Member | Primary Role |
|---|---|
| Aditya Rana | Project Lead · ETL Pipeline |
| Aanya Mehrotra | Data Sourcing · EDA |
| Pihu Jaitly | Tableau Dashboard · PPT |
| Harshil | Statistical Analysis · Report |

**Tools:** Python 3.12 · pandas · seaborn · scipy · Streamlit · Tableau Public · GitHub

**Repository:** `github.com/[org]/SectionC_G-09_NASA-Planetary-Defense`

---

## Slide 14 — Q&A

**Headline:** Questions Welcome

*Suggested visual: starfield with asteroid trajectory arc*

> "The goal of planetary defense is not fear — it's data. If we can see it, we can plan for it."

**Dashboard:** `[Tableau Public URL]`
**GitHub:** `[Repository URL]`
