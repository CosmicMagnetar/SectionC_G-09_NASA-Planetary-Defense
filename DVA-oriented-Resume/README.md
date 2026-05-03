# DVA-Oriented Resume — NASA Planetary Defense

Each team member should update their resume to reflect this capstone project. Below are capstone-specific, quantifiable bullet points that you can adapt for your CV.

---

## 1. Project-Level Summary Bullet
> **Data Analytics Capstone — NASA Planetary Defense (Newton School of Technology)**
> * Built an end-to-end planetary defense analytics pipeline using Python, GitHub, and Tableau to process 68,000+ NASA asteroid records, delivering an interactive decision-support dashboard for tracking high-risk close approaches.

---

## 2. Role-Specific Bullets

### For ETL & Data Engineering Roles (Aditya Rana)
- Architected a Python-based ETL pipeline (Pandas) to ingest, clean, and standardize 41,000+ Near-Earth Asteroid records from JPL's Small Body Database, reducing processing time to <30 seconds.
- Standardised opaque astronomical data structures by implementing comprehensive column rename maps and automated missing value imputation for 29+ orbital fields.
- Engineered 4 distinct analysis-ready datasets and derived key hazard metrics (MOID thresholds, risk tiers) used directly in downstream Tableau dashboards.

### For Data Analytics & EDA Roles (Aanya Mehrotra)
- Conducted systematic Exploratory Data Analysis (EDA) on 68,000+ astronomical records using Matplotlib and Seaborn, identifying key orbital patterns distinguishing the 6.2% of Potentially Hazardous Asteroids.
- Discovered and communicated critical data gaps, revealing that ~80% of small asteroids lack physical diameter data, requiring the use of absolute magnitude as a size proxy for hazard assessment.
- Designed the visual analysis framework that directly informed the Tableau dashboard, translating complex orbital mechanics (e.g. eccentricity, semi-major axis) into accessible business insights.

### For Visualization & Dashboarding Roles (Pihu Jaitly)
- Designed and published an interactive 9-sheet Tableau Public dashboard tracking asteroid close approaches from 2015–2035, serving as an operational intelligence tool for non-specialist stakeholders.
- Implemented global interactive filters, calculated fields, and a traffic-light risk tiering system to segment 41,000+ asteroids into Critical, High, Moderate, and Low hazard categories.
- Translated dense statistical findings into a clear visual narrative, resulting in a decision-ready executive view and a detailed operational timeline forecasting 3,888 future close approaches.

### For Statistical Analysis & Strategy Roles (Harshil)
- Applied rigorous non-parametric hypothesis testing (Mann-Whitney U) across 41,000+ records to statistically validate that Potentially Hazardous Asteroids (PHAs) occupy a distinct orbital regime from non-PHAs (p < 0.001).
- Developed the project's KPI framework (e.g., Critical PHA count, median MOID, approach velocity) and constructed a 9x9 orbital parameter correlation matrix to verify physical relationships like Kepler's Third Law.
- Authored a comprehensive 13-section technical report, translating statistical findings into 10 decision-oriented insights and 4 actionable planetary defense recommendations.
