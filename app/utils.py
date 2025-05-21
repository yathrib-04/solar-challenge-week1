import pandas as pd
from pathlib import Path
from typing import Dict

def load_cleaned_data(data_dir: Path = Path('../data')) -> Dict[str, pd.DataFrame]:
    """
    Load cleaned solar datasets for Benin, Togo, and Sierra Leone.

    Parameters:
        data_dir (Path): Path to the data directory.

    Returns:
        dict: Dictionary with country names as keys and DataFrames as values.
    """
    data = {
        'Benin': pd.read_csv(data_dir / 'benin_clean.csv'),
        'Togo': pd.read_csv(data_dir / 'togo_clean.csv'),
        'Sierra Leone': pd.read_csv(data_dir / 'sierraleone_clean.csv')
    }
    return data 