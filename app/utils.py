import pandas as pd
import logging
from pathlib import Path
import numpy as np
from typing import Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_dataframe(df: pd.DataFrame, country: str) -> bool:
    """
    Validate the dataframe for required columns and data quality.
    
    Args:
        df: DataFrame to validate
        country: Name of the country for logging
    
    Returns:
        bool: True if validation passes, False otherwise
    """
    required_columns = ['GHI', 'DNI', 'DHI']
    
    # Check for required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        logger.error(f"{country} data missing required columns: {missing_columns}")
        return False
    
    # Check for negative values
    for col in required_columns:
        if (df[col] < 0).any():
            logger.warning(f"{country} data contains negative values in {col}")
    
    # Check for missing values
    missing_values = df[required_columns].isnull().sum()
    if missing_values.any():
        logger.warning(f"{country} data contains missing values:\n{missing_values}")
    
    # Check for outliers (values beyond 3 standard deviations)
    for col in required_columns:
        mean = df[col].mean()
        std = df[col].std()
        outliers = df[abs(df[col] - mean) > 3 * std]
        if not outliers.empty:
            logger.warning(f"{country} data contains {len(outliers)} outliers in {col}")
    
    return True

def load_cleaned_data(data_dir: Path = Path('../data')) -> Dict[str, pd.DataFrame]:
    """
    Load cleaned solar datasets for Benin, Togo, and Sierra Leone.

    Parameters:
        data_dir (Path): Path to the data directory.

    Returns:
        dict: Dictionary with country names as keys and DataFrames as values.
    """
    try:
        logger.info(f"Loading data from {data_dir}")
        
        if not data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {data_dir}")
        
        data = {
            'Benin': pd.read_csv(data_dir / 'benin_clean.csv'),
            'Togo': pd.read_csv(data_dir / 'togo_clean.csv'),
            'Sierra Leone': pd.read_csv(data_dir / 'sierraleone_clean.csv')
        }
        
        # Validate each dataset
        for country, df in data.items():
            logger.info(f"Validating {country} data...")
            if not validate_dataframe(df, country):
                raise ValueError(f"Data validation failed for {country}")
            
            # Add data quality metrics
            df.attrs['quality_metrics'] = {
                'missing_values': df.isnull().sum().to_dict(),
                'outliers': {
                    col: len(df[abs(df[col] - df[col].mean()) > 3 * df[col].std()])
                    for col in ['GHI', 'DNI', 'DHI']
                }
            }
        
        logger.info("All data loaded and validated successfully")
        return data
        
    except FileNotFoundError as e:
        logger.error(f"Data file not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise 