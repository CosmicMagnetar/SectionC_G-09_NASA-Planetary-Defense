# Portfolio Case Study — Aanya Mehrotra
## NASA Planetary Defense: Asteroid Risk & Close Approach Analysis

**NST DVA Capstone 2 · SectionC_G-09**
**Role:** Data Lead · Exploratory Data Analysis
**Live Dashboard:** [Tableau Public](https://tableaupublic.com) _(paste URL)_
**Repository:** [GitHub](https://github.com) _(paste URL)_
**Portfolio:** [https://dva-portfolio-seven.vercel.app/](https://dva-portfolio-seven.vercel.app/)
---

## Problem Statement

With 41,000+ known Near-Earth Asteroids and 27,000+ close approach records, the challenge is not data scarcity — it is signal extraction. This project applied systematic EDA to identify which physical and orbital characteristics distinguish the 6.2% of asteroids that are Potentially Hazardous from the remainder, and to surface patterns in close approach timing, velocity, and distance.

---

## My Role

As **Data Lead and EDA Analyst**, I was responsible for:

- Conducting the full Exploratory Data Analysis in `notebooks/03_eda.ipynb`
- Designing the visual analysis framework (8 analytical sections)
- Identifying the key patterns in physical properties, orbit classes, MOID distribution, and close approach behaviour
- Authoring the EDA insights that informed the statistical analysis and Tableau build
- Contributing to the data dictionary and column definitions

---

## Dataset Scale

- **NEA Catalogue:** 41,150 asteroids after cleaning, with 33 fully-named columns
- **Close Approaches:** 27,430 events (2015–2035), including 3,888 future approaches
- **PHAs:** 2,539 (6.17% of catalogue) — primary analytical focus

---

## Key EDA Findings

### Physical Properties
- Absolute magnitude H is right-skewed — most NEAs are small (H > 20)
- Physical size data (diameter, albedo) is missing for ~80% of objects
- H magnitude is the only reliable size proxy for the majority of the catalogue

### Orbit Classification
- **Apollo** class dominates (~60% of NEAs) and has the highest PHA count
- **Aten** class has the highest *proportion* of PHAs relative to its total count
- Orbit class label mapping (e.g. `AMO` → "Amor (Earth-approaching, outside orbit)") dramatically improved Tableau filter usability

### MOID Patterns
- Clear separation between PHAs (MOID ≤ 0.05 AU by definition) and non-PHAs
- Sub-threshold PHAs cluster near MOID = 0.01–0.04 AU — the highest-risk zone

### Close Approach Patterns
- Annual approach count is consistent 2015–2035 — no alarming future spike
- Velocity peaks at 10–20 km/s; ~65% classified "Moderate (5–15 km/s)"
- Very close approaches (< 10 Lunar Distances) occur regularly across all years

---

## Visualisations Produced

1. Absolute Magnitude H distribution histogram
2. Diameter distribution (< 50 km) histogram
3. Orbit class horizontal bar chart
4. Eccentricity vs Semi-Major Axis scatter (PHA coloured)
5. MOID distribution — All NEAs vs PHAs overlay
6. Annual close approach count line chart (2015–2035)
7. Velocity distribution + speed category pie chart
8. Future approaches: Distance vs Velocity scatter (coloured by size)
9. Risk tier bar chart (traffic light colours)

---

## Skills Demonstrated

`EDA` · `matplotlib` · `seaborn` · `pandas` · `Jupyter Notebooks`
`Data Storytelling` · `Visual Design` · `Pattern Recognition` · `GitHub`

---

## What I Learned

Large astronomical datasets require domain-adapted EDA — standard business data assumptions (like normally distributed metrics) don't hold. MOID and orbital eccentricity have physically constrained ranges and distributions that need domain-aware visualisation. Learning to communicate these patterns in plain language for a non-astronomer audience was the most valuable skill this project developed.
