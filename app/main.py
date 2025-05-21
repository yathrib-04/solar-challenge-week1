import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_cleaned_data
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page config
st.set_page_config(
    page_title="Solar Data Analysis",
    page_icon="☀️",
    layout="wide"
)

# Title and description
st.title("Solar Energy Data Analysis Dashboard")
st.markdown("""
This dashboard provides an interactive visualization of solar energy data from Benin, Togo, and Sierra Leone.
Select countries and metrics to compare their solar energy characteristics.
""")

try:
    # Load data with validation
    data = load_cleaned_data()
    
    # Sidebar for country selection
    st.sidebar.header("Country Selection")
    selected_countries = st.sidebar.multiselect(
        "Select countries to compare",
        options=list(data.keys()),
        default=list(data.keys())
    )
    
    if not selected_countries:
        st.warning("Please select at least one country to view the analysis.")
        st.stop()
    
    # Metric selection
    metric = st.sidebar.selectbox(
        "Select metric to compare",
        options=['GHI', 'DNI', 'DHI'],
        help="GHI: Global Horizontal Irradiance\nDNI: Direct Normal Irradiance\nDHI: Diffuse Horizontal Irradiance"
    )
    
    # Create boxplot
    st.header(f"{metric} Comparison")
    
    # Prepare data for plotting
    plot_data = []
    for country in selected_countries:
        df = data[country].copy()
        df['Country'] = country
        plot_data.append(df[['Country', metric]])
    
    plot_df = pd.concat(plot_data)
    
    # Create and display boxplot
    fig = px.box(
        plot_df,
        x='Country',
        y=metric,
        title=f"{metric} Distribution by Country",
        color='Country'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Display data quality metrics
    st.header("Data Quality Metrics")
    for country in selected_countries:
        with st.expander(f"Quality Metrics for {country}"):
            metrics = data[country].attrs.get('quality_metrics', {})
            
            # Missing values
            st.subheader("Missing Values")
            missing_df = pd.DataFrame(metrics.get('missing_values', {}), index=['Count']).T
            st.dataframe(missing_df)
            
            # Outliers
            st.subheader("Outliers (beyond 3 standard deviations)")
            outliers_df = pd.DataFrame(metrics.get('outliers', {}), index=['Count']).T
            st.dataframe(outliers_df)
    
    # Summary statistics
    st.header("Summary Statistics")
    summary_data = []
    for country in selected_countries:
        stats = data[country][metric].describe()
        stats['Country'] = country
        summary_data.append(stats)
    
    summary_df = pd.DataFrame(summary_data)
    summary_df = summary_df.set_index('Country')
    st.dataframe(summary_df)
    
    # Top regions by average GHI
    st.header("Top Regions by Average GHI")
    ghi_means = {country: data[country]['GHI'].mean() for country in selected_countries}
    top_regions = pd.DataFrame({
        'Country': list(ghi_means.keys()),
        'Average GHI': list(ghi_means.values())
    }).sort_values('Average GHI', ascending=False)
    
    st.dataframe(top_regions)
    
except FileNotFoundError as e:
    st.error(f"Data files not found. Please ensure all required data files are in the data directory.")
    logger.error(f"File not found error: {e}")
except ValueError as e:
    st.error(f"Data validation error: {e}")
    logger.error(f"Validation error: {e}")
except Exception as e:
    st.error("An unexpected error occurred. Please check the logs for details.")
    logger.error(f"Unexpected error: {e}")

st.markdown("---")
st.markdown("Developed for Solar Challenge Week 1 | [Teyiba Aman]")