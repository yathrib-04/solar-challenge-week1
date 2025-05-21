import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from app.utils import load_cleaned_data

st.set_page_config(page_title="Solar Data Dashboard", layout="wide")
st.title("Cross-Country Solar Data Dashboard")
st.markdown("""
This interactive dashboard allows you to explore and compare solar energy data from Benin, Togo, and Sierra Leone.\
Select countries and metrics to visualize boxplots and see top regions by solar potential.
""")

# Load data
data = load_cleaned_data()

# Sidebar for country and metric selection
st.sidebar.header("Options")
country_options = list(data.keys())
selected_countries = st.sidebar.multiselect(
    "Select countries:", country_options, default=country_options
)
metric_options = ['GHI', 'DNI', 'DHI']
selected_metric = st.sidebar.selectbox("Select metric:", metric_options)

# Filter data based on selection
filtered_data = {c: df for c, df in data.items() if c in selected_countries}

# Boxplot
st.subheader(f"Boxplot of {selected_metric} by Country")
if filtered_data:
    plot_data = pd.DataFrame({c: df[selected_metric] for c, df in filtered_data.items()})
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=plot_data, ax=ax, palette='Set2')
    ax.set_xlabel("Country")
    ax.set_ylabel(selected_metric)
    st.pyplot(fig)
else:
    st.info("Please select at least one country.")

# Top regions table (by mean GHI)
st.subheader("Top Countries by Average GHI")
avg_ghi = {c: df['GHI'].mean() for c, df in filtered_data.items()}
top_ghi_df = pd.DataFrame(list(avg_ghi.items()), columns=["Country", "Average GHI"]).sort_values(by="Average GHI", ascending=False)
st.table(top_ghi_df)

st.markdown("---")
st.markdown("Developed for Solar Challenge Week 1 | [Teyiba Aman]")