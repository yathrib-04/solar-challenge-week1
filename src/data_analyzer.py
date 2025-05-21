import pandas as pd
import numpy as np
from scipy import stats
from typing import List, Dict, Tuple
import plotly.express as px
from windrose import WindroseAxes
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalyzer:
    """Class for performing various analyses on solar data."""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize the DataAnalyzer.
        
        Args:
            data (pd.DataFrame): Input dataset
        """
        self.data = data.copy()
        
    def detect_outliers(self, columns: List[str], z_threshold: float = 3) -> Dict[str, int]:
        """
        Detect outliers in specified columns using Z-score method.
        
        Args:
            columns (List[str]): List of column names to analyze
            z_threshold (float): Z-score threshold for outlier detection
            
        Returns:
            Dict[str, int]: Dictionary with column names and number of outliers
        """
        outliers_count = {}
        
        for col in columns:
            z_scores = stats.zscore(self.data[col], nan_policy='omit')
            outliers = abs(z_scores) > z_threshold
            outliers_count[col] = sum(outliers)
            
        return outliers_count
    
    def analyze_time_series(self, columns: List[str]) -> Dict[str, pd.Series]:
        """
        Analyze time series data for specified columns.
        
        Args:
            columns (List[str]): List of column names to analyze
            
        Returns:
            Dict[str, pd.Series]: Dictionary with column names and their time series data
        """
        if 'Timestamp' not in self.data.columns:
            raise ValueError("Timestamp column not found in data")
            
        self.data['Timestamp'] = pd.to_datetime(self.data['Timestamp'])
        time_series = {}
        
        for col in columns:
            time_series[col] = self.data.set_index('Timestamp')[col]
            
        return time_series
    
    def analyze_cleaning_impact(self, module_columns: List[str]) -> pd.DataFrame:
        """
        Analyze the impact of cleaning on module performance.
        
        Args:
            module_columns (List[str]): List of module performance columns
            
        Returns:
            pd.DataFrame: Aggregated statistics by cleaning status
        """
        if 'Cleaning' not in self.data.columns:
            raise ValueError("Cleaning column not found in data")
            
        return self.data.groupby('Cleaning')[module_columns].agg(['mean', 'std'])
    
    def calculate_correlations(self, columns: List[str]) -> pd.DataFrame:
        """
        Calculate correlation matrix for specified columns.
        
        Args:
            columns (List[str]): List of column names to analyze
            
        Returns:
            pd.DataFrame: Correlation matrix
        """
        return self.data[columns].corr()
    
    def analyze_wind(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Analyze wind data for wind rose plot.
        
        Returns:
            Tuple[np.ndarray, np.ndarray]: Wind direction and wind speed arrays
        """
        if 'WD' not in self.data.columns or 'WS' not in self.data.columns:
            raise ValueError("Wind direction (WD) or wind speed (WS) columns not found")
            
        return self.data['WD'].values, self.data['WS'].values
    
    def analyze_temperature_humidity(self) -> pd.DataFrame:
        """
        Analyze relationship between temperature, GHI, and humidity.
        
        Returns:
            pd.DataFrame: DataFrame with relevant columns for analysis
        """
        required_columns = ['Tamb', 'GHI', 'RH']
        if not all(col in self.data.columns for col in required_columns):
            raise ValueError("Required columns (Tamb, GHI, RH) not found in data")
            
        return self.data[required_columns] 