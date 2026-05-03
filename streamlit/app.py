import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
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
            
            # Build a single-trace horizontal bar with explicit colors and borders
            ordered = ["Critical", "High", "Moderate", "Low"]
            counts_map = {r: 0.0 for r in ordered}
            for _, row in risk_counts.iterrows():
                counts_map[row['Risk Tier']] = float(row['Count'])

            y_vals = [r for r in ordered]
            x_vals = [counts_map[r] for r in y_vals]

            fig_risk = go.Figure(go.Bar(
                x=x_vals,
                y=y_vals,
                orientation='h',
                marker=dict(color=[color_map.get(r, '#888') for r in y_vals], line=dict(color='#000000', width=1.5)),
            ))
            fig_risk.update_layout(showlegend=False, margin=dict(l=0, r=0, t=30, b=0), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            fig_risk.update_layout(height=320)
            st.plotly_chart(fig_risk, use_container_width=True, config={"responsive": True})
            with st.expander("Risk counts (table)"):
                st.dataframe(risk_counts, use_container_width=True, hide_index=True)
            
        with col_chart2:
            st.subheader("Orbit Class Breakdown")
            class_counts = filtered_nea['orbit_class_label'].value_counts().reset_index()
            class_counts.columns = ['Orbit Class', 'Count']
            class_counts['Count'] = class_counts['Count'].astype(float)
            
            # Use graph_objects Pie for more consistent rendering in previews
            fig_class = go.Figure(go.Pie(
                labels=class_counts['Orbit Class'],
                values=class_counts['Count'],
                hole=0.5,
                marker=dict(line=dict(color='#000000', width=1)),
                sort=False
            ))
            fig_class.update_traces(textinfo='none')
            fig_class.update_layout(margin=dict(l=0, r=0, t=30, b=0), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", height=320)
            st.plotly_chart(fig_class, use_container_width=True, config={"responsive": True})
            with st.expander("Orbit class counts (table)"):
                st.dataframe(class_counts, use_container_width=True, hide_index=True)
            
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
            # Build two histogram traces (PHA vs non-PHA) for reliable preview rendering
            pha_true = moid_viz[moid_viz['is_pha_str'] == 'True'][moid_col]
            pha_false = moid_viz[moid_viz['is_pha_str'] == 'False'][moid_col]

            fig_moid = go.Figure()
            if len(pha_false) > 0:
                fig_moid.add_trace(go.Histogram(x=pha_false, name='Not PHA', nbinsx=100, marker_color='#1f77b4', opacity=0.75))
            if len(pha_true) > 0:
                fig_moid.add_trace(go.Histogram(x=pha_true, name='PHA', nbinsx=100, marker_color='#d62728', opacity=0.75))

            fig_moid.update_layout(barmode='overlay', xaxis_title='MOID (AU)', yaxis_title='Count', margin=dict(l=0, r=0, t=30, b=0))
            # Add vertical line as a shape
            fig_moid.add_shape(type='line', x0=0.05, x1=0.05, y0=0, y1=1, xref='x', yref='paper', line=dict(color='orange', dash='dash'))
            fig_moid.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", height=360)
            st.plotly_chart(fig_moid, use_container_width=True, config={"responsive": True})
            with st.expander("MOID sample (table)"):
                st.dataframe(moid_viz.head(10)[[moid_col, 'is_potentially_hazardous', 'full_name']], use_container_width=True, hide_index=True)
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

            # Invert absolute magnitude (H) to compute a display size metric. Lower H => larger size
            scatter_viz['display_size'] = (30 - scatter_viz['absolute_magnitude_h']).clip(lower=1)

            # Build graph_objects scatter traces per PHA flag for consistent rendering
            fig_scatter = go.Figure()
            for pha_flag, color in [('True', '#d62728'), ('False', '#00d2ff')]:
                sub = scatter_viz[scatter_viz['is_pha_str'] == pha_flag]
                if len(sub) == 0:
                    continue
                fig_scatter.add_trace(go.Scatter(
                    x=sub['semi_major_axis_au'], y=sub['orbital_eccentricity'], mode='markers',
                    marker=dict(size=(sub['display_size']), color=color, line=dict(width=0.5, color='#000')),
                    name=f'PHA={pha_flag}',
                    text=sub['full_name']
                ))

            fig_scatter.add_shape(type='line', x0=1.0, x1=1.0, y0=0, y1=1, xref='x', yref='paper', line=dict(color='green', dash='dash'))
            fig_scatter.update_layout(xaxis_title='Semi-Major Axis (AU)', yaxis_title='Eccentricity', plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            fig_scatter.update_layout(height=520)
            st.plotly_chart(fig_scatter, use_container_width=True, config={"responsive": True})
            with st.expander("Scatter source sample (table)"):
                st.dataframe(scatter_viz.head(10)[['full_name','semi_major_axis_au','orbital_eccentricity','absolute_magnitude_h']], use_container_width=True, hide_index=True)
        else:
            st.info("No orbital data available for current filter selection.")
        
    with tab3:
        st.header("Close Approach Timeline (2015-2035)")
        
        # Yearly approaches
        yearly_counts = close_df.groupby('approach_year').size().reset_index(name='count')
        yearly_counts['count'] = yearly_counts['count'].astype(float)
        
        # Use a single-trace Scatter so rendering is consistent in preview
        fig_timeline = go.Figure(go.Scatter(x=yearly_counts['approach_year'], y=yearly_counts['count'], mode='lines+markers', line=dict(color='#00d2ff')))
        fig_timeline.add_vline(x=2025, line_dash="dash", line_color="red", annotation_text="Present (2025)")
        fig_timeline.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        fig_timeline.update_layout(height=300)
        st.plotly_chart(fig_timeline, use_container_width=True, config={"responsive": True})
        with st.expander("Yearly counts (table)"):
            st.dataframe(yearly_counts, use_container_width=True, hide_index=True)
        
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
        
        # Build velocity histogram with separate traces per category for preview compatibility
        vel_df = close_df.dropna(subset=['velocity_km_s','speed_category'])
        fig_vel = go.Figure()
        for cat, color in speed_color_map.items():
            sub = vel_df[vel_df['speed_category'] == cat]['velocity_km_s']
            if len(sub) == 0:
                continue
            fig_vel.add_trace(go.Histogram(x=sub, name=cat, marker_color=color, opacity=0.75, nbinsx=50))

        fig_vel.update_layout(barmode='overlay', xaxis_title='Velocity (km/s)', yaxis_title='Count', plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        fig_vel.update_layout(height=360)
        st.plotly_chart(fig_vel, use_container_width=True, config={"responsive": True})
        with st.expander("Velocity sample (table)"):
            st.dataframe(close_df[['velocity_km_s','speed_category']].dropna().head(20), use_container_width=True, hide_index=True)
        
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
