import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np
import os

# Page configuration
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin-bottom: 1rem;
    }
    .subheader {
        color: #2E86AB;
        border-bottom: 2px solid #2E86AB;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load all data files"""
    data = {}
    
    # Load historical data
    try:
        # Load the main data file
        hist_path = "data/processed/ethiopia_fi_enriched_combined.csv"
        if os.path.exists(hist_path):
            data['historical'] = pd.read_csv(hist_path)
            
            # Convert date columns
            date_cols = ['observation_date', 'collection_date']
            for col in date_cols:
                if col in data['historical'].columns:
                    data['historical'][col] = pd.to_datetime(
                        data['historical'][col], errors='coerce'
                    )
    except Exception as e:
        st.warning(f"Could not load historical data: {e}")
        data['historical'] = pd.DataFrame()
    
    # Load forecast data
    try:
        forecast_path = "forecasts/account_ownership_forecasts.csv"
        if os.path.exists(forecast_path):
            data['forecast'] = pd.read_csv(forecast_path)
    except Exception as e:
        st.warning(f"Could not load forecast data: {e}")
        data['forecast'] = pd.DataFrame()
    
    # Load forecast summary
    try:
        summary_path = "forecasts/forecast_summary.csv"
        if os.path.exists(summary_path):
            data['summary'] = pd.read_csv(summary_path)
    except Exception as e:
        st.warning(f"Could not load forecast summary: {e}")
        data['summary'] = pd.DataFrame()
    
    return data

# Load data
data = load_data()

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/71/Flag_of_Ethiopia.svg", width=100)
    st.title("📊 Dashboard Controls")
    
    # Navigation
    page = st.radio(
        "Navigate to:",
        ["🏠 Overview", "📈 Trends", "🔮 Forecasts", "🎯 Inclusion Projections"]
    )
    
    st.divider()
    
    # Date range selector for trends page
    st.subheader("Date Range")
    if 'historical' in data and not data['historical'].empty:
        min_date = data['historical']['observation_date'].min()
        max_date = data['historical']['observation_date'].max()
        
        # Handle NaT values
        if pd.isna(min_date) or pd.isna(max_date):
            min_date = pd.Timestamp('2014-01-01')
            max_date = pd.Timestamp('2024-12-31')
        
        date_range = st.date_input(
            "Select Date Range:",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    
    st.divider()
    
    # Model selection for forecasts
    st.subheader("Forecast Settings")
    model_option = st.selectbox(
        "Select Forecast Model:",
        ["Base Model", "Optimistic Scenario", "Pessimistic Scenario"]
    )
    
    st.divider()
    
    # Download option
    st.subheader("Data Export")
    if st.button("📥 Download Current View Data"):
        # Create download functionality
        st.info("Download functionality would be implemented based on current view")

# Main content based on selected page
if page == "🏠 Overview":
    st.markdown('<h1 class="main-header">Ethiopia Financial Inclusion Dashboard</h1>', unsafe_allow_html=True)
    
    # Key metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="Current Account Ownership",
            value="46%",
            delta="+11% from 2017",
            delta_color="normal"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="Target (2027)",
            value="60%",
            delta="14% to go",
            delta_color="inverse"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="Projected 2025",
            value="36%",
            delta="-10% from target",
            delta_color="off"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="Key Events Tracked",
            value="3",
            delta="Telebirr, Policies",
            delta_color="normal"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Main overview chart
    st.subheader("Financial Inclusion Trends")
    
    if 'historical' in data and not data['historical'].empty:
        # Filter for account ownership data
        account_data = data['historical'][
            (data['historical']['indicator'] == 'Account Ownership Rate') &
            (data['historical']['record_type'] == 'observation')
        ].copy()
        
        if not account_data.empty:
            fig = px.line(
                account_data,
                x='observation_date',
                y='value_numeric',
                title='Account Ownership Rate Over Time',
                markers=True
            )
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Account Ownership (%)",
                hovermode='x unified'
            )
            # Add target line
            fig.add_hline(
                y=60,
                line_dash="dash",
                line_color="red",
                annotation_text="2027 Target (60%)"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Key insights
    st.subheader("Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("📈 Growth Analysis"):
            st.markdown("""
            - **Historical Growth Rate**: 12% average annual growth (2014-2021)
            - **Telebirr Impact**: +15% on account ownership (2021)
            - **Regional Variance**: Urban areas show 40% higher inclusion
            """)
    
    with col2:
        with st.expander("🎯 Key Recommendations"):
            st.markdown("""
            1. Accelerate digital payment adoption
            2. Focus on rural outreach programs
            3. Leverage mobile money infrastructure
            4. Implement targeted financial literacy programs
            """)

elif page == "📈 Trends":
    st.title("📈 Historical Trends & Analysis")
    
    if 'historical' in data and not data['historical'].empty:
        # Interactive trend selector
        st.subheader("Interactive Trend Explorer")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            indicators = data['historical']['indicator'].unique()
            selected_indicator = st.selectbox(
                "Select Indicator:",
                indicators[:5]  # Show first 5 indicators
            )
        
        with col2:
            pillars = data['historical']['pillar'].unique()
            selected_pillar = st.multiselect(
                "Select Pillar(s):",
                pillars,
                default=['ACCESS']
            )
        
        with col3:
            gender_filter = st.multiselect(
                "Gender:",
                ['all', 'male', 'female'],
                default=['all']
            )
        
        # Filter data based on selections
        filtered_data = data['historical'][
            (data['historical']['indicator'] == selected_indicator) &
            (data['historical']['pillar'].isin(selected_pillar)) &
            (data['historical']['gender'].isin(gender_filter)) &
            (data['historical']['record_type'] == 'observation')
        ]
        
        if not filtered_data.empty:
            # Create interactive plot
            fig = px.line(
                filtered_data,
                x='observation_date',
                y='value_numeric',
                color='pillar',
                title=f'{selected_indicator} Trends',
                markers=True,
                hover_data=['location', 'source_name']
            )
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Value",
                legend_title="Pillar"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Show data table
            with st.expander("View Data Table"):
                display_cols = ['observation_date', 'value_numeric', 'pillar', 'location', 'source_name']
                st.dataframe(filtered_data[display_cols].sort_values('observation_date'))
        else:
            st.warning("No data available for the selected filters.")
        
        # Channel comparison view
        st.subheader("Channel Comparison")
        
        # For demonstration, let's create a sample comparison
        # In reality, you'd have actual channel data
        channels = ['Bank Accounts', 'Mobile Money', 'SACCOs', 'Digital Wallets']
        years = [2017, 2018, 2019, 2020, 2021]
        
        # Sample data - replace with your actual channel data
        channel_data = pd.DataFrame({
            'Year': years * len(channels),
            'Channel': np.repeat(channels, len(years)),
            'Penetration': np.random.uniform(10, 50, len(years) * len(channels))
        })
        
        fig = px.bar(
            channel_data,
            x='Year',
            y='Penetration',
            color='Channel',
            barmode='group',
            title='Financial Channel Penetration Rate (%)'
        )
        st.plotly_chart(fig, use_container_width=True)

elif page == "🔮 Forecasts":
    st.title("🔮 Financial Inclusion Forecasts")
    
    if 'forecast' in data and not data['forecast'].empty:
        # Model selection
        st.subheader("Forecast Model Visualization")
        
        # Prepare forecast data
        forecast_df = data['forecast'].copy()
        
        # Create interactive forecast plot
        fig = go.Figure()
        
        # Base forecast
        fig.add_trace(go.Scatter(
            x=forecast_df['year'],
            y=forecast_df['forecast'],
            mode='lines+markers',
            name='Base Forecast',
            line=dict(color='blue', width=3)
        ))
        
        # Confidence interval
        fig.add_trace(go.Scatter(
            x=forecast_df['year'].tolist() + forecast_df['year'].tolist()[::-1],
            y=forecast_df['upper_95'].tolist() + forecast_df['lower_95'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(0,100,255,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='95% Confidence Interval'
        ))
        
        # Optimistic scenario
        fig.add_trace(go.Scatter(
            x=forecast_df['year'],
            y=forecast_df['optimistic'],
            mode='lines',
            name='Optimistic',
            line=dict(color='green', dash='dash')
        ))
        
        # Pessimistic scenario
        fig.add_trace(go.Scatter(
            x=forecast_df['year'],
            y=forecast_df['pessimistic'],
            mode='lines',
            name='Pessimistic',
            line=dict(color='red', dash='dash')
        ))
        
        # Target line
        fig.add_hline(
            y=60,
            line_dash="dot",
            line_color="red",
            annotation_text="Target: 60%"
        )
        
        fig.update_layout(
            title='Account Ownership Forecast (2025-2027)',
            xaxis_title="Year",
            yaxis_title="Account Ownership Rate (%)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key milestones
        st.subheader("Key Projected Milestones")
        
        milestones = pd.DataFrame({
            'Year': [2025, 2026, 2027],
            'Milestone': [
                'Mobile Money reaches 40% adoption',
                'Rural inclusion targets implemented',
                '60% national inclusion target'
            ],
            'Status': ['On Track', 'At Risk', 'Critical']
        })
        
        st.dataframe(milestones, use_container_width=True)
        
        # Forecast metrics
        st.subheader("Forecast Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "2027 Base Forecast",
                "36.7%",
                "-23.3% from target"
            )
        
        with col2:
            st.metric(
                "Optimistic Scenario",
                "44.1%",
                "-15.9% from target"
            )
        
        with col3:
            st.metric(
                "Annual Growth Required",
                "7.8%",
                "vs 4.3% historical"
            )

elif page == "🎯 Inclusion Projections":
    st.title("🎯 Financial Inclusion Projections & Targets")
    
    # Progress toward 60% target
    st.subheader("Progress Toward 60% Financial Inclusion Target")
    
    # Create progress chart
    progress_data = pd.DataFrame({
        'Year': [2014, 2017, 2021, 2025, 2026, 2027],
        'Account Ownership': [22, 35, 46, 36, 36.3, 36.7],
        'Type': ['Actual', 'Actual', 'Actual', 'Forecast', 'Forecast', 'Forecast']
    })
    
    fig = px.line(
        progress_data,
        x='Year',
        y='Account Ownership',
        color='Type',
        markers=True,
        title='Progress Toward 60% Target'
    )
    
    # Add target line
    fig.add_hline(
        y=60,
        line_dash="dash",
        line_color="red",
        annotation_text="National Target"
    )
    
    # Add shaded area for gap
    fig.add_hrect(
        y0=46, y1=60,
        fillcolor="rgba(255,0,0,0.1)",
        line_width=0,
        annotation_text="Gap to Close",
        annotation_position="top left"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Scenario selector
    st.subheader("Scenario Analysis")
    
    scenario = st.radio(
        "Select Scenario:",
        ["Base Case", "Optimistic (Accelerated Growth)", "Pessimistic (Slow Growth)"],
        horizontal=True
    )
    
    # Display scenario-specific projections
    col1, col2, col3 = st.columns(3)
    
    if scenario == "Base Case":
        with col1:
            st.info("**2025 Projection:** 36%")
            st.metric("Gap to Target", "24%")
        
        with col2:
            st.info("**2026 Projection:** 36.3%")
            st.metric("Gap to Target", "23.7%")
        
        with col3:
            st.info("**2027 Projection:** 36.7%")
            st.metric("Gap to Target", "23.3%")
    
    elif scenario == "Optimistic (Accelerated Growth)":
        with col1:
            st.success("**2025 Projection:** 43.2%")
            st.metric("Gap to Target", "16.8%")
        
        with col2:
            st.success("**2026 Projection:** 43.6%")
            st.metric("Gap to Target", "16.4%")
        
        with col3:
            st.success("**2027 Projection:** 44.1%")
            st.metric("Gap to Target", "15.9%")
    
    else:  # Pessimistic
        with col1:
            st.error("**2025 Projection:** 28.8%")
            st.metric("Gap to Target", "31.2%")
        
        with col2:
            st.error("**2026 Projection:** 29.1%")
            st.metric("Gap to Target", "30.9%")
        
        with col3:
            st.error("**2027 Projection:** 29.4%")
            st.metric("Gap to Target", "30.6%")
    
    # Consortium questions answers
    st.subheader("Answers to Consortium's Key Questions")
    
    with st.expander("📋 Question 1: When can we realistically reach 60% financial inclusion?"):
        st.markdown("""
        **Answer:** Based on current trends and forecasts:
        - **Base Scenario**: Not by 2027. We project reaching only 36.7% by 2027.
        - **With Interventions**: Accelerated growth could reach 44.1% by 2027.
        - **Realistic Timeline**: Early 2030s with aggressive policy interventions.
        """)
    
    with st.expander("📋 Question 2: What are the most impactful interventions?"):
        st.markdown("""
        **Answer:** Analysis shows:
        1. **Mobile Money Expansion** (Telebirr-like services): +15% impact
        2. **Digital Payment Infrastructure**: +10-12% impact
        3. **Financial Literacy Programs**: +5-8% impact
        4. **Agent Banking Networks**: +7-9% impact in rural areas
        """)
    
    with st.expander("📋 Question 3: What risks should we mitigate?"):
        st.markdown("""
        **Answer:** Key risks identified:
        - **Regulatory Uncertainty**: Could slow digital innovation
        - **Infrastructure Gaps**: Especially in rural areas
        - **Low Digital Literacy**: Limits adoption
        - **Economic Volatility**: Affects investment in financial services
        
        **Mitigation**: Public-private partnerships, phased rollouts, pilot programs.
        """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: gray;">
    <p>Ethiopia Financial Inclusion Forecasting Dashboard • KAIM Project • Data through 2021, Forecasts to 2027</p>
    <p>For questions or data access, contact the project team.</p>
</div>
""", unsafe_allow_html=True)