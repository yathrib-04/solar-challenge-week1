# Solar Data Streamlit Dashboard

## Overview
This app provides an interactive dashboard to visualize and compare solar energy data from Benin, Togo, and Sierra Leone. Built with Streamlit, it allows users to select countries, choose metrics, and view boxplots and summary tables.

## How to Run Locally
1. Install requirements:
   ```sh
   pip install -r requirements.txt
   pip install streamlit
   ```
2. From the project root, run:
   ```sh
   streamlit run app/main.py
   ```
3. The dashboard will open in your browser.

## Features
- Country selection via sidebar
- Metric selection (GHI, DNI, DHI)
- Interactive boxplots
- Table of top countries by average GHI

## Development Process
- Modularized data loading in `app/utils.py`
- Main dashboard logic in `app/main.py`
- Data is read from local cleaned CSVs in the `data/` directory (not committed to git)

## Deployment
To deploy to Streamlit Community Cloud, push your code to GitHub and follow the [Streamlit deployment guide](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app).

## Author
- Teyiba Aman 