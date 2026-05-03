import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="NASA Planetary Defense Dashboard",
    page_icon="☄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    base_path = Path(__file__).parent.parent / "data" / "processed"
    
    try:
        nea_df = pd.read_csv(base_path / "nea_catalogue_clean.csv")
        close_df = pd.read_csv(base_path / "close_approaches_clean.csv")
        
        # Convert dates
        if 'close_approach_date' in close_df.columns:
            close_df['close_approach_date'] = pd.to_datetime(close_df['close_approach_date'])
        
        return nea_df, close_df
    except FileNotFoundError:
        st.error("Data files not found. Please run the ETL pipeline first: `python scripts/05_final_load_prep.py`")
        return pd.DataFrame(), pd.DataFrame()

nea_df, close_df = load_data()

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
            
            # Custom colors for risk tiers
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
                category_orders={"Risk Tier": ["Critical", "High", "Moderate", "Low"]}
            )
            fig_risk.update_layout(showlegend=False)
            st.plotly_chart(fig_risk, use_container_width=True)
            
        with col_chart2:
            st.subheader("Orbit Class Breakdown")
            class_counts = filtered_nea['orbit_class_label'].value_counts().reset_index()
            class_counts.columns = ['Orbit Class', 'Count']
            
            fig_class = px.pie(
                class_counts, 
                values='Count', 
                names='Orbit Class',
                hole=0.4
            )
            fig_class.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_class, use_container_width=True)
            
    with tab2:
        st.header("Orbital Mechanics Analysis")
        
        # MOID Histogram
        st.subheader("Minimum Orbit Intersection Distance (MOID)")
        st.markdown("MOID ≤ 0.05 AU is the threshold for 'Potentially Hazardous' classification.")
        
        # Limit to relevant range for visualization
        moid_viz = filtered_nea[filtered_nea['min_orbit_intersection_dist_au'] <= 1.0]
        
        # Convert bool to string for coloring
        moid_viz['is_pha_str'] = moid_viz['is_potentially_hazardous'].astype(str)
        
        fig_moid = px.histogram(
            moid_viz, 
            x='min_orbit_intersection_dist_au',
            color='is_pha_str',
            nbins=100,
            color_discrete_map={'True': '#d62728', 'False': '#1f77b4'},
            labels={'min_orbit_intersection_dist_au': 'MOID (AU)', 'is_pha_str': 'Is PHA'}
        )
        fig_moid.add_vline(x=0.05, line_dash="dash", line_color="orange", annotation_text="PHA Threshold (0.05 AU)")
        st.plotly_chart(fig_moid, use_container_width=True)
        
        # Scatter: Eccentricity vs Semi-major axis
        st.subheader("Orbital Eccentricity vs. Semi-Major Axis")
        
        # Sample data to prevent browser crash if huge
        scatter_viz = filtered_nea.sample(min(len(filtered_nea), 5000), random_state=42)
        scatter_viz['is_pha_str'] = scatter_viz['is_potentially_hazardous'].astype(str)
        
        fig_scatter = px.scatter(
            scatter_viz,
            x='semi_major_axis_au',
            y='orbital_eccentricity',
            color='is_pha_str',
            size='absolute_magnitude_h',
            hover_name='full_name',
            hover_data=['risk_tier', 'min_orbit_intersection_dist_au'],
            color_discrete_map={'True': '#d62728', 'False': '#1f77b4'},
            labels={'semi_major_axis_au': 'Semi-Major Axis (AU)', 'orbital_eccentricity': 'Eccentricity'},
            range_x=[0, 4]
        )
        fig_scatter.add_vline(x=1.0, line_dash="dash", line_color="green", annotation_text="Earth Orbit (1 AU)")
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with tab3:
        st.header("Close Approach Timeline (2015-2035)")
        
        # Yearly approaches
        yearly_counts = close_df.groupby('approach_year').size().reset_index(name='count')
        
        fig_timeline = px.line(
            yearly_counts, 
            x='approach_year', 
            y='count',
            markers=True,
            labels={'approach_year': 'Year', 'count': 'Number of Close Approaches'}
        )
        fig_timeline.add_vline(x=2025, line_dash="dash", line_color="red", annotation_text="Present (2025)")
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        st.divider()
        
        # Approach Velocity Distribution
        st.subheader("Approach Velocity Distribution")
        
        fig_vel = px.histogram(
            close_df,
            x='velocity_km_s',
            color='speed_category',
            nbins=50,
            labels={'velocity_km_s': 'Velocity (km/s)'}
        )
        st.plotly_chart(fig_vel, use_container_width=True)
        
        # Top upcoming approaches
        st.subheader("Top Upcoming Close Approaches (Next 100)")
        future_df = close_df[close_df['close_approach_date'] >= pd.Timestamp('2025-01-01')].copy()
        future_df = future_df.sort_values('close_approach_date').head(100)
        
        # Format for display
        display_cols = ['full_name', 'close_approach_date', 'distance_lunar_distances', 'velocity_km_s', 'speed_category']
        future_display = future_df[display_cols].copy()
        future_display['close_approach_date'] = future_display['close_approach_date'].dt.strftime('%Y-%m-%d %H:%M')
        future_display['distance_lunar_distances'] = future_display['distance_lunar_distances'].round(2)
        future_display['velocity_km_s'] = future_display['velocity_km_s'].round(2)
        
        st.dataframe(future_display, use_container_width=True, hide_index=True)
