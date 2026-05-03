# Data Dictionary — NASA Planetary Defense

**NST DVA Capstone 2 · Team SectionC_G-09**  
**Source:** NASA/JPL Small Body Database (SBDB) & Center for Near Earth Object Studies (CNEOS)

---

## Dataset 1: NEA Catalogue (`nea_catalogue_clean.csv`)

| Item | Details |
|---|---|
| Dataset name | Near-Earth Asteroid (NEA) Catalogue |
| Source | NASA JPL SBDB — https://ssd.jpl.nasa.gov/tools/sbdb_query.html |
| Raw file | `near_earth_asteroids_2025.csv` |
| Processed file | `nea_catalogue_clean.csv` |
| Granularity | One row per unique asteroid |
| Rows (approx.) | 36,000+ |

### Column Definitions — NEA Catalogue

| Column Name | Data Type | Description | Example Value | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| `spk_id` | int | JPL SPK (Solar Physics Kernel) unique identifier | `20000433` | Identifier | Renamed from `spkid` |
| `full_name` | string | Full designation string with name if known | `433 Eros (A898 PA)` | Labels | Leading whitespace stripped |
| `primary_designation` | string | Primary provisional or permanent designation number | `433` | Join key | Renamed from `pdes` |
| `name` | string | Common name of the asteroid (if officially named) | `Eros` | Labels, filter | Null if unnamed |
| `is_named` | bool | True if the asteroid has an official name | `True` | Filter, KPI | **Derived** — `name` not null |
| `is_potentially_hazardous` | bool | PHA classification: MOID ≤ 0.05 AU and H ≤ 22 | `False` | **Primary hazard filter** | Renamed from `pha` |
| `absolute_magnitude_h` | float | H magnitude — proxy for size (lower = larger/brighter) | `10.39` | Size analysis, KPI | Renamed from `H` |
| `diameter_km` | float | Physical diameter in kilometres | `16.84` | Size analysis | Null if unmeasured |
| `diameter_m` | float | Physical diameter in metres | `16840.0` | Dashboards | Null if unmeasured |
| `diameter_is_estimated` | bool | True if diameter is model-estimated, not observed | `False` | Data quality | — |
| `size_category` | string | Human-readable size bin (e.g. "Large (>1 km) — City killer+") | `Large (>1 km)` | Filter, colour | — |
| `albedo` | float | Surface reflectivity (0–1); used in size estimation | `0.25` | Physical analysis | Often null for small objects |
| `rotation_period_hours` | float | Rotation period in hours | `5.27` | Physical analysis | Renamed from `rot_per` |
| `class` | string | JPL orbit class code (AMO, APO, ATE, etc.) | `AMO` | Filter | Retained for compatibility |
| `orbit_class_label` | string | Full human-readable orbit class name | `Amor (Earth-approaching, outside orbit)` | Dashboard filter | **Derived** — mapped from `class` |
| `orbital_eccentricity` | float | Eccentricity of orbit (0 = circle, 1 = parabola) | `0.2228` | Orbital analysis | Renamed from `e` |
| `semi_major_axis_au` | float | Semi-major axis of orbit in AU | `1.458` | Orbital analysis | Renamed from `a` |
| `orbital_inclination_deg` | float | Inclination to the ecliptic plane in degrees | `10.83` | Orbital analysis | Renamed from `i` |
| `perihelion_dist_au` | float | Distance at closest approach to the Sun (AU) | `1.133` | Orbital analysis | Renamed from `q` |
| `aphelion_dist_au` | float | Distance at farthest point from the Sun (AU) | `1.78` | Orbital analysis | Renamed from `ad` |
| `orbital_period_days` | float | Orbital period in Earth days | `643.0` | Temporal analysis | Renamed from `per` |
| `orbital_period_years` | float | Orbital period in Earth years | `1.76` | Temporal analysis | Renamed from `per_y` |
| `mean_motion_deg_per_day` | float | Rate of angular motion in degrees/day | `0.5598` | Orbital analysis | Renamed from `n` |
| `min_orbit_intersection_dist_au` | float | Minimum Orbit Intersection Distance with Earth (AU) | `0.148` | **Primary hazard metric** | Renamed from `moid_au`; rows with null dropped |
| `min_orbit_intersection_dist_km` | float | MOID in kilometres | `22,140,485` | Dashboard tooltip | Renamed from `moid_km` |
| `moid_lunar_distances` | float | MOID expressed in lunar distances | `57.6` | Dashboard | — |
| `orbital_condition_code` | float | JPL orbit quality code (0=best, 9=poorest) | `0.0` | Data quality filter | Renamed from `condition_code` |
| `first_obs` | date | Date of first recorded observation | `1893-10-29` | Temporal analysis | Parsed to datetime |
| `last_obs` | date | Date of most recent observation | `2021-05-13` | Temporal analysis | Parsed to datetime |
| `data_arc_days` | float | Length of observation arc in days | `46582.0` | Data quality | Renamed from `data_arc` |
| `data_arc_years` | float | Length of observation arc in years | `127.53` | Dashboards | — |
| `observation_span_years` | float | Computed from last_obs − first_obs | `127.53` | Data quality analysis | **Derived** — `(last_obs - first_obs).days / 365.25` |
| `risk_tier` | string | Hazard classification: Critical / High / Moderate / Low | `Low` | **Dashboard KPI** | **Derived** — based on `is_potentially_hazardous` + MOID |

