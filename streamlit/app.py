import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
from pathlib import Path

# Set Plotly dark theme globally (avoids per-chart template bug in Plotly 5.22)
pio.templates.default = "plotly_dark"

# Set page config
st.set_page_config(
    page_title="NASA Planetary Defense Dashboard",
    page_icon="☄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium aesthetics
st.markdown("""
<style>
    div[data-testid="metric-container"] {
        background-color: #1e1e2f;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border: 1px solid #333344;
    }
    div[data-testid="metric-container"] label,
    div[data-testid="stMetricLabel"] {
        color: #a0a0b0 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"],
    div[data-testid="metric-container"] > div > div {
        color: #00d2ff !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    # Try a couple of likely locations so Streamlit preview and different CWDs work.
    candidates = [
        Path(__file__).resolve().parent.parent / "data" / "processed",
        Path.cwd() / "data" / "processed",
    ]

    base_path = None
    for p in candidates:
        if p.exists():
            base_path = p
            break

    if base_path is None:
        st.error("Data folder not found. Run the ETL pipeline or place data under `data/processed`.")
        return pd.DataFrame(), pd.DataFrame(), None

    try:
        nea_df = pd.read_csv(base_path / "nea_catalogue_clean.csv", low_memory=False)
        close_df = pd.read_csv(base_path / "close_approaches_clean.csv", low_memory=False)

        # Normalize and ensure required columns exist
        if 'close_approach_date' in close_df.columns:
            close_df['close_approach_date'] = pd.to_datetime(close_df['close_approach_date'], errors='coerce')

        # If approach_year missing or contains NaNs, derive from parsed date
        if 'approach_year' not in close_df.columns or close_df['approach_year'].isnull().all():
            if 'close_approach_date' in close_df.columns:
                close_df['approach_year'] = close_df['close_approach_date'].dt.year

        # Ensure numeric columns are numeric
        for col in ['velocity_km_s', 'distance_lunar_distances']:
            if col in close_df.columns:
                close_df[col] = pd.to_numeric(close_df[col], errors='coerce')

        # Fill missing categorical values to avoid plotting errors
        if 'speed_category' not in close_df.columns:
            close_df['speed_category'] = 'Unknown'
        else:
            close_df['speed_category'] = close_df['speed_category'].fillna('Unknown')

        if 'risk_tier' not in nea_df.columns:
            nea_df['risk_tier'] = None
        else:
            nea_df['risk_tier'] = nea_df['risk_tier'].fillna('Unknown')

        # Normalize hazard flag to boolean-like strings for consistent plotting
        if 'is_potentially_hazardous' in nea_df.columns:
            nea_df['is_potentially_hazardous'] = nea_df['is_potentially_hazardous'].astype(str)

        return nea_df, close_df, base_path
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame(), None

nea_df, close_df, data_path = load_data()

# Allow manual cache refresh if Streamlit is holding an old empty cache
if st.sidebar.button("Reload data (clear cache)"):
    st.cache_data.clear()
    st.experimental_rerun()

# Debug panel: show path, shapes, and presence of expected columns
with st.sidebar.expander("Data diagnostics", expanded=False):
    st.write("Data path:", str(data_path) if data_path is not None else "Not found")
    st.write("NEA rows:", len(nea_df))
    st.write("Close approach rows:", len(close_df))

    expected_cols = [
        'risk_tier', 'orbit_class_label', 'min_orbit_intersection_dist_au',
        'semi_major_axis_au', 'orbital_eccentricity', 'absolute_magnitude_h',
        'approach_year', 'velocity_km_s', 'speed_category', 'close_approach_date',
        'distance_lunar_distances'
    ]
    missing = []
    present = []
    for c in expected_cols:
        if c in nea_df.columns or c in close_df.columns:
            present.append(c)
        else:
            missing.append(c)

    st.write("Present columns (sample):", present[:8])
    if missing:
        st.warning(f"Missing expected columns: {', '.join(missing)}")

# App layout
st.title("☄️ NASA Planetary Defense Dashboard")
st.markdown("Interactive exploration of Near-Earth Asteroids (NEAs) and Close Approaches.")

if not nea_df.empty and not close_df.empty:
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # NEA filters
    st.sidebar.subheader("NEA Catalogue")
    orbit_classes = ["All"] + sorted(list(nea_df['orbit_class_label'].dropna().unique()))
    selected_class = st.sidebar.selectbox("Orbit Class", orbit_classes)
    
    risk_tiers = ["All"] + sorted(list(nea_df['risk_tier'].dropna().unique()))
    selected_risk = st.sidebar.selectbox("Risk Tier", risk_tiers)
    
    # Filter data based on selection
    filtered_nea = nea_df.copy()
    if selected_class != "All":
        filtered_nea = filtered_nea[filtered_nea['orbit_class_label'] == selected_class]
    if selected_risk != "All":
        filtered_nea = filtered_nea[filtered_nea['risk_tier'] == selected_risk]

    # Chart input diagnostics (shows what each chart will receive)
    with st.sidebar.expander("Chart inputs (debug)", expanded=False):
        st.write("Filtered NEA rows:", len(filtered_nea))
        try:
            rc = filtered_nea['risk_tier'].value_counts().reset_index()
            rc.columns = ['Risk Tier', 'Count']
            st.write("Risk counts:")
            st.dataframe(rc.head(10), use_container_width=True)
        except Exception as e:
            st.write("Risk counts error:", e)

        try:
            cc = filtered_nea['orbit_class_label'].value_counts().reset_index()
            cc.columns = ['Orbit Class', 'Count']
            st.write("Orbit class counts:")
            st.dataframe(cc.head(10), use_container_width=True)
        except Exception as e:
            st.write("Orbit class counts error:", e)

        moid_col = 'min_orbit_intersection_dist_au'
        try:
            moid_viz_samp = filtered_nea[filtered_nea[moid_col].notna() & (filtered_nea[moid_col] <= 1.0)].head(10)
            st.write(f"MOID sample rows (<=1 AU): {len(filtered_nea[filtered_nea[moid_col].notna() & (filtered_nea[moid_col] <= 1.0)])}")
            st.dataframe(moid_viz_samp[[moid_col, 'is_potentially_hazardous', 'full_name']].head(10), use_container_width=True)
        except Exception as e:
            st.write("MOID sample error:", e)

        try:
            scatter_cols = ['semi_major_axis_au', 'orbital_eccentricity', 'absolute_magnitude_h']
            scatter_valid = filtered_nea.dropna(subset=scatter_cols)
            st.write("Scatter valid rows:", len(scatter_valid))
        except Exception as e:
            st.write("Scatter sample error:", e)

        try:
            yc = close_df.groupby('approach_year').size().reset_index(name='count')
            st.write("Yearly counts sample:")
            st.dataframe(yc.head(10), use_container_width=True)
        except Exception as e:
            st.write("Yearly counts error:", e)
        
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Overview & KPIs", "🪐 Orbital Analysis", "⏱️ Close Approaches"])
    
    with tab1:
        st.header("Executive Overview")
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total NEAs", f"{len(filtered_nea):,}")
        
        pha_count = len(filtered_nea[filtered_nea['is_potentially_hazardous'].astype(str).str.lower() == 'true'])
        col2.metric("Potentially Hazardous", f"{pha_count:,}")
        
        future_approaches = len(close_df[close_df['approach_year'] >= 2025])
        col3.metric("Future Approaches (≥2025)", f"{future_approaches:,}")
        
        median_vel = close_df['velocity_km_s'].median()
        col4.metric("Median Approach Velocity", f"{median_vel:.1f} km/s")
        
        st.divider()
        
        # Charts
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("Risk Tier Distribution")
            risk_counts = filtered_nea['risk_tier'].value_counts().reset_index()
            risk_counts.columns = ['Risk Tier', 'Count']
            risk_counts['Count'] = risk_counts['Count'].astype(float)
            
            color_map = {
                'Critical': '#d62728', 
                'High': '#ff7f0e', 
                'Moderate': '#ffdd57', 
                'Low': '#2ca02c'
            }
            
            fig_risk = px.bar(
                risk_counts, 
                x='Count', 
                y='Risk Tier', 
                orientation='h',
                color='Risk Tier',
                color_discrete_map=color_map,
                category_orders={"Risk Tier": ["Critical", "High", "Moderate", "Low"]},

            )
            fig_risk.update_layout(showlegend=False, margin=dict(l=0, r=0, t=30, b=0), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_risk, use_container_width=True)
            
        with col_chart2:
            st.subheader("Orbit Class Breakdown")
            class_counts = filtered_nea['orbit_class_label'].value_counts().reset_index()
            class_counts.columns = ['Orbit Class', 'Count']
            class_counts['Count'] = class_counts['Count'].astype(float)
            
            fig_class = px.pie(
                class_counts, 
                values='Count', 
                names='Orbit Class',
                hole=0.5,

            )
            # Removed text labels to prevent cluttering; relying on hover tooltips instead
            fig_class.update_traces(textinfo='none')
            fig_class.update_layout(margin=dict(l=0, r=0, t=30, b=0), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_class, use_container_width=True)
            
    with tab2:
        st.header("Orbital Mechanics Analysis")
        
        # MOID Histogram
        st.subheader("Minimum Orbit Intersection Distance (MOID)")
        st.markdown("MOID ≤ 0.05 AU is the threshold for 'Potentially Hazardous' classification.")
        
        # Limit to relevant range for visualization
        moid_col = 'min_orbit_intersection_dist_au'
        moid_viz = filtered_nea[filtered_nea[moid_col].notna() & (filtered_nea[moid_col] <= 1.0)].copy()
        
        if not moid_viz.empty:
            # Convert bool to string for coloring
            moid_viz['is_pha_str'] = moid_viz['is_potentially_hazardous'].astype(str)
            
            fig_moid = px.histogram(
                moid_viz, 
                x=moid_col,
                color='is_pha_str',
                nbins=100,
                color_discrete_map={'True': '#d62728', 'False': '#1f77b4'},
                labels={moid_col: 'MOID (AU)', 'is_pha_str': 'Is PHA'},

            )
            fig_moid.add_vline(x=0.05, line_dash="dash", line_color="orange", annotation_text="PHA Threshold (0.05 AU)")
            fig_moid.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_moid, use_container_width=True)
        else:
            st.info("No MOID data available for current filter selection.")
        
        # Scatter: Eccentricity vs Semi-major axis
        st.subheader("Orbital Eccentricity vs. Semi-Major Axis")
        
        # Filter to rows with valid data for the scatter plot
        scatter_cols = ['semi_major_axis_au', 'orbital_eccentricity', 'absolute_magnitude_h']
        scatter_valid = filtered_nea.dropna(subset=scatter_cols)
        
        if not scatter_valid.empty:
            # Sample data to prevent browser crash if huge (reduced for Cloud memory)
            scatter_viz = scatter_valid.sample(min(len(scatter_valid), 2000), random_state=42).copy()
            scatter_viz['is_pha_str'] = scatter_viz['is_potentially_hazardous'].astype(str)
            
            # Invert absolute magnitude (H) to compute a display size metric. 
            # Lower H means larger physical size.
            scatter_viz['display_size'] = (30 - scatter_viz['absolute_magnitude_h']).clip(lower=1)
            
            fig_scatter = px.scatter(
                scatter_viz,
                x='semi_major_axis_au',
                y='orbital_eccentricity',
                color='is_pha_str',
                size='display_size',
                hover_name='full_name',
                hover_data={'display_size': False, 'absolute_magnitude_h': True, 'risk_tier': True, moid_col: True},
                color_discrete_map={'True': '#d62728', 'False': '#00d2ff'},
                labels={'semi_major_axis_au': 'Semi-Major Axis (AU)', 'orbital_eccentricity': 'Eccentricity'},
                range_x=[0, 4],

            )
            fig_scatter.add_vline(x=1.0, line_dash="dash", line_color="green", annotation_text="Earth Orbit (1 AU)")
            fig_scatter.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("No orbital data available for current filter selection.")
        
    with tab3:
        st.header("Close Approach Timeline (2015-2035)")
        
        # Yearly approaches
        yearly_counts = close_df.groupby('approach_year').size().reset_index(name='count')
        yearly_counts['count'] = yearly_counts['count'].astype(float)
        
        fig_timeline = px.line(
            yearly_counts, 
            x='approach_year', 
            y='count',
            markers=True,
            labels={'approach_year': 'Year', 'count': 'Number of Close Approaches'},

        )
        fig_timeline.add_vline(x=2025, line_dash="dash", line_color="red", annotation_text="Present (2025)")
        fig_timeline.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        st.divider()
        
        # Approach Velocity Distribution
        st.subheader("Approach Velocity Distribution")
        
        # Color map matches ACTUAL speed_category values from the ETL pipeline
        speed_color_map = {
            'Very Fast (>30 km/s)': '#d62728',
            'Fast (15–30 km/s)': '#ff7f0e',
            'Moderate (5–15 km/s)': '#ffdd57',
            'Slow (<5 km/s)': '#00d2ff'
        }
        
        fig_vel = px.histogram(
            close_df,
            x='velocity_km_s',
            color='speed_category',
            nbins=50,
            labels={'velocity_km_s': 'Velocity (km/s)', 'speed_category': 'Speed Category'},

            color_discrete_map=speed_color_map,
            category_orders={'speed_category': ['Slow (<5 km/s)', 'Moderate (5–15 km/s)', 'Fast (15–30 km/s)', 'Very Fast (>30 km/s)']}
        )
        fig_vel.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_vel, use_container_width=True)
        
        # Top upcoming approaches
        st.subheader("Top Upcoming Close Approaches (Next 100)")
        future_df = close_df[close_df['close_approach_date'] >= pd.Timestamp('2025-01-01')].copy()
        future_df = future_df.sort_values('close_approach_date').head(100)
        
        if not future_df.empty:
            # Format for display
            display_cols = ['full_name', 'close_approach_date', 'distance_lunar_distances', 'velocity_km_s', 'speed_category']
            future_display = future_df[display_cols].copy()
            future_display['close_approach_date'] = future_display['close_approach_date'].dt.strftime('%Y-%m-%d %H:%M')
            future_display['distance_lunar_distances'] = future_display['distance_lunar_distances'].round(2)
            future_display['velocity_km_s'] = future_display['velocity_km_s'].round(2)
            
            st.dataframe(future_display, use_container_width=True, hide_index=True)
        else:
            st.info("No future close approaches found in the dataset.")
