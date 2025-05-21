import pandas as pd
import numpy as np
from pathlib import Path

def clean_solar_data(file_path: str, country: str) -> pd.DataFrame:
    """
    Clean solar data for a specific country.
    
    Args:
        file_path (str): Path to the raw data file
        country (str): Country name
        
    Returns:
        pd.DataFrame: Cleaned dataset
    """
    # Read the data
    df = pd.read_csv(file_path)
    
    # Convert timestamp to datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Handle missing values
    # For solar irradiance metrics, replace negative values with 0
    irradiance_cols = ['GHI', 'DNI', 'DHI']
    for col in irradiance_cols:
        if col in df.columns:
            df[col] = df[col].clip(lower=0)
    
    # Remove rows with all irradiance values missing
    if all(col in df.columns for col in irradiance_cols):
        df = df.dropna(subset=irradiance_cols, how='all')
    
    # Add country column
    df['Country'] = country
    
    return df

def main():
    # Create data directory if it doesn't exist
    data_dir = Path('../data')
    data_dir.mkdir(exist_ok=True)
    
    # Define file mappings
    files = {
        'benin-malanville.csv': 'Benin',
        'togo-dapaong_qc.csv': 'Togo',
        'sierraleone-bumbuna.csv': 'Sierra Leone'
    }
    
    # Process each file
    for file_name, country in files.items():
        print(f"Processing {country} data...")
        
        # Clean the data
        df = clean_solar_data(file_name, country)
        
        # Save cleaned data
        output_file = data_dir / f"{country.lower().replace(' ', '_')}_clean.csv"
        df.to_csv(output_file, index=False)
        print(f"Saved cleaned data to {output_file}")

if __name__ == "__main__":
    main() 