---



## Dataset 2: Close Approaches (`close_approaches_clean.csv`)

| Item | Details |
|---|---|
| Dataset name | Asteroid Close Approaches (2015–2035) |
| Source | NASA CNEOS Close Approach Data — https://cneos.jpl.nasa.gov/ca/ |
| Raw file | `asteroid_close_approaches_2015_2035.csv` |
| Processed file | `close_approaches_clean.csv` |
| Granularity | One row per close approach event |
| Rows (approx.) | 95,000+ |

### Column Definitions — Close Approaches

| Column Name | Data Type | Description | Example Value | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| `designation` | string | Asteroid designation code | `2022 AP1` | Join key, label | — |
| `full_name` | string | Full asteroid name including provisional designation | `(2022 AP1)` | Labels | Whitespace stripped |
| `close_approach_date` | datetime | Date and time of close approach (UTC) | `2015-01-01 00:27` | **Primary time axis** | Parsed from string to datetime |
| `distance_au` | float | Nominal close approach distance in AU | `0.0451` | Orbital analysis | — |
| `distance_km` | float | Nominal close approach distance in km | `6,746,806` | Distance KPI | Renamed from `dist_km` |
| `distance_lunar_distances` | float | Close approach distance in Lunar Distances (LD) | `17.55` | **Dashboard filter** | Renamed from `dist_lunar` |
| `distance_min_au` | float | Minimum possible close approach distance (AU) | `0.0138` | Uncertainty range | — |
| `distance_max_au` | float | Maximum possible close approach distance (AU) | `0.0766` | Uncertainty range | — |
| `velocity_km_s` | float | Velocity relative to Earth at close approach (km/s) | `11.89` | **Speed KPI** | — |
| `velocity_relative_km_h` | float | Relative velocity in km/h | `42,810` | Dashboard tooltip | Renamed from `v_rel_kmh` |
| `velocity_infinity_km_s` | float | Hyperbolic excess velocity at infinity (km/s) | `11.89` | Orbital analysis | Renamed from `v_inf`; nulls filled with `velocity_km_s` |
| `absolute_magnitude` | float | H magnitude of the approaching asteroid | `28.39` | Size proxy | Nulls filled with column median |
| `is_future` | bool | True if approach date is in the future (post-data-export) | `False` | **Future filter** | — |
| `approach_year` | int | Year of close approach | `2015` | Temporal grouping | **Derived** |
| `approach_month` | int | Month number of close approach | `1` | Temporal grouping | **Derived** |
| `approach_month_name` | string | Month name of close approach | `January` | Dashboard labels | **Derived** |
| `approach_day_of_week` | string | Day of week of close approach | `Thursday` | Temporal pattern | **Derived** |
| `is_very_close_approach` | bool | True if distance < 10 Lunar Distances | `False` | **High-risk filter** | **Derived** |
| `speed_category` | string | Binned speed: Slow / Moderate / Fast / Very Fast | `Moderate (5–15 km/s)` | Dashboard colour | **Derived** — cut on `velocity_km_s` |

---



## Derived Columns Summary

| Derived Column | Source Dataset | Logic | Purpose |
|---|---|---|---|
| `is_named` | NEA | `name` is not null | Filter named vs unnamed asteroids |
| `observation_span_years` | NEA | `(last_obs - first_obs).days / 365.25` | Data quality indicator |
| `risk_tier` | NEA | PHA + MOID thresholds | Traffic-light hazard KPI |
| `orbit_class_label` | NEA | Mapped from `class` codes | Human-readable dashboard labels |
| `approach_year` | Close | `close_approach_date.dt.year` | Year-level temporal grouping |
| `approach_month` | Close | `close_approach_date.dt.month` | Month-level grouping |
| `approach_month_name` | Close | `close_approach_date.dt.strftime('%B')` | Dashboard axis labels |
| `approach_day_of_week` | Close | `close_approach_date.dt.day_name()` | Weekly pattern analysis |
| `is_very_close_approach` | Close | `distance_lunar_distances < 10` | Highlight extreme events |
| `speed_category` | Close | Binned on `velocity_km_s` | Categorical speed filter |

---

## Data Quality Notes

- **Diameter & albedo nulls** are expected — many small NEAs have no physical measurements. Use `absolute_magnitude_h` as a size proxy.
- **MOID nulls** are dropped during cleaning — rows without MOID cannot be classified for hazard analysis.
- **`velocity_infinity_km_s` nulls** are imputed from `velocity_km_s` (physically valid for distant encounters).
- **`orbital_condition_code = 0`** means best-quality orbit; higher codes indicate more uncertain orbits.
- **PHA definition:** Officially classified when MOID ≤ 0.05 AU **and** H ≤ 22.0. Our `risk_tier` field adds finer sub-classification within PHAs.
