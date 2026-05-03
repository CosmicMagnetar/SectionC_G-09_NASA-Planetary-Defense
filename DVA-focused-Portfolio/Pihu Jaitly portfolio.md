# Portfolio Case Study — Pihu Jaitly
## NASA Planetary Defense: Asteroid Risk & Close Approach Analysis

**NST DVA Capstone 2 · SectionC_G-09**
**Role:** Visualization Lead · Tableau Dashboard · Presentation
**Live Dashboard:** [Tableau Public](https://tableaupublic.com) _(paste URL)_
**Repository:** [GitHub](https://github.com) _(paste URL)_

---

## Problem Statement

Raw data insights only create value when decision-makers can act on them. This project required translating 41,150 asteroid records and 27,430 close approach events into an interactive Tableau dashboard that a non-specialist — a policy-maker, science communicator, or planetary defense analyst — could navigate independently to answer: "Which asteroids are dangerous and when are they coming?"

---

## My Role

As **Visualization Lead**, I was responsible for:

- Designing and building 4 distinct Tableau Public dashboards and a Streamlit web application
- Implementing interactive filters and Tableau Extensions (Data-Driven Parameters, Export All)
- Establishing the visual language: traffic-light risk colours, dark space aesthetic, tooltip design
- Writing `tableau/tableau_4_dashboards_guide.md` — the build guide for all 4 dashboards
- Creating and exporting all dashboard screenshots for `tableau/screenshots/`
- Leading the presentation deck (`reports/presentation_outline.md` + `.pptx`)

---

## Dashboard Architecture

**4 Dashboards Built:**

1. **Executive Hazard Overview:** KPI banners, Risk Tier breakdown, Orbit Treemap
2. **Orbital Mechanics Deep Dive:** MOID Histogram, Eccentricity Scatter, Observation Span Box Plots
3. **Historical Approach Timeline:** Annual Timeline, Velocity Histogram, Monthly Heatmap
4. **Future Risk Forecast:** Future Approaches Scatter Map, Top 20 Nearest Text Table

**Calculated fields created in Tableau:**
```
// Is Large Asteroid
[absolute_magnitude_h] <= 18 OR [diameter_km] >= 1

// Speed in km/h
[velocity_km_s] * 3600

// Diameter Estimate (where null)
IF ISNULL([diameter_km]) THEN
    1329 / POWER(10, 0.2 * [absolute_magnitude_h]) * SQRT(0.15)
ELSE [diameter_km] END
```

---

## Design Decisions

- **Colour palette:** Critical = `#d62728` · High = `#ff7f0e` · Moderate = `#ffdd57` · Low = `#2ca02c`
- **Background:** Dark slate `#1a1a2e` for space aesthetic and contrast
- **Filter placement:** Global dashboard filters applied across all sheets
- **Tooltip:** Every mark shows `full_name`, `risk_tier`, `min_orbit_intersection_dist_au`, `velocity_km_s`

---

## Key Insights Surfaced by Dashboard

- Risk tier bars immediately show Moderate and Low dominate — providing visual reassurance while highlighting the critical minority
- Eccentricity scatter reveals PHAs cluster in a distinct orbital zone (semi-major axis 0.8–1.4 AU, eccentricity 0.3–0.7)
- Future approach scatter shows no alarming density spike — tracking rate is consistent

---

## Skills Demonstrated

`Tableau Desktop` · `Tableau Public` · `Streamlit` · `Dashboard Design` · `Data Visualisation`
`Calculated Fields` · `Interactive Filters` · `Colour Theory` · `Storytelling` · `PowerPoint`

---

## What I Learned

Effective dashboards are not about chart quantity — they are about answering a specific question with the minimum cognitive load. The planetary defense use case required balancing scientific precision (correct axis labels, reference lines at MOID = 0.05 AU) with accessibility for non-specialist audiences (plain language KPI names, traffic-light colours). This tension is the core challenge of all applied data visualisation work.
