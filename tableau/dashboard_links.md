# Tableau Dashboard Links — NASA Planetary Defense

**NST DVA Capstone 2 · SectionC_G-09**

---

## Dashboard Details

| Item | Link | Notes |
|---|---|---|
| **Tableau Public Dashboard** | `[PASTE TABLEAU PUBLIC URL HERE]` | **Main submission link** |
| Workbook / Story Link | `[Optional — paste if using Tableau Story]` | Optional |
| Demo Recording | `[Optional — paste Loom/YouTube link]` | Optional |

---

## How to Publish to Tableau Public (Free)

1. Download [Tableau Public Desktop](https://public.tableau.com/en-us/s/download) (free — no licence needed)
2. Open Tableau Public Desktop
3. **Connect → Text File** → navigate to `data/processed/` → connect all 4 CSVs
4. Build your sheets per `tableau/tableau_dashboard_guide.md`
5. When ready: **File → Save to Tableau Public**
6. Sign in / create a free account at https://public.tableau.com
7. After saving, copy the public URL and paste it above and in `README.md`

---

## Screenshot Checklist

Add exported dashboard screenshots to `tableau/screenshots/` using these filenames:

| File | Contents |
|---|---|
| `01_kpi_overview.png` | Full dashboard overview — KPI banner + risk tier bars |
| `02_hazard_analysis.png` | MOID histogram + eccentricity scatter |
| `03_close_approach_timeline.png` | Annual timeline + velocity histogram |
| `04_future_approaches.png` | Future approach scatter (2025–2035) |

**To export screenshots from Tableau:**
- Dashboard → `File → Export as Image` OR use OS screenshot tool
- Recommended resolution: 1920 × 1080 or higher

---

## Dashboard Filters Reference

The following interactive filters must be visible in the published dashboard:

| Filter | Type | Applied To |
|---|---|---|
| Risk Tier | Multi-select | All NEA sheets |
| Orbit Class | Multi-select | All NEA sheets |
| Size Category | Multi-select | All NEA sheets |
| Approach Year | Range slider | All Close Approach sheets |
| Speed Category | Multi-select | Close Approach sheets |
| Very Close Approach only | Toggle (Boolean) | Close Approach sheets |

> **Submission requirement:** At least one interactive filter must be visible and functional in the published Tableau Public dashboard.

---

## Tableau Public Profile

After publishing, your profile URL will be:
`https://public.tableau.com/app/profile/[your-username]`

Add this to your DVA-focused Portfolio and DVA-oriented Resume.
